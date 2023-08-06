import os
from logger_local_python_package.LoggerLocal import logger_local
import sys
import dotenv
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..')))
from db.library_db import LibraryDb
dotenv.load_dotenv()


class AccessTokenLibrary:

    def insert_user_external(self, user_name, profile_id, access_token):
        object_start = {
            'user_name': user_name,
            'profile_id': profile_id,
            'access_token': access_token
        }
        logger_local.start(object=object_start)
        insert_user_ext = LibraryDb()
        insert_user_ext.insert_user_access_token(
            user_name, profile_id, access_token)
        logger_local.end(object={})

    def update_user_external(self, profile_id, access_token):
        object_start = {
            'profile_id': profile_id,
            'access_token': access_token
        }
        logger_local.start(object=object_start)
        insert_user_ext = LibraryDb()
        insert_user_ext.update_by_profile_id(profile_id, access_token)
        logger_local.end(object={})

    def get_access_token(self, profile_id):
        object_start = {
            'profile_id': profile_id
        }
        logger_local.start(object=object_start)
        insert_user_ext = LibraryDb()
        res = insert_user_ext.select_by_profile_id(profile_id)
        logger_local.end(object={'access_token': res})
        return res

    def get_access_token_by_user_name(self, user_name):
        object_start = {
            'user_name': user_name
        }
        logger_local.start(object=object_start)
        insert_user_ext = LibraryDb()
        res = insert_user_ext.get(user_name)
        logger_local.end(object={'access_token': res})
        return res

    def delete_access_token_by_profile_id(self, profile_id):
        object_start = {
            'profile_id': profile_id
        }
        logger_local.start(object=object_start)
        insert_user_ext = LibraryDb()
        insert_user_ext.delete_by_profile_id(profile_id)
        logger_local.end(object={})

    def update_user_external_by_username(self, user_name, access_token):
        object_start = {
            'user_name': user_name,
            'access_token': access_token
        }
        logger_local.start(object=object_start)
        insert_user_ext = LibraryDb()
        insert_user_ext.update_by_user_name(user_name, access_token)
        logger_local.end(object={})
