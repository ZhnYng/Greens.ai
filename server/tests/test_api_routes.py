from application.models import Entry
from datetime import datetime
from application.utils.QueryUtils import QueryUtils
from application.utils.Validation import Validation
from application.models import Entry, User, Image
from application import db
from flask import json
import pytest
import os
import io
from flask_jwt_extended import decode_token


resources_url = os.path.join('tests', 'resources')

@pytest.mark.parametrize(
    "entrylist",
    [
        [r'0002.jpg'],
        [r'1014.jpg'],
        [r'1019.jpg'],
    ],
)
def test_upload_image(
    entrylist, client, capsys
):
    """
    Test for uploading an image.

    Args:
        entrylist: List containing file names of images to be uploaded.
        client: Test client for the Flask app.
        capsys: Fixture for capturing stdout and stderr during tests.
    """
    with capsys.disabled():
        with open(os.path.join(resources_url, entrylist[0]), 'rb') as img1:
            imgStringIO1 = io.BytesIO(img1.read())

        body = {"image": (imgStringIO1, entrylist[0])}
        response = client.post(
            "/upload",
            data=body,
            content_type="multipart/form-data",
        )
        response_body = json.loads(response.get_data(as_text=True))
        assert response.status_code == 201
        
        query_utils = QueryUtils()
        last_row = query_utils.get_entries(Image)[-1]
        assert str(response_body) == str({"image_id": f"{last_row.get('id')}", "success": f"{last_row.get('name')} uploaded"})


@pytest.mark.xfail(reason='Invalid file types')
@pytest.mark.parametrize(
    "entrylist",
    [
        [r'random.txt'],
        [r'unknown.csv'],
    ],
)
def test_upload_invalid_image(
    entrylist, client, capsys
):
    """
    Test for attempting to upload an invalid image.

    Args:
        entrylist: List containing file names of invalid images.
        client: Test client for the Flask app.
        capsys: Fixture for capturing stdout and stderr during tests.
    """
    with capsys.disabled():
        with open('/'+os.path.join(resources_url, entrylist[0]), 'rb') as img1:
            imgStringIO1 = io.BytesIO(img1.read())

        body = {"image": (imgStringIO1, entrylist[0])}
        response = client.post(
            "/upload",
            data=body,
            content_type="multipart/form-data",
        )
        response_body = json.loads(response.get_data(as_text=True))
        assert response.status_code == 201
        
        query_utils = QueryUtils()
        last_row = query_utils.get_entries(Image)[-1]
        assert str(response_body) == str({"image_id": f"{last_row.get('id')}", "success": f"{last_row.get('name')} uploaded"})


@pytest.mark.parametrize(
    "entrylist",
    [
        [r'huge_image.jpg'],
        [r'tiny_image.jpg'],
    ],
)
def test_upload_edge_image(
    entrylist, client, capsys
):
    """
    Test for uploading edge case images (huge or tiny).

    Args:
        entrylist: List containing file names of edge case images to be uploaded.
        client: Test client for the Flask app.
        capsys: Fixture for capturing stdout and stderr during tests.
    """
    with capsys.disabled():
        with open(os.path.join(resources_url, entrylist[0]), 'rb') as img1:
            imgStringIO1 = io.BytesIO(img1.read())

        body = {"image": (imgStringIO1, entrylist[0])}
        response = client.post(
            "/upload",
            data=body,
            content_type="multipart/form-data",
        )
        response_body = json.loads(response.get_data(as_text=True))
        assert response.status_code == 201
        
        query_utils = QueryUtils()
        last_row = query_utils.get_entries(Image)[-1]
        assert str(response_body) == str({"image_id": f"{last_row.get('id')}", "success": f"{last_row.get('name')} uploaded"})


@pytest.mark.parametrize(
    "entrylist",
    [
        [1],
        [2],
        [3],
    ],
)
def test_get_image(
    entrylist, user1, client, capsys
):
    """
    Test for retrieving an image.

    Args:
        entrylist: List containing image IDs to retrieve.
        user1: Fixture providing access token of a user.
        client: Test client for the Flask app.
        capsys: Fixture for capturing stdout and stderr during tests.
    """
    with capsys.disabled():
        jwt_token = user1["access_token"]
        response = client.get(
            f"/get_image/{entrylist[0]}",
            content_type="application/json",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        response_body = response.get_data()

        assert response.status_code == 200
        # Test that route returns images in bytes
        assert type(response_body) == bytes


import pytest
import json
from application import app as flask_app
from application.utils.QueryUtils import QueryUtils

@pytest.mark.parametrize(
    "entrylist",
    [
        ['1', '31x31', 'Bean'],
        ['3', '128x128', 'Brinjal'],
        ['2', '31x31', 'Carrot'],
    ],
)
def test_predict(entrylist, user1, client, capsys):
    """
    Test for making predictions using the 'predict' route.

    Args:
        entrylist: List containing image ID, model type, and expected predicted vegetable.
        user1: Fixture providing access token of a user.
        client: Test client for the Flask app.
        capsys: Fixture for capturing stdout and stderr during tests.
    """
    with capsys.disabled():
        body = {"image_id": entrylist[0]}
        jwt_token = user1["access_token"]
        response = client.post(
            f"/predict/{entrylist[1]}",
            data=json.dumps(body),
            content_type="application/json",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        response_body = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert str(response_body) == str({"success": entrylist[2]})


@pytest.mark.parametrize(
    "entrylist",
    [
        ['1', '31x31_model', 'Broccoli'],
        ['2', '244x244', 'Broccoli'],
        ['3', 'None', 'Broccoli'],
    ],
)
def test_invalid_predict(entrylist, user1, client, capsys):
    """
    Test for invalid predictions using the 'predict' route.

    Args:
        entrylist: List containing image ID, invalid model type, and expected error message.
        user1: Fixture providing access token of a user.
        client: Test client for the Flask app.
        capsys: Fixture for capturing stdout and stderr during tests.
    """
    with capsys.disabled():
        body = {"image_id": entrylist[0]}
        jwt_token = user1["access_token"]
        response = client.post(
            f"/predict/{entrylist[1]}",
            data=json.dumps(body),
            content_type="application/json",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        response_body = json.loads(response.get_data(as_text=True))

        assert response.status_code == 400
        assert str(response_body) == str({"error": f"Prediction failed: Model can only be '31x31' or '128x128'."})


def test_search_for_prediction(client, capsys):
    """
    Test for searching predictions using the 'searchForPrediction' route.

    Args:
        client: Test client for the Flask app.
        capsys: Fixture for capturing stdout and stderr during tests.
    """
    with capsys.disabled():
        response = client.get(
            f"/searchForPrediction",
        )
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"


def test_search_for_prediction_invalid_vegetable_name(
    client, capsys
):
    """
    Test for searching predictions with an invalid vegetable name.
    """
    with capsys.disabled():
        response = client.get(
            f"/searchForPrediction?vegetable_name=Egg",
        )
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"

        
def test_search_for_prediction_invalid_model(
    client, capsys
):
    """
    Test for searching predictions with an invalid model.
    """
    with capsys.disabled():
        response = client.get(
            f"/searchForPrediction?model=224x224",
        )
        assert response.status_code == 400
        assert response.headers["Content-Type"] == "application/json"


def test_get_user_predictions(
    user1, client, capsys
):
    """
    Test case to verify the retrieval of user predictions.

    Args:
        user1 (dict): A dictionary containing user authentication details.
        client: Flask test client.
        capsys: Pytest fixture for capturing stdout/stderr.
    """
    with capsys.disabled():
        jwt_token = user1["access_token"]
        response = client.get(
            f"/getUserPredictions",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"


def test_remove_predictions(
    user1, client, capsys
):
    """
    Test case to verify the removal of past predictions.

    Args:
        user1 (dict): A dictionary containing user authentication details.
        client: Flask test client.
        capsys: Pytest fixture for capturing stdout/stderr.
    """
    with capsys.disabled():
        query_utils = QueryUtils()
        last_row = query_utils.get_entries(Entry)[-1]

        jwt_token = user1["access_token"]
        response = client.delete(
            f"/removePastPrediction/{last_row.get('id')}",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        response_body = json.loads(response.get_data(as_text=True))

        assert response.status_code == 200


def test_remove_predictions(
    user2, client, capsys  # Using user2 which is not the owner of the records
):
    """
    Test case to verify that a user cannot remove predictions they do not own.

    Args:
        user2 (dict): A dictionary containing user authentication details.
        client: Flask test client.
        capsys: Pytest fixture for capturing stdout/stderr.
    """
    with capsys.disabled():
        query_utils = QueryUtils()
        last_row = query_utils.get_entries(Entry)[-1]

        jwt_token = user2["access_token"]
        response = client.delete(
            f"/removePastPrediction/{last_row.get('id')}",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        response_body = json.loads(response.get_data(as_text=True))

        assert response.status_code == 403


@pytest.mark.parametrize(
    "invalid_entry_row_ids",
    [
        ['456789'],
        ['4567344'],
        ['6789876'],
    ],
)
def test_invalid_remove_predictions(
    invalid_entry_row_ids, user1, client, capsys
):
    """
    Test case to verify that attempting to remove an invalid prediction fails gracefully.

    Args:
        invalid_entry_row_ids (list): A list containing invalid prediction IDs.
        user1 (dict): A dictionary containing user authentication details.
        client: Flask test client.
        capsys: Pytest fixture for capturing stdout/stderr.
    """
    with capsys.disabled():
        jwt_token = user1["access_token"]
        
        response = client.delete(
            f"/removePastPrediction/{invalid_entry_row_ids[0]}",
            headers={"Authorization": f"Bearer {jwt_token}"},
        )
        response_body = json.loads(response.get_data(as_text=True))
        assert response.status_code == 400
        assert str(response_body) == str({"error": f"Delete failed: list index out of range"})