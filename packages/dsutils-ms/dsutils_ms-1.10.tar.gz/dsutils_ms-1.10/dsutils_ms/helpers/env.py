from os import getenv
import json
from dsutils_ms.helpers.log import log_title

def get_credential(key: str) -> str:
    data = getenv(key)

    if data is None:
        raise Exception(f"Environment variable {key} not found")

    JSON_CREDENTIALS = ["GOOGLE_SERVICE_ACCOUNT"]
    if key in JSON_CREDENTIALS:
        data = data.replace("\\\\n", "\\n")
        data = json.loads(data)

    return data
