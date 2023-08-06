import os
from opencage.geocoder import OpenCageGeocode
from logger_local_python_package.localLogger import _Local_Logger as local_logger
from dotenv import load_dotenv
load_dotenv()

class Country:
    def __init__(self):
        pass
    
    @staticmethod
    def get_country_name(location):
        # Create a geocoder instance
        object1={
            'function': 'get_country_name',
            'location':location
        }
        local_logger.start(object=object1)
        api_key = os.getenv("OPENCAGE_KEY")

        # Define the city or state
        geocoder = OpenCageGeocode(api_key)

        # Use geocoding to get the location details
        results = geocoder.geocode(location)

        if results and len(results) > 0:
            first_result = results[0]
            components = first_result['components']

            # Extract the country from components
            country = components.get('country', '')
            if not country:
                # If country is not found, check for country_code as an alternative
                country = components.get('country_code', '')
            object2={
                'function': 'get_country_name',
                'return':country
            }
            local_logger.end(object=object2)
            return country

        else:
            local_logger.error("country didnt found for %s."%location)
            object3={
                'function': 'get_country_name',
                'return':'None'
            }
            local_logger.end(object=object3)
            return None


if __name__ == "__main__":
    pass
