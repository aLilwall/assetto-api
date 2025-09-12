import requests


def get_access_token(api_key):
    """Retrieve an access token from the API token service."""
    token_response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "response_type": "cloud_iam",
            "apikey": api_key,
        },
        headers={
            "Accept": "application/json"
        }
    )
    if token_response.status_code == 200:
        return token_response.json()["access_token"]
    else:
        return None
