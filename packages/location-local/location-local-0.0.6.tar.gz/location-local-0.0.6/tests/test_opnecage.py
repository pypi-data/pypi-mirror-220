import os
from unittest.mock import Mock
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from CirclesGetCountryName.opencage_get_country_name import Country
from dotenv import load_dotenv
import pytest

# Load environment variables from .env file
load_dotenv()

# Get the Local_Logger instance


# Define the tests for the Country class
class TestCountry:
    @pytest.mark.test
    def test_get_country_name(self):

        mock_results = [
            {
                'components': {
                    'country': 'United States',
                    'country_code': 'US'
                }
            }
        ]
        geocoder_mock = Mock(return_value=mock_results)
        Country.geocoder = geocoder_mock
        result = Country.get_country_name("New York")
        assert result == "United States"
    @pytest.mark.test
    def test_get_country_name_no_results(self):

        geocoder_mock = Mock(return_value=[])
        Country.geocoder = geocoder_mock

        result = Country.get_country_name("Invalid Location")
        assert result is None


if __name__ == "__main__":
    pytest.main()

