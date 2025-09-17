import requests
from flask import Flask, request
from cloudant_auth import get_access_token

API_KEY = "mw-us01eVjYEtSIWjPVZ3xQ_sAKFBVDDZUeaEuwNbvX8"
ACCOUNT = "a01a2d5d-4843-41b4-9b11-6d08205eefab-bluemix"

app = Flask(__name__)


@app.route("/")
def is_running():
    """Method to test connection with the API and Cloudant Database.
    """
    return get()


@app.get("/items")
def get():
    """Get method that returns all documents from Cloudant.
    """
    response = response = requests.get(
        f"https://{ACCOUNT}.cloudantnosqldb.appdomain.cloud/blender-models/_all_docs",
        headers={
            "content-type": "application/json",
            "Authorization": f"Bearer {get_access_token(api_key=API_KEY)}"
        }
    )
    documents = response.json()
    return documents['rows'], 200


@app.get("/item/<string:item_name>")
def get_item(item_name):
    """Get method that returns a specific document from Cloudant.
    """
    response = requests.get(
        f"https://{ACCOUNT}.cloudantnosqldb.appdomain.cloud/blender-models/{item_name}",
        headers={
            "content-type": "application/json",
            "Authorization": f"Bearer {get_access_token(api_key=API_KEY)}"
        }
    )

    if response.status_code == 200:
        document = response.json()

    return {item_name: document[item_name]}


@app.post("/item")
def post_item():
    """Post method that creates a new document in Cloundant.
    """
    data = request.get_json()

    key, *_ = data.items()
    _id, models = key

    payload = {"_id": _id, _id: models}

    response = requests.post(
        f"https://{ACCOUNT}.cloudantnosqldb.appdomain.cloud/blender-models",
        headers={
            "content-type": "application/json",
            "Authorization": f"Bearer {get_access_token(API_KEY)}"
        },
        json=payload
    )

    if response.status_code == 201:
        document = response.json()
        return document
    elif response.status_code == 409:
        get = requests.get(
            f"https://{ACCOUNT}.cloudantnosqldb.appdomain.cloud/blender-models/{_id}",
            headers={
                "content-type": "application/json",
                "Authorization": f"Bearer {get_access_token(API_KEY)}"
            }
        )

        data = get.json()
        rev = data["_rev"]

        response = requests.delete(
            f"https://{ACCOUNT}.cloudantnosqldb.appdomain.cloud/blender-models/{_id}?rev={rev}",
            headers={
                "content-type": "application/json",
                "Authorization": f"Bearer {get_access_token(API_KEY)}"
            }
        )
        post_item()
    else:
        return f"Failed to create document, error code:{response.status_code}"


@app.put("/item/<string:document_id>")
def put_item(document_id):
    """Put method that update a document in Cloudant.
    """
    pass


@app.delete("/item/<string:document_id>")
def delete_item(document_id):
    """Post method that deletes a document in Cloundant.
    """
    get = requests.get(
        f"https://{ACCOUNT}.cloudantnosqldb.appdomain.cloud/blender-models/{document_id}",
        headers={
            "content-type": "application/json",
            "Authorization": f"Bearer {get_access_token(API_KEY)}"
        }
    )

    data = get.json()
    rev = data["_rev"]

    response = requests.delete(
        f"https://{ACCOUNT}.cloudantnosqldb.appdomain.cloud/blender-models/{document_id}?rev={rev}",
        headers={
            "content-type": "application/json",
            "Authorization": f"Bearer {get_access_token(API_KEY)}"
        }
    )

    return response.json(), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
