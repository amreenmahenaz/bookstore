import unittest
from unittest.mock import patch, call, Mock
from PreSyncEodDumpFile import main, sync_and_clean_vox_eod_dump_file, printlog
from datetime import datetime

class TestPreSyncEodDumpFile(unittest.TestCase):

    @patch('PreSyncEodDumpFile.datetime')
    @patch('builtins.print')
    def test_printlog(self, mock_print, mock_datetime):
        """Test the printlog function."""
        mock_datetime.now.return_value = datetime(2025, 1, 9, 12, 0, 0)
        printlog("Test log message")
        mock_print.assert_called_with("20250109-12:00:00 - Test log message")

    def test_main_invalid_arguments(self):
        """Test main with missing arguments."""
        with self.assertRaises(SystemExit):
            with patch('sys.argv', ['PreSyncEodDumpFile.py']):
                main()

    @patch('PreSyncEodDumpFile.call')
    def test_sync_and_clean_vox_eod_dump_file(self, mock_call):
        """Test sync_and_clean_vox_eod_dump_file logic."""
        sync_and_clean_vox_eod_dump_file(
            "20250108", "20250109", "/mock/input/dir", 5
        )

        # Define the expected shell commands that are called
        clean_cmd = (
            "find /mock/input/dir/2025/01/08 -print -mtime +5 "
            "-bexec /bin/rm -f {} \\;"
        )
        mkdir_cmd = "/bin/mkdir -p /mock/input/dir/2025/01/09"
        rsync_cmd = "/usr/bin/rsync -trp /mock/input/dir/2025/01/08 /mock/input/dir/2025/01/09"

        # Check if the mock_call is invoked correctly
        mock_call.assert_has_calls(
            [call(clean_cmd, shell=True), call(mkdir_cmd, shell=True), call(rsync_cmd, shell=True)]
        )

    @patch('sys.argv', [
        'PreSyncEodDumpFile.py',
        '-i', '/mock/input/dir',
        '-k', '5'
    ])
    @patch('PreSyncEodDumpFile.sync_and_clean_vox_eod_dump_file')
    @patch('PreSyncEodDumpFile.datetime')
    def test_main(self, mock_datetime, mock_sync, mock_args):
        """Test main with valid arguments."""
        mock_datetime.now.return_value = datetime(2025, 1, 9)
        mock_sync.return_value = None

        main()

        mock_sync.assert_called_once_with(
            "20250108", "20250109", "/mock/input/dir", 5
        )

if __name__ == "__main__":
    unittest.main()
