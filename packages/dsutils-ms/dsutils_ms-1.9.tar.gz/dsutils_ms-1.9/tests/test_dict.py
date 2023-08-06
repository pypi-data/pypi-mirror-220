from unittest import TestCase

from dsutils_ms.helpers.dict import flatten_dict


class TestDict(TestCase):
    def test_flatten_dict(self):
        data = {
            "name": "John Doe",
            "age": 30,
            "address": {
                "street": "123 Main St",
                "city": "New York",
                "state": "NY",
            },
            "hobbies": ["reading", "coding", "hiking"],
        }

        result = {
            "name": "John Doe",
            "age": 30,
            "address.street": "123 Main St",
            "address.city": "New York",
            "address.state": "NY",
            "hobbies[0]": "reading",
            "hobbies[1]": "coding",
            "hobbies[2]": "hiking",
        }

        flatten_data = flatten_dict(data)

        self.assertEqual(flatten_data, result)
