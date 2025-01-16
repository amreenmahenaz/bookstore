import unittest
from unittest.mock import patch, MagicMock, mock_open
from MQsubmit import connect_to_mq, disconnect_from_mq, process_file, main

class TestMQSubmit(unittest.TestCase):
    @patch("pymqi.connect")
    @patch("pymqi.Queue")
    def test_connect_to_mq_success(self, mock_queue, mock_connect):
        mock_qmgr = MagicMock()
        mock_queue_instance = MagicMock()
        mock_connect.return_value = mock_qmgr
        mock_queue.return_value = mock_queue_instance

        qmgr, queue = connect_to_mq("QM1", "QUEUE1")
        mock_connect.assert_called_once_with("QM1")
        mock_queue.assert_called_once_with(mock_qmgr, "QUEUE1")
        self.assertEqual(qmgr, mock_qmgr)
        self.assertEqual(queue, mock_queue_instance)

    @patch("pymqi.connect", side_effect=Exception("Connection failed"))
    def test_connect_to_mq_failure(self, mock_connect):
        with self.assertRaises(SystemExit):
            connect_to_mq("QM1", "QUEUE1")

    @patch("pymqi.Queue.close")
    @patch("pymqi.QueueManager.disconnect")
    def test_disconnect_from_mq_success(self, mock_disconnect, mock_close):
        mock_queue = MagicMock()
        mock_qmgr = MagicMock()

        disconnect_from_mq(mock_queue, mock_qmgr)

        mock_close.assert_called_once()
        mock_disconnect.assert_called_once()

    @patch("pymqi.Queue.close", side_effect=Exception("Close failed"))
    def test_disconnect_from_mq_failure(self, mock_close):
        mock_queue = MagicMock()
        with self.assertRaises(Exception):
            disconnect_from_mq(mock_queue, None)

    @patch("builtins.open", mock_open(read_data="Test message"))
    @patch("pymqi.Queue.put")
    @patch("pymqi.PMO")
    def test_process_file_success(self, mock_pmo, mock_put, mock_open_file):
        mock_queue = MagicMock()
        mock_qmgr = MagicMock()

        process_file("test_file.txt", mock_queue, mock_qmgr)

        mock_open_file.assert_called_once_with("test_file.txt", "r")
        mock_put.assert_called_once()

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_process_file_file_not_found(self, mock_open_file):
        mock_queue = MagicMock()
        mock_qmgr = MagicMock()

        with self.assertRaises(SystemExit):
            process_file("nonexistent.txt", mock_queue, mock_qmgr)

        mock_open_file.assert_called_once_with("nonexistent.txt", "r")

    @patch("MQsubmit.connect_to_mq")
    @patch("MQsubmit.disconnect_from_mq")
    @patch("MQsubmit.process_file")
    def test_main_success(self, mock_process_file, mock_disconnect, mock_connect):
        mock_qmgr = MagicMock()
        mock_queue = MagicMock()
        mock_connect.return_value = (mock_qmgr, mock_queue)

        files = ["file1.txt", "file2.txt"]

        with patch("sys.argv", ["script.py", "QM1", "QUEUE1"] + files):
            main("QM1", "QUEUE1", files)

        mock_connect.assert_called_once_with("QM1", "QUEUE1")
        mock_process_file.assert_any_call("file1.txt", mock_queue, mock_qmgr)
        mock_process_file.assert_any_call("file2.txt", mock_queue, mock_qmgr)
        mock_disconnect.assert_called_once_with(mock_queue, mock_qmgr)


if __name__ == "__main__":
    unittest.main()
