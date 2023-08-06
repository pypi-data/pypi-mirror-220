import os
from opencage.geocoder import OpenCageGeocode
from logger_local_python_package.localLogger import logger_local
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENCAGE_KEY")
component_id=113 
class Country:
    def __init__(self):
        pass
    
    @staticmethod
    def get_country_name(location):
        # Create a geocoder instance
        object1={
            'component_id':component_id,
            'location':location,
        }
        logger_local.start(object=object1)
        

        # Define the city or state
        geocoder = OpenCageGeocode(api_key)

        # Use geocoding to get the location details
        results = geocoder.geocode(location)

        if results and len(results) > 0:
            first_result = results[0]
            components = first_result['components']

            # Extract the country from components
            country_name = components.get('country', '')
            if not country_name:
                # If country is not found, check for country_code as an alternative
                country_name = components.get('country_code', '')
        else:
            country_name = None
            logger_local.error("country didnt found for %s."%location)
        object2={
                'component_id':component_id ,
                'country_name':country_name
            }
        logger_local.end(object=object2)
        return country_name


if __name__ == "__main__":
    pass
