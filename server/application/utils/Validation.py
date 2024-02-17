import re

class Validation:
    def check_criterias(self, criteria, input):
        for criteria in criteria:
            if not re.match(criteria['regex'], input):
                raise AssertionError(criteria['error'])
            
    # Check if all required fields are present in the JSON data
    def validate_fields(self, required_fields, body):

        def recursive_items(dictionary):
            for key, value in dictionary.items():
                if type(value) is dict:
                    yield (key, value)
                    yield from recursive_items(value)
                else:
                    yield (key, value)

        all_fields = []
        for key, value in recursive_items(body):
            all_fields.append(key)

        for field in required_fields:
            if field not in all_fields:
                raise AssertionError(f'Missing {field} in the request JSON.')
            
    def password_validation(self, password):
        password_criteria = [
            {
                "error": "Password must have at least 8 characters",
                "regex": ".{8,}"
            },
            {
                "error": "Password must have at least one uppercase letter",
                "regex": "(?=.*[A-Z])"
            },
            {
                "error": "Password must have at least one lowercase letter",
                "regex": "(?=.*[a-z])"
            },
            {
                "error": "Password must have at least one digit",
                "regex": "(?=.*\\d)"
            },
            {
                "error": "No whitespace allowed",
                "regex": "(?!.*\\s)"
            }
        ]
        self.check_criterias(password_criteria, password)
            
    def email_validation(self, email):
        email_criteria = [
            {
                "error": "Invalid email format",
                "regex": r"^[\w\.-]+@[\w\.-]+\.\w+$"
            }
        ]
        self.check_criterias(email_criteria, email)

    def name_validation(self, name):
        name_criteria = [
            {
                "error": "Name must be 2 or more characters and can only contain alphanumerical characters",
                "regex": r"^\w{2,}$"
            }
        ]
        self.check_criterias(name_criteria, name)

    def int_validation(self, variable):
        criteria = [
            {
                "error": "Variable must be an integer",
                "regex": "^[-+]?[0-9]+$"
            }
        ]
        if variable == None:
            return True
        self.check_criterias(criteria, str(variable))

    def float_validation(self, variable):
        criteria = [
            {
                "error": "Variable must be a float",
                "regex": r"^[-+]?[0-9]*\.?[0-9]+$"
            }
        ]
        if variable == None:
            return True
        self.check_criterias(criteria, str(variable))

    def positive_validation(self, variable):
        criteria = [
            {
                "error": "Variable must be a positive number",
                "regex": "^[+]?([0-9]*[.])?[0-9]+$"
            }
        ]
        if variable == None:
            return True
        self.check_criterias(criteria, str(variable))

    def negative_validation(self, variable):
        criteria = [
            {
                "error": "Variable must be a negative number",
                "regex": "^-([0-9]*[.])?[0-9]+$"
            }
        ]
        if variable == None:
            return True
        self.check_criterias(criteria, str(variable))

    def accepted_words_validation(self, input_word, accepted_words:list):
        if input_word == None:
            return True
        elif input_word not in accepted_words:
            raise AssertionError(f"Only {', '.join(accepted_words)} are accepted")
        
    def img_validation(self, file_mimetype):
        if file_mimetype.split('/')[0] != 'image':
            raise ValueError(f"Only image files are accepted")