import re
from datetime import datetime

def validate_data_type(data, expected_type):
    if not isinstance(data, expected_type):
        print(f"Data type validation failed. Expected {expected_type.__name__}, but got {type(data).__name__}.")
        return False
    return True

def validate_range(data, min_value=None, max_value=None):
    if min_value is not None and data < min_value:
        print(f"Numeric range validation failed. Value should be greater than or equal to {min_value}.")
        return False
    if max_value is not None and data > max_value:
        print(f"Numeric range validation failed. Value should be less than or equal to {max_value}.")
        return False
    return True

def validate_string_length(data, min_length=None, max_length=None):
    if max_length is not None and len(data) > max_length:
        print(f"String length validation failed. String length should be at most {max_length} characters.")
        return False
    if min_length is not None and len(data) < min_length:
        print(f"String length validation failed. String length should be at least {min_length} characters.")
        return False
    return True

def validate_not_null(data):
    if data is None:
        print("Not-null validation failed. Value cannot be null.")
        return False
    return True

def validate_pattern(data, pattern):
    if not re.match(pattern, data):
        print("Pattern validation failed. Value does not match the specified pattern.")
        return False
    return True

def validate_email(email):
    # Using a simple regex pattern for basic email validation
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        print("Email validation failed. Invalid email format.")
        return False
    return True

def validate_password(password, require_special_char=False):
    if require_special_char:
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    else:
        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$"

    if not re.match(password_pattern, password):
        raise ValueError("Invalid password format.")
    else:
        print("Password validation passed successfully.")

def validate_date(date, date_format='YYYY/MM/DD'):
   
    date_format = date_format.replace('YYYY', '%Y').replace('MM', '%m').replace('DD', '%d')
    try:
        datetime.strptime(date, date_format)
        print("Date validation passed successfully.")
        return True
    except ValueError:
        print(f"Invalid date format. Expected format: {date_format}.")
        return False

def validate_url(url):
    # Using a regex pattern for basic URL validation
    url_pattern = r"^(https?://)?(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$"
    if not re.match(url_pattern, url):
        print("URL validation failed. Invalid URL format.")
        return False
    return True

def validate_with_custom_rule(data, custom_rule_func):
    if not custom_rule_func(data):
        print("Custom rule validation failed. Data does not satisfy the custom validation rule.")
        return False
    return True

def validate_data(data, data_type=None, min_value=None, max_value=None, max_length=None, min_length=None, not_null=False, pattern=None, custom_rule_func=None):
    try:
        is_valid = True

        if data_type:
            is_valid &= validate_data_type(data, data_type)
        if isinstance(data, (int, float)):
            is_valid &= validate_range(data, min_value, max_value)
        if isinstance(data, str):
            is_valid &= validate_string_length(data, max_length, min_length)
        if not_null:
            is_valid &= validate_not_null(data)
        if pattern:
            is_valid &= validate_pattern(data, pattern)
        if custom_rule_func:
            is_valid &= validate_with_custom_rule(data, custom_rule_func)

        return is_valid

    except ValueError as e:
        print(f"Validation error: {str(e)}")
        return False
