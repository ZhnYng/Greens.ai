import pytest

# Testing password_validation method
def test_password_valid(validator):
    assert validator.password_validation("ValidPass123") is None

def test_password_short(validator):
    with pytest.raises(AssertionError, match="Password must have at least 8 characters"):
        validator.password_validation("Short1")

def test_password_no_uppercase(validator):
    with pytest.raises(AssertionError, match="Password must have at least one uppercase letter"):
        validator.password_validation("nouppercase1")

# Testing email_validation method
def test_email_valid(validator):
    assert validator.email_validation("example@test.com") is None

def test_email_invalid(validator):
    with pytest.raises(AssertionError, match="Invalid email format"):
        validator.email_validation("invalidemail")

# Testing integer validation method
def test_int_valid(validator):
    assert validator.int_validation(10) is None

def test_int_invalid(validator):
    with pytest.raises(AssertionError, match="Variable must be an integer"):
        validator.int_validation(0.01)

@pytest.mark.parametrize("mimetypes", [['image/jpeg'], ['image/png'], ['image/jpg']])
def test_img_valid(validator, mimetypes):
    assert validator.img_validation(mimetypes[0]) is None

@pytest.mark.parametrize("mimetypes", [['text/csv'], ['text/html']])
def test_img_invalid(validator, mimetypes):
    with pytest.raises(ValueError, match="Only image files are accepted"):
        validator.img_validation(mimetypes[0])