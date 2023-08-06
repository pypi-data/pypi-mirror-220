import unittest

from switcore.action.activity_router import ActivityRouter, PathResolver
from switcore.action.schemas import SwitRequest, BaseState, SwitResponse, ViewCallbackType
from tests.utils import ViewIdTypes, ActionIdTypes, create_activity_handler, create_swit_request


class RouterTest(unittest.IsolatedAsyncioTestCase):
    async def test_router(self):
        activity_router = ActivityRouter()
        swit_request = create_swit_request(
            ViewIdTypes.right_panel, str(PathResolver(ActionIdTypes.test_action_id, ["a", 1])))

        @activity_router.register([ViewIdTypes.right_panel], ActionIdTypes.test_action_id)
        async def draw_webhook_create(request: SwitRequest, state: BaseState, a: str, number: int):  # noqa
            self.assertEqual(a, "a")
            self.assertEqual(number, 1)
            return SwitResponse(callback_type=ViewCallbackType.update)

        activity_handler = create_activity_handler()
        activity_handler.include_activity_router(activity_router)

        swit_response = await activity_handler.on_view_actions_submit(swit_request, BaseState())
        self.assertTrue(isinstance(swit_response, SwitResponse))

    async def test_escape_router(self):
        activity_router = ActivityRouter()
        swit_request = create_swit_request(
            ViewIdTypes.right_panel, str(PathResolver(ActionIdTypes.test_escape_action_id, ["a", 1])))

        @activity_router.register([ViewIdTypes.right_panel], ActionIdTypes.test_escape_action_id)
        async def draw_webhook_create(request: SwitRequest, state: BaseState, a: str, number: int):  # noqa
            self.assertEqual(a, "a")
            self.assertEqual(number, 1)
            return SwitResponse(callback_type=ViewCallbackType.update)

        activity_handler = create_activity_handler()
        activity_handler.include_activity_router(activity_router)

        swit_response = await activity_handler.on_view_actions_submit(swit_request, BaseState())
        self.assertTrue(isinstance(swit_response, SwitResponse))
