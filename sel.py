import unittest
from unittest.mock import patch, MagicMock
import datetime
import subprocess
import preSyncEodDumpFile as script  # Replace with the script filename

class TestPreSyncEodDumpFile(unittest.TestCase):
    
    @patch('datetime.datetime')
    def test_get_previous_working_date(self, mock_datetime):
        # Mock datetime to return a Wednesday
        mock_datetime.now.return_value = datetime.datetime(2024, 12, 18)
        expected_date = '20241217'  # Previous working day is Tuesday (2024-12-17)
        result = script.get_previous_working_date()
        self.assertEqual(result, expected_date)

    @patch('subprocess.call')
    @patch('os.path.join')
    def test_sync_and_clean_vox_eod_dump_file(self, mock_path_join, mock_subprocess_call):
        # Setup
        mock_path_join.side_effect = lambda *args: '/'.join(args)
        mock_subprocess_call.return_value = 0
        
        # Input
        from_date = '20241216'
        to_date = '20241218'
        input_dir = '/dummy/dir'
        keep_days = 5
        
        # Call the function
        script.sync_and_clean_vox_eod_dump_file(from_date, to_date, input_dir, keep_days)

        # Verifications
        clean_cmd = f'{script.FIND} /dummy/dir -print -mtime +5 -exec /bin/rm -f {{}} ;'
        mkdir_cmd = f'/bin/mkdir -p /dummy/dir/2024/12/18'
        rsync_cmd = f'/usr/bin/rsync -trp /dummy/dir /dummy/dir/2024/12/18'
        
        # Assert subprocess was called with the expected commands
        mock_subprocess_call.assert_any_call(clean_cmd, shell=True)
        mock_subprocess_call.assert_any_call(mkdir_cmd, shell=True)
        mock_subprocess_call.assert_any_call(rsync_cmd, shell=True)
        self.assertEqual(mock_subprocess_call.call_count, 3)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('preSyncEodDumpFile.get_previous_working_date')
    @patch('preSyncEodDumpFile.sync_and_clean_vox_eod_dump_file')
    def test_main_function(self, mock_sync, mock_get_prev_date, mock_parse_args):
        # Mock CLI arguments
        mock_parse_args.return_value = MagicMock(i='/dummy/input', k=3)
        mock_get_prev_date.return_value = '20241217'
        
        # Call main
        script.main()
        
        # Verify calls
        mock_get_prev_date.assert_called_once()
        mock_sync.assert_called_once_with('20241217', unittest.mock.ANY, '/dummy/input', 3)

if __name__ == '__main__':
    unittest.main()
