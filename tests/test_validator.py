from validator import Validator, validate, rules as R


def test_validator_001_simple():
    request = {"age": 23}
    rule = {"age": [R.Min(18)]}
    result = Validator(request, rule).validate()
    assert result

    request = {"age": 13}
    rule = {"age": [R.Min(18)]}
    result = Validator(request, rule).validate()
    assert not result

    request = {"age": 13}
    rule = {"age": [R.Max(18)]}
    result = Validator(request, rule).validate()
    assert result

    request = {"name": "Jon"}
    rule = {"name": [R.Required()]}
    result = Validator(request, rule).validate()
    assert result

    request = {"name": ""}
    rule = {"name": [R.Required()]}
    result = Validator(request, rule).validate()
    assert not result


def test_validate_002_simple():
    request = {"age": 23}
    rule = {"age": [R.Min(18)]}
    result = validate(request, rule)
    assert result

    request = {"age": 13}
    rule = {"age": [R.Min(18)]}
    result = validate(request, rule)
    assert not result

    request = {"age": 13}
    rule = {"age": [R.Max(18)]}
    result = validate(request, rule)
    assert result

    request = {"name": "Jon"}
    rule = {"name": [R.Required()]}
    result = validate(request, rule)
    assert result

    request = {"name": ""}
    rule = {"name": [R.Required()]}
    result = validate(request, rule)
    assert not result


def test_validator_003_simple():
    request = {"age": 23}
    rule = {"age": [R.Min(18), R.Max(30)]}
    result = Validator(request, rule).validate()
    assert result

    request = {"age": 33}
    rule = {"age": [R.Min(18), R.Max(30)]}
    result = Validator(request, rule).validate()
    assert not result

    request = {"age": 23, "name": "Jon"}
    rule = {"age": [R.Min(18)], "name": [R.Required()]}
    result = Validator(request, rule).validate()
    assert result

    request = {"age": 23, "name": ""}
    rule = {"age": [R.Min(18), R.Max(30)], "name": [R.Required()]}
    result = Validator(request, rule).validate()
    assert not result


def test_validate_004_simple():
    request = {"age": 23}
    rule = {"age": [R.Min(18), R.Max(30)]}
    result = validate(request, rule)
    assert result

    request = {"age": 33}
    rule = {"age": [R.Min(18), R.Max(30)]}
    result = validate(request, rule)
    assert not result

    request = {"age": 23, "name": "Jon"}
    rule = {"age": [R.Min(18)], "name": [R.Required()]}
    result = validate(request, rule)
    assert result

    request = {"age": 23, "name": ""}
    rule = {"age": [R.Min(18), R.Max(30)], "name": [R.Required()]}
    result = validate(request, rule)
    assert not result


def test_validator_005_error_msg():
    request = {"age": 100}
    rule = {"age": [R.Between(18, 90)]}
    val = Validator(request, rule)
    result = val.validate()
    errors = val.get_error_messages()
    assert not result
    assert "age" in errors.keys()
    assert "Between" in errors["age"].keys()

    request = {"age": 28, "name": "John", "surname": "Krasinski"}
    rule = {
        "age": [R.Between(18, 50)],
        "name": [R.Required()],
        "surname": [R.Required(), R.Mail()],
    }
    val = Validator(request, rule)
    result = val.validate()
    errors = val.get_error_messages()

    # Test General
    assert not result
    assert len(errors) == 1
    assert "surname" in errors.keys()

    # Test Error 1
    mail_err = errors["surname"]
    assert len(mail_err) == 1
    assert "Mail" in mail_err.keys()


def test_validator_006_error_msg():
    request = {"age": 100}
    rule = {"age": [R.Between(18, 90)]}
    result, errors = validate(request, rule, return_errors=True)
    assert not result
    assert "age" in errors.keys()
    assert "Between" in errors["age"].keys()

    request = {"age": 28, "name": "John", "surname": "Krasinski"}
    rule = {
        "age": [R.Between(18, 50)],
        "name": [R.Required()],
        "surname": [R.Required(), R.Mail()],
    }
    result, errors = validate(request, rule, return_errors=True)

    # Test General
    assert not result
    assert len(errors) == 1
    assert "surname" in errors.keys()

    # Test Error 1
    mail_err = errors["surname"]
    assert len(mail_err) == 1
    assert "Mail" in mail_err.keys()


def test_validator_007_error_msg():
    request = {
        "age": 53,
        "name": "Peter",
        "surname": "Griffin",
        "profession": "",
        "mail": "petergriffin.com",
    }
    rule = {
        "age": [R.Between(18, 50), R.Required()],
        "name": [R.Required()],
        "surname": [R.Required()],
        "profession": [R.Required, R.Mail],
        "mail": [R.Required(), R.Mail()],
    }
    val = Validator(request, rule)
    result = val.validate()
    errors = val.get_error_messages()

    # Test General
    assert not result
    assert len(errors) == 3
    assert "age" in errors
    assert "profession" in errors
    assert "mail" in errors

    # Test Error 1
    age_err = errors["age"]
    assert len(age_err) == 1
    assert "Between" in age_err

    # Test Error 2
    profession_err = errors["profession"]
    assert len(profession_err) == 2
    assert "Required" in profession_err
    assert "Mail" in profession_err

    # Test Error 3
    mail_err = errors["mail"]
    assert len(mail_err) == 1
    assert "Mail" in mail_err


def test_validator_008_error_msg():
    request = {
        "age": 53,
        "name": "Peter",
        "surname": "Griffin",
        "profession": "",
        "mail": "petergriffin.com",
    }
    rule = {
        "age": [R.Between(18, 50), R.Required()],
        "name": [R.Required()],
        "surname": [R.Required()],
        "profession": [R.Required, R.Mail],
        "mail": [R.Required(), R.Mail()],
    }
    result, errors = validate(request, rule, return_errors=True)

    # Test General
    assert not result
    assert len(errors) == 3
    assert "age" in errors
    assert "profession" in errors
    assert "mail" in errors

    # Test Error 1
    age_err = errors["age"]
    assert len(age_err) == 1
    assert "Between" in age_err

    # Test Error 2
    profession_err = errors["profession"]
    assert len(profession_err) == 2
    assert "Required" in profession_err
    assert "Mail" in profession_err

    # Test Error 3
    mail_err = errors["mail"]
    assert len(mail_err) == 1
    assert "Mail" in mail_err
