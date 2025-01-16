import unittest
from unittest.mock import patch, MagicMock
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
    @patch("pymqi.connect")
    def test_disconnect_from_mq_success(self, mock_connect, mock_close):
        mock_qmgr = MagicMock()
        mock_queue = MagicMock()
        disconnect_from_mq(mock_queue, mock_qmgr)
        mock_queue.close.assert_called_once()
        mock_qmgr.disconnect.assert_called_once()

    @patch("pymqi.Queue.close", side_effect=Exception("Close failed"))
    def test_disconnect_from_mq_failure(self, mock_close):
        mock_queue = MagicMock()
        with self.assertRaises(Exception):
            disconnect_from_mq(mock_queue, None)

    @patch("builtins.open", create=True)
    @patch("pymqi.MQMessage")
    @patch("pymqi.PMO")
    @patch("pymqi.Queue.put")
    def test_process_file_success(self, mock_put, mock_pmo, mock_msg, mock_open):
        mock_file_handle = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file_handle
        mock_file_handle.read.return_value = "test_message"
        mock_queue = MagicMock()
        process_file("test_file.txt", mock_queue, MagicMock())
        mock_open.assert_called_once_with("test_file.txt", "r")
        mock_msg.assert_called_once()
        mock_pmo.assert_called_once()
        mock_put.assert_called_once()

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_process_file_file_not_found(self, mock_open):
        mock_queue = MagicMock()
        with self.assertRaises(SystemExit):
            process_file("non_existent_file.txt", mock_queue, MagicMock())

    @patch("MQsubmit.connect_to_mq")
    @patch("MQsubmit.disconnect_from_mq")
    @patch("MQsubmit.process_file")
    def test_main_success(self, mock_process_file, mock_disconnect, mock_connect):
        mock_qmgr = MagicMock()
        mock_queue = MagicMock()
        mock_connect.return_value = (mock_qmgr, mock_queue)

        main("QM1", "QUEUE1", ["file1.txt", "file2.txt"])
        mock_connect.assert_called_once_with("QM1", "QUEUE1")
        mock_process_file.assert_any_call("file1.txt", mock_queue, mock_qmgr)
        mock_process_file.assert_any_call("file2.txt", mock_queue, mock_qmgr)
        mock_disconnect.assert_called_once_with(mock_queue, mock_qmgr)


if __name__ == "__main__":
    unittest.main()
