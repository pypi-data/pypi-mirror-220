import os
import shutil
import glob
import base64
import urllib
import requests

from cgc.utils.config_utils import get_config_path
from cgc.utils.config_utils import save_to_config
from cgc.utils.config_utils import read_from_cfg
from cgc.utils.cryptography import rsa_crypto
from cgc.utils import prepare_headers
from cgc.utils.consts.env_consts import API_URL, TMP_DIR

from cgc.utils.requests_helper import call_api, EndpointTypes
from cgc.utils.response_utils import retrieve_and_validate_response_send_metric

TMP_DIR_PATH = os.path.join(get_config_path(), TMP_DIR)


def _get_jwt_from_server() -> str:
    """Function to get JWT token and api key for user

    :param username: _description_
    :type username: str
    :param password: _description_
    :type password: str
    """
    user_id = urllib.parse.quote(read_from_cfg("user_id"))
    password = urllib.parse.quote(read_from_cfg("password"))
    url = f"{API_URL}/v1/api/user/create/token"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    metric = "auth.jwt"
    __payload = f"grant_type=&username={user_id}&password={password}"
    __res = call_api(
        request=EndpointTypes.post,
        url=url,
        headers=headers,
        data=__payload,
    )
    return retrieve_and_validate_response_send_metric(__res, metric)


def get_jwt() -> str:
    json_data = _get_jwt_from_server()
    return json_data["access_token"]


def auth_create_api_key_with_save():
    """Function to create API key and API secret for user and save it to config file."""
    url = f"{API_URL}/v1/api/user/create/api-key"
    headers = prepare_headers.prepare_headers_api_key()
    metric = "auth.api-key"
    __res = call_api(
        request=EndpointTypes.post,
        url=url,
        headers=headers,
    )

    json_data = retrieve_and_validate_response_send_metric(__res, metric)
    api_key = json_data["details"].get("_id")
    secret = json_data["details"].get("secret")
    save_to_config(api_key=api_key, api_secret=secret)


def save_and_unzip_file(res: requests.Response) -> str:
    """Function to save file, unzip it and return path to its directory.

    :param res: API response with file to save and unzip
    :type res: requests.Response
    :return: path to the directory containing the file
    :rtype: str
    """
    zip_file = res.headers.get("content-disposition").split('"')[1]
    namespace = zip_file.split("---")[-1].split(".")[0]

    if not os.path.isdir(TMP_DIR_PATH):
        os.makedirs(TMP_DIR_PATH)
    zip_file_path = f"{TMP_DIR_PATH}/{zip_file}"
    with open(zip_file_path, "wb") as f:
        f.write(res.content)

    unzip_dir = zip_file_path[:-4]
    shutil.unpack_archive(zip_file_path, unzip_dir)

    return unzip_dir, namespace


def get_aes_key_and_password(unzip_dir: str, priv_key_bytes: bytes):
    """Function to get AES key and password from the unzipped file.

    :param unzip_dir: path to the directory containing the file
    :type unzip_dir: str
    :param priv_key_bytes: private key bytes
    :type priv_key_bytes: bytes
    :return: AES key and password
    :rtype: str, str
    """
    encrypted_password_path = ""
    encrypted_aes_path = ""
    for file in glob.glob(
        f"{unzip_dir}/**/*encrypted*",
        recursive=True,
    ):
        if file.endswith("priv"):
            encrypted_aes_path = f"{file}"
        elif file.endswith("password"):
            encrypted_password_path = f"{file}"

    rsa_key = rsa_crypto.import_create_RSAKey(priv_key_bytes)

    with open(encrypted_aes_path, "rb") as aes, open(
        encrypted_password_path, "rb"
    ) as pwd:
        aes_key = rsa_crypto.decrypt_rsa(aes.read(), rsa_key).decode("ascii")
        password = base64.b64decode(rsa_crypto.decrypt_rsa(pwd.read(), rsa_key)).decode(
            "utf-8"
        )

    return aes_key, password
