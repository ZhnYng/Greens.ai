import pytest
from application.models import Entry, User, Image
from datetime import datetime
from werkzeug.security import generate_password_hash

@pytest.mark.parametrize(
    "entry_list",
    [
        [1, 1, '31x31', 'Bean'],
        [2, 3, '128x128', 'Potato'],
        [1, 4, '128x128', 'Brinjal'],
    ],
)
def test_entry_model(capsys, entry_list):
    """
    Test case to validate the Entry model.

    Args:
        capsys: Pytest fixture for capturing stdout/stderr.
        entry_list (list): A list containing parameters for creating Entry instances.
    """
    with capsys.disabled():
        # Create an instance of the Entry model
        entry = Entry(
            user_id=entry_list[0],
            image_id=entry_list[1],
            model=entry_list[2],
            predicted_vegetable=entry_list[3],
            predicted_on=datetime.utcnow(),
        )

        assert entry.user_id == entry_list[0]
        assert entry.image_id == entry_list[1]
        assert entry.model == entry_list[2]
        assert entry.predicted_vegetable == entry_list[3]


@pytest.mark.parametrize(
    "user_list",
    [
        ['test@gmail.com', 'Michael', 'Bean125%23'],
        ['test2@gmail.com', 'ZhenYang', 'password&@(#)'],
        ['test3@gmail.com', 'tester', "testpassword&@(*#23)"],
    ],
)
def test_user_model(capsys, user_list):
    """
    Test case to validate the User model.

    Args:
        capsys: Pytest fixture for capturing stdout/stderr.
        user_list (list): A list containing parameters for creating User instances.
    """
    with capsys.disabled():
        # Create an instance of the User model
        hashed_password = generate_password_hash(
            user_list[2], method="pbkdf2:sha1"
        )

        user = User(
            email=user_list[0], 
            name=user_list[1], 
            password=hashed_password
        )

        assert user.email == user_list[0]
        assert user.name == user_list[1]
        assert user.password == hashed_password


@pytest.mark.parametrize(
    "image_list",
    [
        ['./images/test.png', 'image/png', 'test.png'],
        ['./images/testimage2.png', 'image/png', 'testimage2.png'],
        ['./images/1002.png', 'image/png', "1002.png"],
    ],
)
def test_image_model(capsys, image_list):
    """
    Test case to validate the Image model.

    Args:
        capsys: Pytest fixture for capturing stdout/stderr.
        image_list (list): A list containing parameters for creating Image instances.
    """
    with capsys.disabled():
        # Create an instance of the Image model
        image = Image(
            filepath=image_list[0],
            mimetype=image_list[1], 
            name=image_list[2],
        )

        assert image.filepath == image_list[0]
        assert image.mimetype == image_list[1]
        assert image.name == image_list[2]