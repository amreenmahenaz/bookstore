import unittest
from unittest.mock import patch, MagicMock
from gs_secure_cmd import (
    parse_arguments,
    invoke_gs_script,
    build_gs_script,
    build_options,
)

class TestGSSecureCmd(unittest.TestCase):
    def test_parse_arguments(self):
        with patch("sys.argv", ["gs_secure_cmd.py", "--cmd", "deploy", "--user", "test_user",
                                "--pass_file", "test_pass_file", "--gs_version", "1.0"]):
            args = parse_arguments()
            self.assertEqual(args.cmd, "deploy")
            self.assertEqual(args.user, "test_user")
            self.assertEqual(args.pass_file, "test_pass_file")
            self.assertEqual(args.gs_version, "1.0")

    def test_build_gs_script(self):
        result = build_gs_script("test_user", "test_password", "deploy", "1.0")
        self.assertIn("--username=test_user", result)
        self.assertIn("--password=test_password", result)
        self.assertIn("deploy", result)

    def test_build_options(self):
        result = build_options("pu deploy", "zone1", "props", "override", "test.jar")
        self.assertIn("--zones=zone1", result)
        self.assertIn("props", result)
        self.assertIn("override", result)
        self.assertIn("test.jar", result)

    @patch("gs_secure_cmd.subprocess.check_output")
    def test_invoke_gs_script_success(self, mock_check_output):
        mock_check_output.return_value = "Command executed successfully"
        result = invoke_gs_script("dummy_gs_script", "dummy_args")
        self.assertEqual(result, "Command executed successfully")
        mock_check_output.assert_called_once_with("dummy_gs_script dummy_args", shell=True, text=True)

    @patch("gs_secure_cmd.subprocess.check_output")
    def test_invoke_gs_script_failure(self, mock_check_output):
        mock_check_output.side_effect = subprocess.CalledProcessError(1, "cmd", "Error output")
        with self.assertRaises(SystemExit):
            invoke_gs_script("dummy_gs_script", "dummy_args")

if __name__ == "__main__":
    unittest.main()
