import os
from opencage.geocoder import OpenCageGeocode
from LoggerLocalPythonPackage.LocalLogger import _Local_Logger as local_logger
from dotenv import load_dotenv
load_dotenv()

class Country:
    def __init__(self):
        pass
    
    @staticmethod
    def get_country_name(location):
        # Create a geocoder instance
        local_logger.start("start get_country_name(${location}) ")
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
            local_logger.end("end get_country_name return value= "+str(country))
            return country

        else:
            local_logger.error("country didnt found for %s."%location)
            local_logger.end("end get_country_name return value= None")
            return None


if __name__ == "__main__":
    pass
