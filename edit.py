import unittest
from unittest.mock import patch, MagicMock, mock_open
from MQsubmit import connect_to_mq, disconnect_from_mq, process_file, main


class TestMQSubmit(unittest.TestCase):
    @patch('pymqi.connect')
    @patch('pymqi.Queue')
    def test_connect_to_mq_success(self, mock_queue, mock_connect):
        mock_connect.return_value = MagicMock()
        mock_queue.return_value = MagicMock()
        
        qmgr, queue = connect_to_mq('QM1', 'QUEUE1')
        
        mock_connect.assert_called_once_with('QM1')
        mock_queue.assert_called_once_with(qmgr, 'QUEUE1')

    @patch('pymqi.connect', side_effect=Exception('Connection failed'))
    def test_connect_to_mq_failure(self, mock_connect):
        with self.assertRaises(Exception):
            connect_to_mq('QM1', 'QUEUE1')

    @patch('pymqi.Queue.close')
    def test_disconnect_from_mq_success(self, mock_close):
        queue_mock = MagicMock()
        disconnect_from_mq(queue_mock, None)
        mock_close.assert_called_once()

    @patch('pymqi.Queue.close', side_effect=Exception('Close failed'))
    def test_disconnect_from_mq_failure(self, mock_close):
        with self.assertRaises(Exception):
            disconnect_from_mq(MagicMock(), None)

    @patch('builtins.open', new_callable=mock_open, read_data='test data')
    @patch('pymqi.Queue.put')
    def test_process_file_success(self, mock_put, mock_open):
        queue_mock = MagicMock()
        process_file('test_file.txt', queue_mock, None)
        
        mock_open.assert_called_once_with('test_file.txt', 'r')
        mock_put.assert_called_once()

    @patch('pymqi.Queue.put', side_effect=Exception('Put failed'))
    def test_process_file_failure(self, mock_put):
        with self.assertRaises(Exception):
            process_file('test_file.txt', MagicMock(), None)

    @patch('MQsubmit.connect_to_mq')
    @patch('MQsubmit.disconnect_from_mq')
    @patch('MQsubmit.process_file')
    def test_main_success(self, mock_process_file, mock_disconnect, mock_connect):
        mock_qmgr = MagicMock()
        mock_queue = MagicMock()
        mock_connect.return_value = (mock_qmgr, mock_queue)
        
        mock_process_file.return_value = None
        mock_disconnect.return_value = None

        main('QM1', 'QUEUE1', ['file1', 'file2'])
        
        mock_connect.assert_called_once_with('QM1', 'QUEUE1')
        mock_process_file.assert_any_call('file1', mock_queue, mock_qmgr)
        mock_process_file.assert_any_call('file2', mock_queue, mock_qmgr)
        mock_disconnect.assert_called_once_with(mock_queue, mock_qmgr)


if __name__ == '__main__':
    unittest.main()
