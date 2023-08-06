import dotenv
import pytest
import sys
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))

from src.library import AccessTokenLibrary

dotenv.load_dotenv()
insert1 = AccessTokenLibrary()


@pytest.mark.test
def test_getProfiles_returns_name_and_email():
    insert1.insert_user_external("test", 2, "test1")
    token = insert1.get_access_token_by_user_name("test")
    assert token[0] == "test1"


@pytest.mark.test
def test_update_access_token():
    insert1.update_user_external(2, "test2")
    token = insert1.get_access_token_by_user_name("test")
    assert token[0] == "test2"


@pytest.mark.test
def test_delete_access_token():
    insert1.delete_access_token_by_profile_id(2)
    token = insert1.get_access_token_by_user_name("test")
    assert token is None



