"""Regression tests for the course documentation checker."""

from pathlib import Path
import tempfile
import unittest

from check_course_docs import check_commands, check_links, heading_anchors


class CourseDocsChecks(unittest.TestCase):
    """Ensure malformed references fail instead of producing a false pass."""

    def test_repeated_heading_anchors(self):
        self.assertEqual(heading_anchors('# Build\n## Build\n## Test!\n'),
                         {'build', 'build-1', 'test'})

    def test_links_and_heading_fragments(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'README.md'
            path.write_text('# Build\n')
            self.assertEqual(check_links(path, '[build](#build)'), [])
            self.assertEqual(len(check_links(path, '[wrong](#missing)')), 1)
            self.assertEqual(len(check_links(path, '[file](missing.md)')), 1)
            self.assertEqual(check_links(path, '[web](https://example.com)'), [])

    def test_local_executable_and_launch_names(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'README.md'
            packages = {'demo': {'node'}}
            self.assertEqual(check_commands(root, path, 'ros2 run demo node', packages), [])
            self.assertEqual(len(check_commands(root, path, 'ros2 run demo typo', packages)), 1)
            self.assertEqual(len(check_commands(root, path, 'ros2 launch demo lost.py', packages)), 1)
            launch = root / 'src/demo/launch/demo.launch.py'
            launch.parent.mkdir(parents=True)
            launch.write_text('')
            self.assertEqual(check_commands(root, path, 'ros2 launch demo demo.launch.py', packages), [])

    def test_shell_syntax_and_python_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / 'README.md'
            self.assertEqual(check_commands(root, path, '```bash\necho "ok"\n```', {}), [])
            self.assertTrue(check_commands(root, path, '```bash\necho "unclosed\n```', {}))
            self.assertTrue(check_commands(root, path, 'python3 src/missing.py', {}))


if __name__ == '__main__':
    unittest.main()
