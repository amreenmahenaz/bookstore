from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from atlassian import Confluence
import requests

# Create a session with retries
session = requests.Session()
retry = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)

# Initialize Confluence API client using API token
confluence = Confluence(
    url='https://your-confluence-instance.atlassian.net',
    username='your_username',  # Use your Atlassian account email here
    password='your_api_token',  # Use your API token here
    session=session,
    verify_ssl=False  # Optionally disable SSL if you encounter SSL errors
)
