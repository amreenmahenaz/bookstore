import unittest
from unittest.mock import patch, call, MagicMock
from datetime import datetime
from PreSyncEodDumpFile import main, sync_and_clean_vox_eod_dump_file, printlog  # Update module name


class TestPreSyncEodDumpFile(unittest.TestCase):
    @patch("os.path.join")
    @patch("subprocess.run")
    def test_sync_and_clean_vox_eod_dump_file(self, mock_subprocess_run, mock_path_join):
        mock_path_join.side_effect = lambda *args: "/".join(args)
        mock_subprocess_run.return_value = MagicMock(stdout="Command executed successfully")

        sync_and_clean_vox_eod_dump_file("20250108", "20250109", "/mock/input/dir", 5)

        clean_cmd = "find /mock/input/dir/2025/01/08 -mtime +5 -exec rm -f {} \\;"
        mkdir_cmd = "mkdir -p /mock/input/dir/2025/01/09"
        rsync_cmd = "rsync -trp /mock/input/dir/2025/01/08/ /mock/input/dir/2025/01/09/"

        mock_subprocess_run.assert_has_calls([
            call(clean_cmd, shell=True),
            call(mkdir_cmd, shell=True),
            call(rsync_cmd, shell=True, stdout=MagicMock(), stderr=MagicMock(), text=True)
        ])

    @patch("datetime.datetime")
    @patch("builtins.print")
    def test_printlog(self, mock_print, mock_datetime):
        mock_datetime.now.return_value = datetime(2025, 1, 9, 12, 0, 0)
        printlog("Test log message")
        mock_print.assert_called_once_with("2025-01-09 12:00:00: Test log message")

    @patch("argparse.ArgumentParser.parse_args")
    @patch("PreSyncEodDumpFile.sync_and_clean_vox_eod_dump_file")
    def test_main(self, mock_sync_and_clean, mock_parse_args):
        mock_parse_args.return_value = MagicMock(input="/mock/input/dir", keep_days=5)
        with patch("datetime.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(2025, 1, 9)
            main()
            mock_sync_and_clean.assert_called_once_with("20250108", "20250109", "/mock/input/dir", 5)

    @patch("argparse.ArgumentParser.parse_args")
    def test_main_invalid_arguments(self, mock_parse_args):
        mock_parse_args.return_value = MagicMock(input=None, keep_days=5)
        with self.assertRaises(SystemExit):
            main()


if __name__ == "__main__":
    unittest.main()
