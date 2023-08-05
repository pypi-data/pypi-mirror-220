import os
from opencage.geocoder import OpenCageGeocode
from LoggerLocalPythonPackage import LocalLogger
from dotenv import load_dotenv
load_dotenv()
Local_Logger=LocalLogger._Local_Logger
class Country:
    def __init__(self):
        pass

    def get_country_name(self, location):
        # Create a geocoder instance
        Local_Logger.start("start get_country_name(${location}) ")
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
            Local_Logger.end("end get_country_name return value= "+str(country))
            return country

        else:
            Local_Logger.end("end get_country_name return value= None")
            return None


if __name__ == "__main__":
    pass
