import unittest
from unittest.mock import patch, call, MagicMock
from datetime import datetime
from PreSyncEodDumpFile import main, sync_and_clean_vox_eod_dump_file, printlog  # Update to actual file name
import logging


class TestPreSyncEodDumpFile(unittest.TestCase):
    @patch("os.path.join")
    @patch("subprocess.run")
    def test_sync_and_clean_vox_eod_dump_file(self, mock_subprocess_run, mock_path_join):
        # Mock directory path joining
        mock_path_join.side_effect = lambda *args: "/".join(args)

        # Mock subprocess.run to simulate command execution
        mock_subprocess_run.return_value = MagicMock(stdout="Command executed successfully")

        # Call the function
        sync_and_clean_vox_eod_dump_file("20250108", "20250109", "/mock/input/dir", 5)

        # Assertions to validate subprocess commands
        clean_cmd = "find /mock/input/dir/2025/01/08 -mtime +5 -exec rm -f {} \\;"
        mkdir_cmd = "mkdir -p /mock/input/dir/2025/01/09"
        rsync_cmd = "rsync -trp /mock/input/dir/2025/01/08/ /mock/input/dir/2025/01/09/"

        mock_subprocess_run.assert_has_calls([
            call(clean_cmd, shell=True),
            call(mkdir_cmd, shell=True),
            call(rsync_cmd, shell=True, capture_output=True, text=True)
        ])

    @patch("datetime.datetime")
    @patch("builtins.print")
    def test_printlog(self, mock_print, mock_datetime):
        # Mock current time
        mock_datetime.now.return_value = datetime(2025, 1, 9, 12, 0, 0)

        # Call printlog
        printlog("Test log message")

        # Assert print output
        mock_print.assert_called_once_with("2025-01-09 12:00:00: Test log message")

    @patch("argparse.ArgumentParser.parse_args")
    @patch("PreSyncEodDumpFile.sync_and_clean_vox_eod_dump_file")  # Update with actual module name
    def test_main(self, mock_sync_and_clean, mock_parse_args):
        # Mock command-line arguments
        mock_parse_args.return_value = MagicMock(input="/mock/input/dir", keep_days=5)

        # Mock datetime
        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 1, 9)
            mock_datetime.strftime = datetime.strftime

            # Call main
            main()

            # Expected dates
            previous_working_date = "20250108"
            today = "20250109"

            # Assert the sync_and_clean_vox_eod_dump_file function is called with expected arguments
            mock_sync_and_clean.assert_called_once_with(
                previous_working_date, today, "/mock/input/dir", 5
            )

    @patch("argparse.ArgumentParser.parse_args")
    def test_main_invalid_arguments(self, mock_parse_args):
        # Mock invalid arguments
        mock_parse_args.return_value = MagicMock(input=None, keep_days=5)

        # Mock logging
        with patch("PreSyncEodDumpFile.logging") as mock_logging:  # Update with actual module name
            with self.assertRaises(SystemExit):
                main()
            mock_logging.error.assert_called_once_with("Input directory is required")


if __name__ == "__main__":
    unittest.main()
