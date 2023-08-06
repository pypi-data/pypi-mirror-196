import pure_checker

def test_pure_error_code():
    assert pure_checker.pure_error_code(5) == "PURE_E_ZIP_BOMB_ARCHIVES"

def test_pure_error_string():
    assert pure_checker.pure_error_string(5) == "zip bomb: too many archives"