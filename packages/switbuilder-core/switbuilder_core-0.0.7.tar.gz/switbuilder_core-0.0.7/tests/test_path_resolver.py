import unittest

from switcore.action.activity_router import PathResolver
from tests.utils import ActionIdTypes


class PathResolverTest(unittest.TestCase):
    def test_combined_path(self):
        path_resolver: PathResolver = PathResolver(ActionIdTypes.test_action_id, ["a"])
        self.assertEqual(path_resolver.combined_path, "test_action_id/a")
        self.assertEqual(path_resolver.id, "test_action_id")

        path_resolver._paths.append("b")
        self.assertEqual(path_resolver.combined_path, "test_action_id/a/b")
        self.assertEqual(path_resolver.id, "test_action_id")

    def test_from_combined(self):
        path_resolver: PathResolver = PathResolver.from_combined("test_action_id/a/b")
        self.assertEqual(path_resolver.combined_path, "test_action_id/a/b")
        self.assertEqual(path_resolver.id, "test_action_id")
        self.assertEqual(path_resolver._paths, ["a", "b"])

    def test_convert_int(self):
        path_resolver: PathResolver = PathResolver(ActionIdTypes.test_action_id, [1, "a"])
        self.assertEqual(path_resolver.combined_path, "test_action_id/1/a")
        self.assertEqual(path_resolver.paths, [1, "a"])

    def test_escape(self):
        path_resolver: PathResolver = PathResolver(ActionIdTypes.test_escape_action_id, ["a"])
        self.assertEqual(path_resolver.combined_path, "test_escape_action_id\escape/a")
        self.assertEqual(path_resolver.id, "test_escape_action_id\escape")
        self.assertEqual(path_resolver.paths, ["a"])

        path_resolver: PathResolver = PathResolver(ActionIdTypes.test_escape_action_id, ["a/b"])
        self.assertEqual(path_resolver.combined_path, "test_escape_action_id\escape/a\\b")
        self.assertEqual(path_resolver.id, "test_escape_action_id\escape")
        self.assertEqual(path_resolver.paths, ["a\\b"])
