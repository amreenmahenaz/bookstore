@patch("getPlanetBaac.ms.soap.client.TCPConnection")
@patch("getPlanetBaac.ms.soap.envelope.Envelope")
@patch("getPlanetBaac.etree.Element")
def test_make_api_call_success(self, mock_etree_element, mock_envelope, mock_tcp_connection):
    # Mock the SOAP envelope and element
    mock_request = MagicMock()
    mock_response = MagicMock()
    mock_response.body = [{"effective_date": "2025-01-01", "baac_company": "TestCompany"}]

    mock_envelope.return_value = mock_request
    mock_tcp_connection.return_value.sendrequest.return_value = mock_response

    # Simulate the etree.Element behavior
    mock_etree_element.return_value.tag = "effective_date"
    mock_etree_element.return_value.text = "2025-01-01"

    make_api_call("20250101", "output.csv")

    # Assertions
    mock_tcp_connection.return_value.sendrequest.assert_called_once_with(mock_request)
    mock_etree_element.assert_called_once_with("effective_date", text="20250101")
