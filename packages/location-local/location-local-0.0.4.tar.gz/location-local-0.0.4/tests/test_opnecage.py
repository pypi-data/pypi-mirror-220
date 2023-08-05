import os
from unittest.mock import Mock
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from CirclesGetCountryName.opencage_get_country_name import Country
from LoggerLocalPythonPackage import LocalLogger
from dotenv import load_dotenv
import pytest

# Load environment variables from .env file
load_dotenv()

# Get the Local_Logger instance
Local_Logger = LocalLogger._Local_Logger

# Define the tests for the Country class
class TestCountry:
    @pytest.mark.test
    def test_get_country_name(self):
        country = Country()

        mock_results = [
            {
                'components': {
                    'country': 'United States',
                    'country_code': 'US'
                }
            }
        ]
        geocoder_mock = Mock(return_value=mock_results)
        country.geocoder = geocoder_mock
        result = country.get_country_name("New York")
        assert result == "United States"
    @pytest.mark.test
    def test_get_country_name_no_results(self):
        country = Country()

        geocoder_mock = Mock(return_value=[])
        country.geocoder = geocoder_mock

        result = country.get_country_name("Invalid Location")
        assert result is None


if __name__ == "__main__":
    pytest.main()

TestCountry1=TestCountry()
TestCountry1.test_get_country_name()