import unittest
import requests
import uuid
from tests.firefly_credentials import get_firefly_credentials

TOKEN = get_firefly_credentials()["token"]
BASE_URL = get_firefly_credentials()["base_url"]
ACCOUNTS_URL = BASE_URL + "/api/v1/accounts"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

class TestFireflyCreateAccount(unittest.TestCase):

    def get_account_count(self):
        response = requests.get(f"{ACCOUNTS_URL}?limit=999", headers=HEADERS)
        self.assertEqual(response.status_code, 200, "Failed to fetch accounts list")
        return len(response.json().get("data", []))

    def create_account(self, name=None):
        """Creates an account and returns its ID and full response."""
        unique_name = name or f"Test Account {uuid.uuid4()}"
        payload = {
            "name": unique_name,
            "type": "asset",
            "account_role": "defaultAsset",
            "currency_id": "1"
        }
        response = requests.post(ACCOUNTS_URL, headers=HEADERS, json=payload)
        self.assertEqual(response.status_code, 200, f"Account creation failed: {response.text}")
        return response.json()["data"]["id"], response

    def delete_account(self, account_id):
        """Deletes account by ID (ignores if already deleted)."""
        delete_url = f"{ACCOUNTS_URL}/{account_id}"
        requests.delete(delete_url, headers=HEADERS)

    def test_create_account_success(self):
        initial_count = self.get_account_count()
        account_id = None

        try:
            account_id, response = self.create_account()
            data = response.json()
            self.assertIn("data", data)
            self.assertEqual(data["data"]["attributes"]["name"], data["data"]["attributes"]["name"])

            final_count = self.get_account_count()
            self.assertEqual(final_count, initial_count + 1,
                             f"Expected {initial_count + 1} accounts but got {final_count}")
        finally:
            if account_id:
                self.delete_account(account_id)

    def test_create_account_missing_required_field(self):
        incomplete_payload = {"type": "asset"}
        response = requests.post(ACCOUNTS_URL, headers=HEADERS, json=incomplete_payload)
        self.assertEqual(response.status_code, 422, f"Unexpected status: {response.status_code}")
        json_data = response.json()
        self.assertIn("message", json_data)
        self.assertIn("errors", json_data)
        self.assertIn("name", json_data["errors"])

    def test_duplicate_account_name(self):
        account_id = None
        try:
            unique_name = f"Duplicate Account {uuid.uuid4()}"
            account_id, first_response = self.create_account(name=unique_name)
            second_response = requests.post(ACCOUNTS_URL, headers=HEADERS, json={
                "name": unique_name,
                "type": "asset",
                "account_role": "defaultAsset",
                "currency_id": "1"
            })

            self.assertEqual(first_response.status_code, 200, f"First request failed: {first_response.text}")
            self.assertEqual(second_response.status_code, 422, f"Second request failed: {second_response.text}")
        finally:
            if account_id:
                self.delete_account(account_id)


if __name__ == "__main__":
    unittest.main()
