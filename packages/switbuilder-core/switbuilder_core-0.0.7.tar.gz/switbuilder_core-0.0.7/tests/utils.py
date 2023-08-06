import datetime
from enum import Enum

from switcore.action.activity_handler_abc import ActivityHandlerABC
from switcore.action.schemas import SwitRequest, PlatformTypes, UserInfo, UserPreferences, Context, UserAction, \
    UserActionType, View, Body, BaseState, SwitResponse
from switcore.ui.header import Header


class ActionIdTypes(str, Enum):
    test_action_id = "test_action_id"
    test_escape_action_id = "test_escape_action_id/escape"


class ViewIdTypes(str, Enum):
    right_panel = "right_panel"


class ActivityHandler(ActivityHandlerABC):

    async def on_right_panel_open(self, swit_request: SwitRequest, state: BaseState) -> SwitResponse:
        pass

    async def on_presence_sync(self, swit_request: SwitRequest, state: BaseState) -> SwitResponse:
        pass

    async def on_user_commands_chat(self, swit_request: SwitRequest, state: BaseState) -> SwitResponse:
        pass

    async def on_user_commands_chat_extension(self, swit_request: SwitRequest, state: BaseState) -> SwitResponse:
        pass

    async def on_user_commands_chat_commenting(self, swit_request: SwitRequest, state: BaseState) -> SwitResponse:
        pass

    async def on_user_commands_context_menus_message(self, swit_request: SwitRequest, state: BaseState) -> SwitResponse:
        pass

    async def on_user_commands_context_menus_message_comment(self, swit_request: SwitRequest,
                                                             state: BaseState) -> SwitResponse:
        pass

    async def on_view_actions_drop(self, swit_request: SwitRequest, state: BaseState) -> SwitResponse:
        pass

    async def on_view_actions_input(self, swit_request: SwitRequest, state: BaseState) -> SwitResponse:
        pass

    async def on_view_actions_oauth_complete(self, swit_request: SwitRequest, state: BaseState) -> SwitResponse:
        pass


def create_swit_request(view_id: ViewIdTypes, action_id: str):
    return SwitRequest(
        platform=PlatformTypes.DESKTOP,
        time=datetime.datetime.now(),
        app_id="test_app_id",
        user_info=UserInfo(
            user_id="test_user_id",
            organization_id="test_organization_id"
        ),
        user_preferences=UserPreferences(
            language="ko",
            time_zone_offset="+0900",
            color_theme="light"
        ),
        context=Context(
            workspace_id="test_workspace_id",
            channel_id="test_channel_id"
        ),
        user_action=UserAction(
            type=UserActionType.view_actions_submit,
            id=action_id,
            slash_command="test_slash_command",
        ),
        current_view=View(
            view_id=view_id,
            state="state",
            header=Header(
                title="test_title",
            ),
            body=Body(),
        ))


def create_activity_handler():
    return ActivityHandler()
