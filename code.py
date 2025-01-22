
    @patch("getPlanetBaac.ms.soap.client.TCPConnection")
    def test_make_api_call_success(self, mock_tcp_connection):
        # Create a real `etree.Element` for testing
        query_date = "2025-01-01"
        output_filename = "output.csv"
        request_body = etree.Element("request")
        etree.SubElement(request_body, "effective_date").text = query_date

        # Mock the SOAP connection and its response
        mock_response = MagicMock()
        mock_response.body = [{"effective_date": "2025-01-01", "baac_company": "TestCompany"}]
        mock_tcp_connection.return_value.sendrequest.return_value = mock_response

        # Call the function
        make_api_call(query_date, output_filename)

        # Assertions
        mock_tcp_connection.return_value.sendrequest.assert_called_once()
        self.assertEqual(mock_response.body[0]["effective_date"], "2025-01-01")

if __name__ == "__main__":
    unittest.main()
