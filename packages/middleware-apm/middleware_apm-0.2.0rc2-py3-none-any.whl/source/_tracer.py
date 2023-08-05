import os
import requests, json
import pyroscope
from opentelemetry import trace

mw_agent_target = os.environ.get('MW_AGENT_SERVICE', '127.0.0.1')


def track(project_name, service_name, access_token="",
          enabled_profiling=True) -> None:
    # Profiling application, if enabled
    if enabled_profiling and access_token != "":

        # Setting Middleware Account Authentication URL
        auth_url = os.getenv('MW_AUTH_URL', 'https://app.middleware.io/api/v1/auth')

        # Setting Middleware Profiling Server URL
        profiling_server_url = os.getenv('MW_PROFILING_SERVER_URL', 'https://profiling.middleware.io')

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            # "Authorization": "Bearer " + c.accessToken
            "Authorization": "Bearer " + access_token
        }
        try:
            response = requests.post(auth_url, headers=headers)

            # Checking if auth API returns status code 200
            if response.status_code == 200:
                data = json.loads(response.text)

                # Checking if a tenantID could be fetched from API Key
                if data["success"]:
                    account = data["data"]["account"]
                    pyroscope.configure(
                        application_name=service_name,  # replace this with some name for your application
                        server_address=profiling_server_url,
                        # replace this with the address of your pyroscope server
                        tenant_id=account,
                    )
                else:
                    print("Request failed: " + data["error"])
            else:
                print("Request failed with status code: " + str(response.status_code))
        except Exception as e:
            print("Error making request:", e)
    else:
        print("Profiling is not enabled or access token is empty")

    # Setting values for tracing application
    if type(project_name) is not str:
        print("project name must be a string")
        return
    if type(service_name) is not str:
        print("service name must be a string")
        return


def record_error(error):
    span = trace.get_current_span()
    span.record_exception(error)
    span.set_status(trace.Status(trace.StatusCode.ERROR, str(error)))


# def set_attribute(name, value):
#     if type(name) is not str:
#         print("name must be a string")
#         return
#     if type(value) is not str:
#         print("value must be a string")
#         return
#     span = trace.get_current_span()
#     span.set_attribute(name, value)
