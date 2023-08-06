"""A Mattermost integration Plugin"""
from typing import Sequence, Any
import requests
from cmem_plugin_base.dataintegration.context import (
    ExecutionContext,
    ExecutionReport,
    PluginContext
)
from cmem_plugin_base.dataintegration.description import Plugin, PluginParameter
from cmem_plugin_base.dataintegration.entity import Entities
from cmem_plugin_base.dataintegration.parameter.multiline import (
    MultilineStringParameterType,
)
from cmem_plugin_base.dataintegration.parameter.password import Password
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin
from cmem_plugin_base.dataintegration.types import Autocompletion, StringParameterType


def header(access_token: Password):
    """Request Header"""
    api_header = {
        "Authorization": f"Bearer {access_token.decrypt()}",
        "Content-Type": "application/json",
    }
    return api_header


def get_request_handler(url: str,
                        url_extend: str,
                        access_token: Password):
    """Handle get requests"""
    response = requests.get(
        f"{url}/api/v4/{url_extend}",
        headers=header(access_token),
        timeout=2,
    )
    return response


def get_dataset(url: str,
                url_expand: str,
                access_token: Password,
                query_terms: list[str]) -> Any:
    """create a list of usernames"""
    term = ""
    payload = {"term": term.join(query_terms), }
    response = requests.post(
        f"{url}/api/v4/{url_expand}/search",
        headers=header(access_token),
        json=payload,
        timeout=2,
    )
    return response.json()


class MattermostSearch(StringParameterType):
    """Mattermost Search Type"""

    def __init__(
            self,
            url_expand: str,
            display_name: str,
    ) -> None:
        self.url_expand = url_expand
        self.display_name = display_name

    autocompletion_depends_on_parameters: list[str] = ["url", "access_token"]

    # auto complete for values
    allow_only_autocompleted_values: bool = True
    # auto complete for labels
    autocomplete_value_with_labels: bool = True

    def autocomplete(
        self,
        query_terms: list[str],
        depend_on_parameter_values: list[Any],
        context: PluginContext,
    ) -> list[Autocompletion]:
        if not depend_on_parameter_values:
            raise ValueError("Input url and access token first.")
        result = []
        if len(query_terms) != 0:
            datasets = get_dataset(depend_on_parameter_values[0],
                                   self.url_expand,
                                   depend_on_parameter_values[1],
                                   query_terms
                                   )
            for object_name in datasets:
                result.append(
                    Autocompletion(
                        value=f"{object_name[self.display_name]}",
                        label=f"{object_name[self.display_name]}",
                    )
                )
            result.sort(key=lambda x: x.label)  # type: ignore
            return result
        if len(query_terms) == 0:
            label = f"Enter a letter to get a list of {self.url_expand}."
            result.append(Autocompletion(value="", label=f"{label}"))
        result.sort(key=lambda x: x.label)  # type: ignore
        return result


@Plugin(
    label="Mattermost Plugin",
    plugin_id="cmem_plugin_mattermost",
    description="Sends automated messages in Mattermost"
    " via bot to channels or direct to users ",
    documentation="""This Plugin sends messages via
    Mattermost bot to channel(s) or user(s).

The plugin can send messages to users and/or channels
on your Mattermost server through your preset bot.

<h2>Workflow mode</h2>

The plugin can send a static message to the pre-configured parameters.
This message will be sent to the defined user and/or
channel every time the workflow is executed.

For dynamic messages, the input of the parameters
user, channel, message is done by an input via entities.
""",
    parameters=[
        PluginParameter(
            name="url",
            label="URL",
            description="url of mattermost server.",
        ),
        PluginParameter(
            name="access_token",
            label="Access Token",
            description="access token of the bot",
        ),
        PluginParameter(
            name="bot_name",
            label="Bot name",
            description="name or display name",
        ),
        PluginParameter(
            name="user",
            label="User",
            description="user who get the message",
            param_type=MattermostSearch("users", "username"),
            default_value="",
        ),
        PluginParameter(
            name="channel",
            label="Channel",
            description="The name or display name"
            " If you want to send your message to multiple"
            " channel separate them with a comma.",
            param_type=MattermostSearch("channels", "name"),
            default_value="",
        ),
        PluginParameter(
            name="message",
            label="Message",
            description="max 16383 character",
            param_type=MultilineStringParameterType(),
            default_value="",
        ),
    ],
)
class MattermostPlugin(WorkflowPlugin):
    """A Mattermost integration Plugin with static messaging"""

    # pylint: disable=R0913
    def __init__(
        self,
        url: str,
        access_token: Password,
        bot_name: str,
        user: str,
        channel: str,
        message: str,
    ) -> None:
        self.url = url
        self.access_token = access_token
        self.bot_name = bot_name
        self.user = user
        self.channel = channel
        self.message = message

    def execute(self, inputs: Sequence[Entities], context: ExecutionContext) -> None:
        self.log.info("Mattermost plugin started.")
        # fix message with every start, could be used at creating of the workflow item
        if not self.user and not self.channel and not inputs:
            pass
        if self.user or self.channel:
            self.send_message_to_provided_parameter()
        if inputs:
            entities_counter = 0
            channel_counter = 0
            channels: list = []
            users: list = []
            user_counter = 0
            # Entity/ies
            for item in inputs:
                column_names = [ep.path for ep in item.schema.paths]
                # columns of given Entity
                for entity in item.entities:
                    entities_counter += 1
                    self.user = ""
                    self.channel = ""
                    self.message = ""
                    i = 0
                    # row of given Entity
                    for _ in column_names:
                        if len(entity.values[i]) > 0:
                            param_value = entity.values[i][0]
                        else:
                            param_value = ""
                        if _ == "user" and param_value != "":
                            self.user = param_value
                            user_counter += 1
                            users.append(self.user)
                        elif _ == "channel" and param_value != "":
                            self.channel = param_value
                            channels.append(self.channel)
                            channel_counter += 1
                        elif _ == "message" and param_value != "":
                            self.message = param_value
                        i += 1
                    self.send_message_to_provided_parameter()
            users = list(dict.fromkeys(users))
            channels = list(dict.fromkeys(channels))
            context.report.update(
                ExecutionReport(
                    entity_count=entities_counter,
                    operation="write",
                    operation_desc="entities received",
                    summary=[
                        ("No. of messages send:", f"{entities_counter}"),
                        ("No. of direct messages", f"{user_counter}"),
                        ("No. of channel messages", f"{channel_counter}"),
                        ("Channels that received a message", f"{', '.join(channels)}"),
                        ("Users who received a message", f"{', '.join(users)}"),
                    ],
                )
            )

    def post_request_handler(self, url_expand, payload):
        """Handle post requests"""
        response = requests.post(
            f"{self.url}/api/v4/{url_expand}",
            headers=header(self.access_token),
            json=payload,
            timeout=2,
        )
        return response

    def get_id(self, obj_name):
        """Request to find the ID"""
        if obj_name:
            response = get_dataset(self.url, "users", self.access_token, [obj_name])
            for _ in response:
                if obj_name in (_["username"],
                                _["nickname"],
                                _["email"],
                                f'{_["first_name"]} {_["last_name"]}'
                                ):
                    return _["id"]
        raise ValueError(f"ID not found, check {obj_name} parameter.")

    def send_message_with_bot_to_user(self):
        """sends messages from bot to one or more users."""
        # payload for json to generate a direct channel with post request
        data = [self.get_id(self.bot_name), self.get_id(self.user)]
        # post request to generate the direct channel
        response = self.post_request_handler("channels/direct", data)
        channel_id = response.json()["id"]
        # payload for the json to generate the message
        payload = {"channel_id": channel_id, "message": self.message}
        # post request to send the message
        self.post_request_handler("posts", payload)

    def get_channel_id(self):
        """Request to find the channel ID with the bot name"""
        if not self.channel:
            raise ValueError("No channel name was provided.")
        list_channel_data = get_dataset(self.url,
                                        "channels",
                                        self.access_token,
                                        [self.channel])
        for _ in list_channel_data:
            if self.channel in (_["name"], _["display_name"]):
                return _["id"]
        raise ValueError(f"Channel {self.channel} do not exist.")

    def send_message_with_bot_to_channel(self) -> None:
        """sends messages from bot to channel."""
        # payload for the json to generate the message
        payload = {"channel_id": self.get_channel_id(),
                   "message": self.message}
        # Post request for the message
        self.post_request_handler("posts", payload)

    def send_message_to_provided_parameter(self) -> None:
        """will test if the message is sending to user or channel or both"""
        if self.message:
            if self.user and self.channel:
                self.send_message_with_bot_to_channel()
                self.send_message_with_bot_to_user()
            elif self.user and not self.channel:
                self.send_message_with_bot_to_user()
            elif self.channel and not self.user:
                self.send_message_with_bot_to_channel()
        else:
            raise ValueError("No recipient.")
