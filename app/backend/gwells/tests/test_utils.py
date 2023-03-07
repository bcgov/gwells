"""
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from unittest.mock import patch, Mock
from requests.exceptions import HTTPError

from django.test import TestCase
from django.contrib.gis.geos import GEOSGeometry, Point

from gwells.utils import geocode_bc_location

class UtilsTestCase(TestCase):

    @patch('gwells.utils.requests.get')
    def test_geocode_bc_location_success(self, mock_requests_get):
        """
        Confirm that 'geocode_bc_location(...)' returns a geometry object
        with valid latitude and longitude
        """
        
        # Mock a response from the BC Physical Address Geocoder API
        # so this test does not need to rely on the availability of 
        # a remote API.
        mock_lon = -122
        mock_lat = 49
        mock_geocode_api_response = {  
            "features": [
              {
                "type": "Feature",
                "geometry": {
                  "type": "Point",
                  "crs": {
                    "type": "EPSG",
                    "properties": {
                      "code": 4326
                    }
                  },
                  "coordinates": [mock_lon, mock_lat]
                }
              }
            ]
        }
        mock_requests_get.return_value = \
            Mock(status_code=200, json=lambda : mock_geocode_api_response)

        response = geocode_bc_location({"addressString": "101 main st.", "localityName": "vancouver"})
        
        # Confirm that a mock API call was used instead of a real API call
        mock_requests_get.assert_called_once()
        
        # Confirm that the 'geocode_bc_location(...)' function returned same the 
        # geographic coords that it received from a call to the
        # BC Physical Address Geocoder API. The returned object should be an
        # instance of django.contrib.gis.geos.Point.
        self.assertTrue(response, Point)
        self.assertEqual(response.coords[0], mock_lon)
        self.assertEqual(response.coords[1], mock_lat)
        

    @patch('gwells.utils.requests.get')
    def test_geocode_bc_location_api_unavailable(self, mock_requests_get):
        """
        Confirm that 'geocode_bc_location(...)' raises an HTTPError when 
        the underlying BC Physical Address Geocoder API returns an HTTP 
        error code
        """
        mock_requests_get.side_effect = HTTPError(Mock(status=500), 'not found')

        with self.assertRaises(HTTPError):        
            geocode_bc_location({"addressString": "101 main st.", "localityName": "vancouver"})        
                
        # Confirm that a mock API call was used instead of a real API call
        mock_requests_get.assert_called_once()
        
    @patch('gwells.utils.requests.get')
    def test_geocode_bc_location_api_invalid_response(self, mock_requests_get):
        """
        Confirm that 'geocode_bc_location(...)' raises an HTTPError if 
        the underlying BC Physical Address Geocoder API returns an HTTP 
        success message, but with invalid json in the body
        """
        mock_geocode_api_response = "invalid json response"
        mock_requests_get.return_value = \
            Mock(status_code=200, json=lambda : mock_geocode_api_response)

        with self.assertRaises(ValueError) as context_manager:        
            geocode_bc_location({"addressString": "101 main st.", "localityName": "vancouver"})            
                
        print(context_manager.exception)

        # Confirm that a mock API call was used instead of a real API call
        mock_requests_get.assert_called_once()     


        