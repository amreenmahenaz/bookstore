import unittest
from unittest.mock import patch, MagicMock, mock_open
import ms.soap
import getPlanetBaac


class TestGetPlanetBaac(unittest.TestCase):

    @patch('getPlanetBaac.ms.soap.client.TCPConnection')
    def test_make_api_call_success(self, mock_tcp_connection):
        # Mock connection and response
        mock_connection = MagicMock()
        mock_response = MagicMock()
        mock_response.body = "<response>success</response>"
        mock_connection.sendrequest.return_value = mock_response

        mock_tcp_connection.return_value = mock_connection

        # Call the method
        getPlanetBaac.make_api_call('2023-12-01', 'output.csv')

        # Assertions
        mock_tcp_connection.assert_called_once_with(
            getPlanetBaac.API_BASE_URL, 
            getPlanetBaac.PORT, 
            getPlanetBaac.auth_provider, 
            timeout=30
        )
        mock_connection.sendrequest.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('csv.writer')
    def test_save_response_to_csv(self, mock_csv_writer, mock_open_file):
        # Mock data
        data = [
            {
                'effective_date': '2023-12-01',
                'cons_div': 'division',
                'taps_account': 'account'
            }
        ]
        filename = 'output.csv'

        # Call the method
        getPlanetBaac.save_response_to_csv(data, filename)

        # Assertions
        mock_open_file.assert_called_once_with(filename, 'w', newline='', encoding='utf-8')
        mock_csv_writer.assert_called_once()
        mock_csv_writer().writerow.assert_called()

    @patch('getPlanetBaac.datetime')
    def test_handle_date_arguments_with_date(self, mock_datetime):
        # Mock date
        mock_datetime.strptime.return_value = mock_datetime(2023, 12, 1)
        mock_datetime.now.return_value = mock_datetime(2023, 12, 3)

        date_str = '2023-12-01'
        query_date, format_date = getPlanetBaac.handle_date_arguments(date_str)

        # Assertions
        self.assertEqual(query_date, '2023-12-01')
        self.assertEqual(format_date, '20231201')

    @patch('getPlanetBaac.datetime')
    def test_handle_date_arguments_without_date(self, mock_datetime):
        # Mock date
        mock_datetime.now.return_value = mock_datetime(2023, 12, 3)

        query_date, format_date = getPlanetBaac.handle_date_arguments(None)

        # Assertions
        self.assertEqual(query_date, '2023-12-01')
        self.assertEqual(format_date, '20231201')

    @patch('getPlanetBaac.make_api_call')
    @patch('getPlanetBaac.generate_output_filename')
    @patch('getPlanetBaac.handle_date_arguments')
    @patch('getPlanetBaac.parse_arguments')
    def test_main(self, mock_parse_args, mock_handle_date_args, mock_generate_output_filename, mock_make_api_call):
        # Mock arguments
        mock_args = MagicMock()
        mock_args.date = '2023-12-01'
        mock_args.output = 'output.csv'
        mock_parse_args.return_value = mock_args
        mock_handle_date_args.return_value = ('2023-12-01', '20231201')
        mock_generate_output_filename.return_value = 'output.csv'

        # Call the main function
        getPlanetBaac.main()

        # Assertions
        mock_parse_args.assert_called_once()
        mock_handle_date_args.assert_called_once_with('2023-12-01')
        mock_generate_output_filename.assert_called_once_with('output.csv', '20231201')
        mock_make_api_call.assert_called_once_with('2023-12-01', 'output.csv')


if __name__ == '__main__':
    unittest.main()
