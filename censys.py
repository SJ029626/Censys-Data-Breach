'''
:Data Breach Capture Through Censys
:Project: By Sanyam Jain
:EmailID: sanyam.jain2602@gmail.com
'''

'''
Initializing Modules
'''
import json
import requests
from constants import Constants, HTTPRequestTypes


'''
Censys Class
'''


class Censys(object):
    def __init__(self, api_id, secret, **kwargs):
        self.base_url = "https://search.censys.io/api/v2"
        self.auth_cred = (api_id, secret)

    def query(self, q, page=100, cursor=None):
        endpoint = "hosts/search"
        params = dict(q=q, per_page=page,
                      cursor=cursor)
        response = self.request_handler("GET", endpoint,
                                        query_params=params)
        return response

    def request_handler(self, method, endpoint,
                        status_404=False,
                        query_params=None,
                        payload_json=None,
                        payload_data=None,
                        custom_output=None,
                        response_type=None,
                        **kwargs
                        ):
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
            url = "{0}/{1}".format(self.base_url, endpoint)
            headers = {"Accept": "application/json"}
            if method in [method_val.value for method_val
                          in HTTPRequestTypes]:
                response = requests.request(method, url,
                                            params=query_params,
                                            json=payload_json,
                                            data=payload_data,
                                            headers=headers,
                                            auth=self.auth_cred)
            #If Wrong Method is being provided.
            else:
                return {Constants.ACTION_RESULT: ErrorMsg.WRONG_MET,
                        Constants.ACTION_STATUS: Constants.ERROR}
            # Status code of the response
            response_data[Constants.STATUS_CODE] = response.status_code
            # If response is successful.
            if response.ok:
                #Providing own custom output if response is None
                if custom_output:
                    response_data[Constants.RESPONSE] = custom_output
                # If Response Comes in Text
                elif response_type == "text":
                    response_data[Constants.RESPONSE] = response.text
                # Response is in JSON.
                else:
                    response_data[Constants.RESPONSE] = response.json()
                execution_status = Constants.SUCCESS
            # If 404 condition is valid situation.
            elif response.status_code == 404 and status_404:
                response_data[Constants.RESPONSE] = response.json()
                execution_status = Constants.SUCCESS
            # If there is Error
            else:
                response_data[Constants.RESPONSE] = json.loads(response.text)
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
