import requests, os
from fastapi import HTTPException
class BackendError(RuntimeError):
    def __init__(self, *args: object, **kwargs) -> None:
        self.response = kwargs.pop("response", None)
        super().__init__(*args)

def get_request_json(url: str, headers: dict) -> dict:
    """
    Send a GET request to the specified URL with the provided headers. 
    Handle any errors that might occur and return the result of the request 
    parsed into JSON format within a python dictionary.
    """
    try:
        response = requests.get(url, headers=headers)
        # Check if the request was successful
        response.raise_for_status()
    except requests.HTTPError as http_err:
        # Handle HTTP errors
        raise BackendError(
            f"HTTP error occurred: {http_err}",
            response=response,
        ) from http_err
    except Exception as err:
        # Handle any other exceptions that requests might raise
        raise BackendError(
            f"An error occurred: {err}",
            response=response,
        ) from err

    #Ensure the response is valid JSON
    try:
        result = response.json()
    except requests.JSONDecodeError as e:
        raise BackendError(
            f"Error decoding JSON from {url}. Text response: {response.text}",
            response=response,
        ) from e

    return result

def get_env_variable(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise HTTPException(status_code=400, detail=f"{name} must be set")
    return value