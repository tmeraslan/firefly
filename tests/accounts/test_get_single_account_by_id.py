import unittest
import requests
import uuid

from tests.firefly_credentials import get_firefly_credentials


TOKEN = get_firefly_credentials()["token"]
BASE_URL = get_firefly_credentials()["base_url"]
# HEADERS = {
#     "Authorization": f"Bearer {TOKEN}",
#     "Accept": "application/vnd.api+json",
#     "X-Trace-Id": str(uuid.uuid4())
# }
HEADERS = {
    "Authorization": f"Bearer {os.getenv('FIREFLY_PERSONAL_TOKEN')}",
    "Accept": "application/json",
    "Content-Type": "application/json",
}


class TestGetSingleAccount(unittest.TestCase):

    def create_temp_account(self, name=None):
        """Create a temporary account and return its ID."""
        account_name = name or f"Temp Account {uuid.uuid4()}"
        payload = {
            "name": account_name,
            "type": "asset",
            "account_role": "defaultAsset",
            "currency_id": "1"
        }
        response = requests.post(f"{BASE_URL}/api/v1/accounts", headers=HEADERS, json=payload)
        self.assertEqual(response.status_code, 200, msg=f"Failed to create account: {response.text}")
        return response.json()["data"]["id"]

    def delete_account(self, account_id):
        """Delete account by ID."""
        requests.delete(f"{BASE_URL}/api/v1/accounts/{account_id}", headers=HEADERS)

    def test_get_existing_account(self):
        account_id = self.create_temp_account()

        try:
            response = requests.get(f"{BASE_URL}/api/v1/accounts/{account_id}", headers=HEADERS)
            self.assertEqual(response.status_code, 200, msg=response.text)
            data = response.json()
            self.assertIn("data", data)
            self.assertEqual(data["data"]["id"], account_id)
            self.assertEqual(data["data"]["type"], "accounts")
        finally:
            self.delete_account(account_id)

    def test_get_nonexistent_account(self):
        account_id = "999999"  # Non-existent ID
        response = requests.get(f"{BASE_URL}/api/v1/accounts/{account_id}", headers=HEADERS)
        self.assertEqual(response.status_code, 404, msg=response.text)
        data = response.json()
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Resource not found")


if __name__ == "__main__":
    unittest.main()
