'''
Generate Screenshot of Targeted List Through Screenshot Machine
'''
'''
Initializing Modules
'''
import json
import requests
import time
import hashlib
import os
from constants import Constants, HTTPRequestTypes


'''
ScreenShot Machine Class
'''


class Screenshot(object):
    def __init__(self, api_key, **kwargs):
        self.base_url = 'http://api.screenshotmachine.com'
        self.headers = {'cache-control': "no-cache"}
        self.api_key = api_key
        self.directory = "{}/images".format(os.getcwd())

    # Get a screenshot of a url
    def fetch_screenshot(self, url, q=None, dimension='1024x768',
                         image_format='png',
                         device='desktop', cache_limit='1',
                         delay='600', **kwargs):
        endpoint = self.base_url
        _hash_string = url + self.api_key
        _hash = hashlib.md5(str.encode(_hash_string)).hexdigest()
        _timeline = int(time.time())
        query_params = {
            'key': self.api_key,
            'url': url+q,
            'dimension': dimension,
            'format': image_format,
            'hash': _hash,
            'device': device,
            'cacheLimit': cache_limit,
            'delay': delay
        }
        _path = '{folder_path}/{_time}.{url}.{format}'.format(folder_path=self.directory,
                                                              _time=_timeline,
                                                              url=url,
                                                              format=image_format)
        response = self.request_handler(method='GET',
                                        endpoint=endpoint,
                                        query_params=query_params,
                                        _path=_path)
        return response

    def request_handler(self, method, endpoint,
                        status_404=False,
                        query_params=None,
                        payload_json=None,
                        payload_data=None,
                        custom_output=None,
                        response_type=None,
                        _path=None,
                        **kwargs
                        ) -> dict:
        """
        description: function handle request and response
        :param method: http method
        :param endpoint : url suffix
        :param params : params
        :param payload: payload
        :param kwargs:
        :return:
        Args:
            method (TYPE): Description
            endpoint (TYPE): Description
            params (None, optional): Description
            payload (None, optional): Description
            **kwargs: Description
        Returns:
            TYPE: Description
        """
        # Defining the variables used specifically for request handler
        response_data = {}
        response = ""
        try:
            url = "{0}".format(self.base_url)
            if method in [method_val.value for method_val
                          in HTTPRequestTypes]:
                response = requests.request(method, url,
                                            params=query_params,
                                            json=payload_json,
                                            data=payload_data,
                                            headers=self.headers)
            #If Wrong Method is being provided.
            else:
                return {Constants.ACTION_RESULT: ErrorMsg.WRONG_MET,
                        Constants.ACTION_STATUS: Constants.ERROR}
            # Status code of the response
            response_data[Constants.STATUS_CODE] = response.status_code
            # If response is successful.
            if response.ok:
                with open(_path, 'wb') as fd:
                    fd.write(response.content)
                    _response_value = _path
                    response_data[Constants.RESPONSE] = _response_value
                    response_data['URL'] = response.url
                    execution_status = Constants.SUCCESS

            # If 404 condition is valid situation.
            elif response.status_code == 404 and status_404:
                response_data[Constants.RESPONSE] = response.json()
                execution_status = Constants.SUCCESS
            # If there is Error
            else:
                response_data[Constants.RESPONSE] = response.text
                execution_status = Constants.ERROR

    # If keyerror is there in the dictionary.
        except KeyError as e:
            exception_error = str(e)
            response_data = {Constants.RESPONSE: exception_error}
            execution_status = Constants.ERROR
        # In Case  when an invalid attribute reference is made,
        #or when an attribute assignment fails.
        except AttributeError as e:
            exception_error = str(e)
            response_data = {Constants.RESPONSE: exception_error}
            execution_status = Constants.ERROR
        #when defined a variable or a function name that is not
        #valid and present.
        except NameError as e:
            exception_error = str(e)
            response_data = {Constants.RESPONSE: exception_error}
            execution_status = Constants.ERROR
        # If JSON is not found.
        except ValueError as e:
            response_data = {Constants.RESPONSE: 'JSON RESPONSE NOT FOUND'}
            execution_status = Constants.ERROR
        # Catching General and rest of the Exception
        except Exception as e:
            exception_error = str(e)
            response_data = {Constants.RESPONSE: exception_error}
            execution_status = Constants.ERROR
        # Returning the response.
        return {Constants.ACTION_RESULT: response_data,
                Constants.ACTION_STATUS: execution_status}
