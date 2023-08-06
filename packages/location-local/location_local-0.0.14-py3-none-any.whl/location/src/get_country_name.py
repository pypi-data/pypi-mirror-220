import os
from opencage.geocoder import OpenCageGeocode
from logger_local_python_package.localLogger import logger_local
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENCAGE_KEY")
class country:
    def __init__(self):
        pass
    
    @staticmethod
    def get_country_name(location):
        # Create a geocoder instance
        object1={
            'component_id':113,
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
            country = components.get('country', '')
            if not country:
                # If country is not found, check for country_code as an alternative
                country = components.get('country_code', '')
        else:
            country = None
            logger_local.error("country didnt found for %s."%location)
        object2={
                'component_id':113 ,
                'country':country
            }
        logger_local.end(object=object2)
        return country


if __name__ == "__main__":
    pass
