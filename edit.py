class TestPreSyncEodDumpFile(unittest.TestCase):
    @patch("subprocess.call")
    @patch("os.makedirs")
    @patch("os.path.join")
    def test_sync_and_clean_vox_eod_dump_file(self, mock_join, mock_makedirs, mock_call):
        # Arrange: Set up mock return values
        mock_join.side_effect = lambda *args: "/".join(args)  # Mock os.path.join behavior
        mock_makedirs.return_value = None  # Mock os.makedirs to do nothing
        mock_call.return_value = 0  # Mock subprocess.call to return success

        from_date = "20250108"
        to_date = "20250109"
        input_file_dir = "/mock/input/dir"
        keep_days = 5

        # Act: Call the function
        sync_and_clean_vox_eod_dump_file(from_date, to_date, input_file_dir, keep_days)

        # Assert: Verify mocks were called with correct arguments
        from_dir = f"{input_file_dir}/2025/01/08"
        to_dir = f"{input_file_dir}/2025/01/09"
        clean_cmd = f"find {from_dir} -print -mtime +{keep_days} -exec /bin/rm -f {{}} \\;"
        mkdir_cmd = f"/bin/mkdir -p {to_dir}"
        rsync_cmd = f"/usr/bin/rsync -trp {from_dir} {to_dir}"

        mock_call.assert_any_call(clean_cmd, shell=True)
        mock_call.assert_any_call(mkdir_cmd, shell=True)
        mock_call.assert_any_call(rsync_cmd, shell=True)

    @patch("preSyncEodDumpFile.printlog")
    @patch("preSyncEodDumpFile.sync_and_clean_vox_eod_dump_file")
    @patch("argparse.ArgumentParser.parse_args")
    def test_main(self, mock_parse_args, mock_sync_and_clean, mock_printlog):
        # Arrange: Mock argument parsing
        mock_parse_args.return_value = MagicMock(input="/mock/input/dir", keep_days=5)
        mock_printlog.return_value = None  # Mock printlog to do nothing
        mock_sync_and_clean.return_value = None  # Mock sync_and_clean_vox_eod_dump_file

        # Act: Call main()
        main()

        # Assert: Verify functions are called with expected values
        mock_sync_and_clean.assert_called_with(
            "20250108",  # Mock previous working date
            "20250109",  # Mock today's date
            "/mock/input/dir",
            5
        )
        mock_printlog.assert_called()

if __name__ == "__main__":
    unittest.main()
