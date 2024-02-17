import requests
from flask import request, Response, json, redirect, url_for, jsonify, send_file
from flask_cors import CORS
from datetime import datetime, timedelta, timezone
import time

# from flask_cors import CORS
from flask_login import (
    login_user,
    login_required,
    logout_user,
    LoginManager,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from . import app
from application import db
from application.models import Entry, User, Image
from datetime import datetime
from application.utils.QueryUtils import QueryUtils
from application.utils.Validation import Validation
from application.utils.Authorization import Authorization

from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_required,
    JWTManager,
    decode_token,
)

# Imports for manipulating images
import numpy as np
import base64
import re
import io
import os
from PIL import Image as PILImage, ImageOps


CORS(app)
jwt = JWTManager(app)

@app.route('/')
def index():
    """
    For changing the root path of flask to point to index.html automatically
    """
    return app.send_static_file('index.html')


@app.route("/upload", methods=["POST"])
def upload():
    """
    Route to handle image upload.

    This route accepts a POST request containing an image file. The image is uploaded
    to the server and stored in the 'images' folder. The route performs input validation
    to ensure that an image file is provided and that its MIME type is valid.
    Upon successful upload, metadata about the image, including the filepath and filename,
    is stored in the database using QueryUtils.add_entry(). The route returns a JSON response
    indicating the success of the upload and provides the generated image ID for further reference.

    Returns:
        - JSON response indicating success or failure of the upload process.
    """
    try:
        # Check if the "images" folder exists, and create it if it doesn't
        images_folder = "images"
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)

        pic = request.files["image"]

        if not pic:
            return jsonify({"error": "No image uploaded"}), 400
        
        filename = secure_filename(pic.filename)
        input_mimetype = pic.mimetype

        # input validation
        validation = Validation()
        try:
            validation.img_validation(input_mimetype)
        except ValueError as err:
            return jsonify({"error": str(err)}), 400

        filename = '{}.png'.format(filename.split('.')[0])
        mimetype = 'image/png'

        image = PILImage.open(io.BytesIO(pic.read()))
        
        timestamp = int(time.time())
        filepath = f'images/{timestamp}_{filename}'
        image.save(filepath) # Save as png as it is more flexible

        image = Image(filepath=filepath, mimetype=mimetype, name=filename)
        query_utils = QueryUtils()
        image_id = query_utils.add_entry(image)
        return (
            jsonify({"image_id": f"{image_id}", "success": f"{filename} uploaded"}),
            201,
        )
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"Upload failed: {error}"}), 500


@app.route("/get_image/<int:image_id>", methods=["GET"])
def get_image(image_id):
    """
    Route to retrieve an image by its ID.

    This route accepts a GET request with an image ID parameter. It retrieves
    the corresponding image from the database using QueryUtils.get_entries_where().
    If the image is found, it opens the image file, reads it, and returns the
    image data as a response in PNG format. The route ensures that the appropriate
    MIME type is set for the response. If the image retrieval fails, an error
    message is returned.

    Args:
        image_id (int): The ID of the image to retrieve.

    Returns:
        - Image data in PNG format as a response.
        - JSON error message if the image retrieval fails.
    """
    try:
        query_utils = QueryUtils()
        result = query_utils.get_entries_where(
            model=Image, condition=Image.id == image_id
        )[0]

        if not result:
            return jsonify({"error": f"No image with id: {image_id}"}), 400

        filepath = result.get('filepath')
        image = PILImage.open(filepath)
        
        def serve_pil_image(pil_img):
            img_io = io.BytesIO()
            pil_img.save(img_io, 'PNG', quality=70)
            img_io.seek(0)
            return send_file(img_io, mimetype=result.get('mimetype'))

        return serve_pil_image(image)
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"Get image failed: {error}"}), 500


@app.route("/predict/<string:model>", methods=["POST"], strict_slashes=False)
@jwt_required()
def predict(model):
    """
    Route to predict the class of an image using a deployed machine learning model.

    This route accepts a POST request containing JSON data with an image ID and the desired model size.
    The image is retrieved from the database using the provided image ID.
    The image is preprocessed by converting it to grayscale and resizing it to the specified model size.
    The preprocessed image is then sent to a deployed machine learning model for prediction.
    The predicted class of the image is determined based on the highest probability in the prediction output.
    The result, along with the image metadata, is stored in the database.
    If successful, the predicted class is returned as a JSON response with a success status code (200).
    If there are any errors during the prediction process, appropriate error messages are returned.

    Args:
        model (string): The size of the model to use for prediction ('31x31' or '128x128').

    Returns:
        - JSON response indicating the predicted class of the image.
        - JSON error message if the prediction process fails.
    """
    INDEX_TO_CLASS_MAPPING = {
        0: "Bean",
        1: "Bitter_Gourd",
        2: "Bottle_Gourd",
        3: "Brinjal",
        4: "Broccoli",
        5: "Cabbage",
        6: "Capsicum",
        7: "Carrot",
        8: "Cauliflower",
        9: "Cucumber",
        10: "Papaya",
        11: "Potato",
        12: "Pumpkin",
        13: "Radish",
        14: "Tomato",
    }

    try:
        if request.method == "POST":
            prediction_data = request.json
            jwt_token = request.headers["Authorization"].split(" ")[1]
            decoded_jwt_token = decode_token(jwt_token)

            # Input validation
            if not model == '31x31' and not model == '128x128': raise ValueError("Model can only be '31x31' or '128x128'.")
            if not prediction_data["image_id"]: raise ValueError("Image id not provided.")
            
            # Retrieve image
            try:
                image_id = prediction_data["image_id"]
                query_utils = QueryUtils()
                result = query_utils.get_entries_where(
                    model=Image, condition=Image.id == image_id
                )[0]

                if not result:
                    return jsonify({"error": f"No image with id: {image_id}"}), 400

                filepath = result.get('filepath')
                image = PILImage.open(filepath)
                

            except Exception as error:
                db.session.rollback()
                return jsonify({"error": f"Get image failed: {error}"}), 500

            # Preprocess image
            image = image.convert('L') # Grayscale

            if model == "31x31":
                image = image.resize((31, 31), PILImage.NEAREST) # Resize with "nearest" method
            elif model == "128x128":
                image = image.resize((128, 128), PILImage.NEAREST) # Resize with "nearest" method
                
            img_array = np.array(image)  # Convert the image to numpy array

            img_array_expanded_dims = np.expand_dims(img_array, axis=0)  # Add an extra dimension for batch size
            img_array_expanded_dims = np.expand_dims(img_array_expanded_dims, axis=-1)  # Add an extra dimension for color channels

            img_preprocessed = img_array_expanded_dims / 255.0  # Normalization

            # Classify image
            def make_prediction(model_url, instances):
                data = json.dumps(
                    {
                        "signature_name": "serving_default",
                        "instances": instances.tolist(),
                    }
                )
                headers = {"content-type": "application/json"}
                json_response = requests.post(model_url, data=data, headers=headers)
                predictions = json.loads(json_response.text)["predictions"]
                return predictions

            deployed_model_url_128x128 = "https://ca2-model-server-mfp2.onrender.com/v1/models/128x128_vgg_l2:predict"
            deployed_model_url_31x31 = "https://ca2-model-server-mfp2.onrender.com/v1/models/31x31_vgg_l2:predict"

            if model == "31x31":
                prediction = make_prediction(deployed_model_url_31x31, img_preprocessed)
            elif model == "128x128":
                prediction = make_prediction(deployed_model_url_128x128, img_preprocessed)

            predicted_vegetable = INDEX_TO_CLASS_MAPPING[np.argmax(prediction, axis=1)[0]]

            # Add result to entry/history table
            new_entry = Entry(
                user_id=decoded_jwt_token['sub'],
                image_id=image_id,
                model=model,
                predicted_vegetable=predicted_vegetable,
                predicted_on=datetime.utcnow(),
            )
            query_utils = QueryUtils()
            query_utils.add_entry(new_entry)

            return jsonify({"success": predicted_vegetable}), 200
        
    except ValueError as error:
        return jsonify({"error": f"Prediction failed: {error}"}), 400

    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"Prediction failed: {error}"}), 500


# Handles /getUserPredictions
# Gets the past predictions of the currently logged in user
@app.route("/getUserPredictions", methods=["GET"], strict_slashes=False)
@jwt_required()
def getPastPredictions():
    """
    Route to retrieve past predictions of the currently logged-in user.

    This route accepts a GET request and requires a valid JWT token for authentication.
    It retrieves the user ID from the JWT token and uses it to query past predictions from the database.
    If predictions are found, the route fetches additional details such as image and user information.
    The results are returned as a JSON response with a success status code (200).
    If there are no past predictions for the user, an empty array is returned with a success status code (200).
    If there are any errors during the retrieval process, appropriate error messages are returned.

    Returns:
        - JSON response containing past predictions of the user.
        - JSON response with an empty array if no predictions are found.
        - JSON error message if the retrieval process fails.
    """
    query_utils = QueryUtils()
    try:
        jwt_token = request.headers["Authorization"].split(" ")[1]
        decoded_jwt_token = decode_token(jwt_token)
        user_id = decoded_jwt_token['sub']

        results = query_utils.get_entries_where(
            model=Entry, condition=Entry.user_id == user_id
        )

        if results:
            # Search get image and user details with image and user id
            for data in results:
                image = query_utils.get_entries_where(
                    model=Image, condition=Image.id == data.get('image_id')
                )[0]
                user = query_utils.get_entries_where(
                    model=User, condition=User.id == data.get('user_id')
                )[0]
                data['user_details'] = user
                data['image_details'] = image

            return jsonify({'success': results}), 200
        else:
            return jsonify({"success": []}), 200
    
    except Exception as error:
        return jsonify({"error": f"Get failed: {error}"}), 500
    

# Handles /removePastPrediction/:id
@app.route("/removePastPrediction/<int:id>", methods=["DELETE"], strict_slashes=False)
@jwt_required()
def removePastPrediction(id):
    """
    Route to remove a past prediction identified by its ID.

    This route accepts a DELETE request and requires a valid JWT token for authentication.
    The ID of the prediction to be removed is provided in the route URL.
    The route first authorizes the user to perform the deletion operation.
    If the user is authorized, the prediction associated with the provided ID is removed from the database.
    If the deletion is successful, a success message with a status code (200) is returned.
    If the provided ID is invalid or the user is not authorized, appropriate error messages are returned.

    Args:
        id (int): The ID of the prediction to be removed.

    Returns:
        - JSON success message indicating successful removal of the prediction.
        - JSON error message if the deletion operation fails due to an invalid ID, unauthorized user, or other errors.
    """
    query_utils = QueryUtils()
    try:
        # Authorization
        authorization = Authorization()
        jwt_token = request.headers['Authorization'].split(' ')[1]
        auth_result = authorization.model_auth(Entry, id, jwt_token)
        if auth_result == "Not Authorized":
            return jsonify({"error": f"{auth_result}"}), 403

        query_utils.remove_entry(id, Entry)
        return jsonify({"success": f"Removed {id} successfully"}), 200
    
    except IndexError as error:
        return jsonify({"error": f"Delete failed: {error}"}), 400
    
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": f"Delete failed: {error}"}), 500


# Handle /searchForPrediction?vegetable_name=Broccoli&model=31x31
@app.route("/searchForPrediction")
def searchForPrediction():
    """
    Route to search for predictions based on provided query parameters.

    This route handles GET requests and accepts query parameters:
    - 'vegetable_name': Optional. Name of the vegetable to search for predictions.
    - 'model': Optional. Model used for the prediction, can be '31x31' or '128x128'.
    - 'userId': Optional. ID of the user whose predictions are to be searched.

    The route performs input validation to ensure the correctness of the query parameters.
    If 'vegetable_name' is provided, it must be one of the predefined vegetable names.
    If 'model' is provided, it must be either '31x31' or '128x128'.
    The route then queries the database based on the provided parameters to retrieve predictions.
    If 'userId' is provided, predictions for that specific user are retrieved.
    Otherwise, predictions are retrieved based on 'vegetable_name' and 'model'.
    The route returns a JSON response with the matching predictions, including details of images and users.

    Returns:
        - JSON object containing a list of matching predictions along with image and user details.
        - JSON error message if the search operation fails due to invalid input or database error.
    """
    vegetable_name = request.args.get("vegetable_name")
    model = request.args.get("model")
    user_id = request.args.get("userId")

    # input validation
    try:
        if vegetable_name and vegetable_name not in ['Bean', 'Bitter_Gourd', 'Bottle_Gourd', 'Brinjal', 'Broccoli', 'Cabbage', 'Capsicum', 'Carrot', 'Cauliflower', 'Cucumber', 'Papaya', 'Potato', 'Pumpkin', 'Radish', 'Tomato']:
            raise ValueError("Vegetable name is invalid.")
        if model and not model == '31x31' and not model == '128x128': 
            raise ValueError("Model can only be '31x31' or '128x128'.")
    except ValueError as err:
        return jsonify({"error": str(err)}), 400

    try:
        query_utils = QueryUtils()
        if user_id:
            if vegetable_name and model:
                result = query_utils.get_entries_where_triple(
                    Entry, 
                    Entry.predicted_vegetable==vegetable_name,
                    Entry.model==model,
                    Entry.user_id==user_id
                )
            elif vegetable_name:
                result = query_utils.get_entries_where_double(
                    Entry, 
                    Entry.predicted_vegetable==vegetable_name,
                    Entry.user_id==user_id
                )
            elif model:
                result = query_utils.get_entries_where_double(
                    Entry, 
                    Entry.model==model,
                    Entry.user_id==user_id
                )
            else:
                result = query_utils.get_entries_where(
                    Entry, 
                    Entry.user_id==user_id
                )
        else:
            if vegetable_name and model:
                result = query_utils.get_entries_where_double(
                    Entry, 
                    Entry.predicted_vegetable==vegetable_name,
                    Entry.model==model
                )
            elif vegetable_name:
                result = query_utils.get_entries_where(
                    Entry, 
                    Entry.predicted_vegetable==vegetable_name
                )
            elif model:
                result = query_utils.get_entries_where(
                    Entry, Entry.model==model
                )
            else:
                result = query_utils.get_entries(Entry)

        # Search get image and user details with image and user id
        for data in result:
            image = query_utils.get_entries_where(
                model=Image, condition=Image.id == data.get('image_id')
            )[0]
            user = query_utils.get_entries_where(
                model=User, condition=User.id == data.get('user_id')
            )[0]
            data['user_details'] = user
            data['image_details'] = image

        return jsonify({"success": result}), 200
    except Exception as error:
        return jsonify({"error": f"Get failed: {error}"}), 500


"""
User credential routes
1. POST /signup
2. POST /login
3. POST /logout
4. GET /getCurrentUser
"""
@app.route("/signup", methods=["POST"])
def signup():
    """
    Route for signing up a new user.

    Accepts POST requests with JSON data containing user information.
    Required fields: 'email', 'name', 'password'.
    Performs input validation for the required fields:
        - 'email' must be a valid email address.
        - 'name' must be a non-empty string.
        - 'password' must meet specified criteria (e.g., minimum length).

    Checks if the provided email is already in use.
    If not, hashes the provided password and creates a new user record in the database.
    
    Returns:
        - JSON object with a success message if the account is successfully created.
        - JSON error message if input validation fails or if an error occurs during account creation.
    """
    try:
        userData = request.json

        # input validation
        validation = Validation()
        try:
            validation.validate_fields(
                required_fields=["email", "name", "password"], body=userData
            )
            validation.email_validation(userData["email"])
            validation.name_validation(userData["name"])
            validation.password_validation(userData["password"])
        except AssertionError as err:
            return jsonify({"error": str(err)}), 400

        # Check if the email is already in use
        existing_user = (
            db.session.query(User).filter_by(email=userData["email"]).first()
        )
        if existing_user:
            return jsonify({"error": "This email has already been used."}), 400

        # Hash the password so the plaintext version isn't saved
        hashed_password = generate_password_hash(
            userData["password"], method="pbkdf2:sha1"
        )

        # Create a new user with the form data
        new_user = User(
            email=userData["email"], name=userData["name"], password=hashed_password
        )
    
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"success": "Account created!"}), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app.route("/login", methods=["POST"])
def login():
    """
    Route for logging in a user.

    Accepts POST requests with JSON data containing user login information.
    Required fields: 'email', 'password', 'remember_me'.
    Performs input validation for the required fields:
        - 'email' must be a valid email address.
        - 'password' must be a non-empty string.
        - 'remember_me' must be a boolean value.
    
    Retrieves the user from the database based on the provided email.
    Validates the password against the hashed password stored in the database.
    If the login credentials are valid, generates a JWT access token for the user.
    
    Returns:
        - JSON object with the JWT access token if login is successful.
        - JSON error message if input validation fails or if the login credentials are invalid.
    """
    userData = request.json

    validation = Validation()
    try:
        validation.validate_fields(["email", "password", "remember_me"], userData)
    except AssertionError as err:
        return jsonify({"error": str(err)}), 400

    user = db.session.query(User).filter_by(email=userData["email"]).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user:
        return jsonify({"error": "Email does not exist"}), 400
    if not check_password_hash(user.password, userData["password"]):
        # if the user doesn't exist or password is wrong, reload the page
        return jsonify({"error": "Password is incorrect"}), 400

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=bool(userData["remember_me"]))
    access_token = create_access_token(identity=user.id)

    return jsonify({"access_token": access_token}), 200


@app.after_request
def refresh_expiring_jwts(response):
    """
    Middleware function to refresh expiring JWT tokens.

    This function is executed after each request. It checks if the JWT access token
    is about to expire within the next 30 minutes. If so, it generates a new access token
    for the same user identity and adds it to the response JSON data.

    Returns:
        - Original response if there is no valid JWT or if the JWT does not need refreshing.
        - Response with the updated access token if JWT refreshing is performed.
    """
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Route for logging out a user.

    Returns:
        - Response with a message indicating successful logout and cleared JWT cookies.
    """
    logout_user()
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response, 200


@app.route("/getCurrentUser")
@jwt_required()
def get_current_user():
    """
    Route for retrieving details of the currently logged-in user.

    Returns:
        - JSON response containing user details:
            - "id": User ID
            - "email": User email
            - "name": User name
    """
    jwt_token = request.headers["Authorization"].split(" ")[1]
    decoded_jwt_token = decode_token(jwt_token)

    query_utils = QueryUtils()
    user = query_utils.get_entries_where(User, User.id == decoded_jwt_token["sub"])[0]

    try:
        return Response(
            json.dumps(
                {
                    "id": user.get("id"),
                    "email": user.get("email"),
                    "name": user.get("name"),
                }
            ),
            status=200,
            mimetype="application/json",
        )
    except Exception as error:
        return jsonify({"error": f"Get current user failed: {error}"}), 500


@app.route('/getUser/<int:id>')
def get_user(id):
    """
    Route for retrieving user details by user ID.

    Args:
        id (int): User ID.

    Returns:
        - JSON response containing user details if the user is found:
            - "success": User details (ID, email, name)
        - JSON response with an error message if the user is not found or an error occurs.
    """
    query_utils = QueryUtils()
    try:
        results = query_utils.get_entries_where(
            model=User, 
            condition=User.id == id
        )[0]

        if not results:
            return jsonify({"error": "User not found"}), 400
        
        return jsonify({"success", results})
    
    except Exception as error:
        return jsonify({"error": f"Get failed: {error}"}), 500