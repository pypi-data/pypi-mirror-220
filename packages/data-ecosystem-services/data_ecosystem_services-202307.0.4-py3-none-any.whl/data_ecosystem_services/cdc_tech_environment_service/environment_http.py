
# Example usage
# http_util = EnvironmentHttp()
# url = 'https://example.com/api/data'
# try:
#    response = http_util.get(url)
#    print(response.text)
# except Exception as e:
#    print(f"Error occurred: {str(e)}")

from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)


import requests
from retrying import retry
import os
import sys

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)


class EnvironmentHttp:
    """
    Utility class for making HTTP requests with retry functionality.
    """

    def __init__(self):
        pass

    def create_curl(self, url, headers, timeout, params):
        """
        Creates a cURL command string based on the provided URL, headers, timeout, and params.

        Args:
            url (str): The URL to request in the cURL command.
            headers (dict): Dictionary of headers to include in the cURL command.
            timeout (int): The timeout value in seconds to include in the cURL command.
            params (dict): Dictionary of query parameters to include in the cURL command.

        Returns:
            str: The cURL command string.

        Example:
            create_curl("https://example.com/api/data",
                        {"User-Agent": "MyApp/1.0"},
                        5,
                        {"param1": "value1", "param2": "value2"})

            Output:
            "curl -X GET 'https://example.com/api/data' \\
                -H 'User-Agent: MyApp/1.0' \\
                -m 5 \\
                --data-urlencode 'param1=value1' \\
                --data-urlencode 'param2=value2'"
        """

        curl_command = f"curl -X GET '{url}' \\\n"
        for header, value in headers.items():
            curl_command += f"     -H '{header}: {value}' \\\n"
            curl_command += f"     -m {timeout} \\\n"

        if params is not None:
            for param, value in params.items():
                curl_command += f"     --data-urlencode '{param}={value}' \\\n"

        # Print the cURL command
        return curl_command

    # Retry on 403 errors wait 5 seconds between retries
    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def get(self, url, headers, timeout, params):
        """
        Make a GET request to the specified URL with retry functionality for 403 errors.

        Args:
            url (str): The URL to make the GET request to.
            headers (dict, optional): Dictionary of HTTP headers to send with the request. Defaults to None.
            timeout (float or tuple, optional): Timeout value for the request in seconds. Defaults to None.
            params (dict, optional): Dictionary of query parameters to include in the request. Defaults to None.

        Returns:
            requests.Response: The response object.

        Raises:
            requests.exceptions.HTTPError: If a non-403 HTTP error occurs.
            Exception: If a 403 error occurs after retrying.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME)
        tracer = tracer_singleton.get_tracer()

        # Counter variable to track the number of 403 errors
        error_count = 0

        with tracer.start_as_current_span("get"):

            try:
                if params is None:
                    response = requests.get(
                        url, headers=headers, timeout=timeout, verify=True)
                else:
                    response = requests.get(
                        url, headers=headers, timeout=timeout, params=params, verify=True)

                if response.status_code == 403:
                    error_count += 1
                    if error_count <= 2:
                        error_msg = f"Warning: 403 Error occurred while making GET request to {url}"
                        logger.warning(error_msg)
                        curl_command = self.create_curl(
                            url, headers, timeout, params)
                        logger.warning(
                            "curl of failed request: " + curl_command)
                    else:
                        error_msg = f"Error: 403 Error occurred while making GET request to {url}"
                        logger.error(error_msg)
                        curl_command = self.create_curl(
                            url, headers, timeout, params)
                        logger.error("curl of failed request: " + curl_command)
                    response.raise_for_status()
                return response

            except Exception as err:
                error_msg = f"Error {err} occurred while making GET request to {url}"
                exc_info = sys.exc_info()
                logger_singleton.error_with_exception(error_msg, exc_info)
                curl_command = self.create_curl(url, headers, timeout, params)
                logger.error("curl of failed request: " + curl_command)
                raise err
