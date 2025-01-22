import unittest
from unittest.mock import patch, MagicMock, mock_open
from datetime import datetime, timedelta
import csv
from lxml import etree

# Import functions from your getPlanetBaac module
from getPlanetBaac import (
    parse_arguments,
    handle_date_arguments,
    generate_output_filename,
    make_api_call,
    save_response_to_csv,
    main,
)

class TestGetPlanetBaac(unittest.TestCase):
    def test_parse_arguments(self):
        """Test parsing command-line arguments."""
        with patch('argparse.ArgumentParser.parse_args') as mock_args:
            mock_args.return_value = MagicMock(date='2025-01-01', output='output.csv')
            args = parse_arguments()
            self.assertEqual(args.date, '2025-01-01')
            self.assertEqual(args.output, 'output.csv')

    def test_handle_date_arguments_with_date(self):
        """Test handling date arguments when a date is provided."""
        date_str = '2025-01-01'
        query_date, format_date = handle_date_arguments(date_str)
        self.assertEqual(query_date, datetime.strptime(date_str, '%Y-%m-%d'))
        self.assertEqual(format_date, '20250101')

    def test_handle_date_arguments_without_date(self):
        """Test handling date arguments when no date is provided."""
        query_date, format_date = handle_date_arguments(None)
        expected_date = datetime.now() - timedelta(days=2)
        self.assertEqual(query_date.date(), expected_date.date())
        self.assertEqual(format_date, expected_date.strftime('%Y%m%d'))

    def test_generate_output_filename(self):
        """Test generating an output filename."""
        base_name = "output"
        date_str = "20250101"
        filename = generate_output_filename(base_name, date_str)
        self.assertEqual(filename, "output_20250101")

    @patch("getPlanetBaac.ms.soap.client.TCPConnection")
    @patch("getPlanetBaac.ms.soap.envelope.Envelope")
    def test_make_api_call_success(self, mock_envelope, mock_tcp_connection):
        """Test making the API call successfully."""
        mock_request = MagicMock()
        mock_response = MagicMock()
        mock_response.body = [{"effective_date": "2025-01-01"}]

        mock_envelope.return_value = mock_request
        mock_tcp_connection.return_value = MagicMock()
        mock_tcp_connection.return_value.sendrequest.return_value = mock_response

        query_date = "20250101"
        output_filename = "output.csv"

        with patch("getPlanetBaac.save_response_to_csv") as mock_save_csv:
            make_api_call(query_date, output_filename)
            mock_tcp_connection.assert_called_once()
            mock_envelope.assert_called_once()
            mock_save_csv.assert_called_once_with(mock_response.body, output_filename)

    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.writer")
    def test_save_response_to_csv(self, mock_csv_writer, mock_open_file):
        """Test saving response to a CSV file."""
        data = [
            {"effective_date": "2025-01-01", "baac_company": "TestCompany"}
        ]
        filename = "output.csv"
        save_response_to_csv(data, filename)

        mock_open_file.assert_called_once_with(filename, 'w', newline='', encoding='utf-8')
        mock_csv_writer.assert_called_once()
        mock_csv_writer.return_value.writerow.assert_any_call(
            ['effective_date', 'baac_company']
        )
        mock_csv_writer.return_value.writerow.assert_any_call(
            ['2025-01-01', 'TestCompany']
        )

    @patch("getPlanetBaac.make_api_call")
    @patch("getPlanetBaac.handle_date_arguments")
    @patch("getPlanetBaac.parse_arguments")
    def test_main(self, mock_parse_arguments, mock_handle_date_arguments, mock_make_api_call):
        """Test the main function."""
        mock_args = MagicMock(date='2025-01-01', output='output.csv')
        mock_parse_arguments.return_value = mock_args
        mock_handle_date_arguments.return_value = (datetime(2025, 1, 1), "20250101")

        main()

        mock_parse_arguments.assert_called_once()
        mock_handle_date_arguments.assert_called_once_with('2025-01-01')
        mock_make_api_call.assert_called_once_with("20250101", "output.csv")


if __name__ == "__main__":
    unittest.main()
