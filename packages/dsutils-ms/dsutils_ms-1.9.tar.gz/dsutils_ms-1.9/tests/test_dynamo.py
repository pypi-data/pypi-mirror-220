from unittest import TestCase

from dsutils_ms.adapters.dynamo import DynamoDB
from dsutils_ms.helpers.env import get_credential


class TestDynamoDB(TestCase):
    def test_dynamo_describe(self):
        aws_region = get_credential("AWS_DYNAMO_ACCESS").split(":")[0]
        access_key = get_credential("AWS_DYNAMO_ACCESS").split(":")[1]
        secret_key = get_credential("AWS_DYNAMO_ACCESS").split(":")[2]

        db_test = DynamoDB(
            aws_region=aws_region,
            access_key=access_key,
            secret_key=secret_key,
            table_name="dev_pytest",
        )

        self.assertEqual(isinstance(db_test.describe(), dict), True)

    def test_dynamo_load(self):
        aws_region = get_credential("AWS_DYNAMO_ACCESS").split(":")[0]
        access_key = get_credential("AWS_DYNAMO_ACCESS").split(":")[1]
        secret_key = get_credential("AWS_DYNAMO_ACCESS").split(":")[2]

        db_test = DynamoDB(
            aws_region=aws_region,
            access_key=access_key,
            secret_key=secret_key,
            table_name="dev_pytest",
        )

        data = [
            {
                "variety_id": "3",
                "aerial_web_blight": ["MR"],
                "anthracnosis": ["R"],
                "asian_soybean_rust": ["S"],
                "cercospora_blight": ["MR", "MS"],
                "country": "Paraguay",
                "crop": "Soybean",
                "fertility_requirement": "3",
                "lodging_resistance": "4",
                "powdery_mildew": ["MR"],
                "septoria_leaf_spot": ["R", "S"],
                "target_spot": ["MR", "S"],
                "variety": "TEC 6029 IPRO",
                "white_mold": ["S"],
            }
        ]

        status = db_test.save(data)

        self.assertEqual(status, True)
