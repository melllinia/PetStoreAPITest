import requests

pet_body_template = {
    "id": 222,
    "category": {
        "id": 0,
        "name": "string"
    },
    "name": "doggieMMM",
    "photoUrls": [
        "string"
    ],
    "tags": [
        {
            "id": 0,
            "name": "string"
        }
    ],
    "status": "available"
}


def get_pet_id(pet_id):
    assert isinstance(pet_id, int), "The ID must be an Integer"
    response = requests.get(f"https://petstore.swagger.io/v2/pet/{pet_id}")
    assert response.status_code in (200, 404), f"Unexpected status code: {response.status_code}"
    return response


def post_pet(pet_body):
    get_res = requests.get(f"https://petstore.swagger.io/v2/pet/{pet_body['id']}")
    response = requests.post("https://petstore.swagger.io/v2/pet", json=pet_body)

    # The pet with given ID doesn't exist
    if get_res.status_code == 404:
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        assert response.json()["id"] == pet_body['id'], "The pet ID in the response does not match the input"

    # The pet with given ID exists
    elif get_res.status_code == 200:
        assert response.status_code != 200, "Expected the POST request to fail since the pet already exists"


def run_tests(test_cases):
    test_id_to_pet_id = {
        1: 1,
        2: 5000,
        3: 2.5,
        4: 555,
        5: 222
    }

    for test_id in test_cases:
        print(f"Running test with test ID: {test_id}")

        pet_id = test_id_to_pet_id.get(test_id, test_id)
        pet_body = pet_body_template.copy()
        pet_body['id'] = pet_id

        if test_id in (1, 2, 3):
            try:
                get_pet_id(pet_id)
                print(f"Test with test ID {test_id} (pet ID {pet_id}) passed.")
            except AssertionError as e:
                print(f"Test with test ID {test_id} (pet ID {pet_id}) failed: {e}")

        elif test_id in (4, 5):
            try:
                post_pet(pet_body)
                print(f"Test with test ID {test_id} (pet ID {pet_id}) passed.")
            except AssertionError as e:
                print(f"Test with test ID {test_id} (pet ID {pet_id}) failed: {e}")


# Define your test cases
test_cases = [1, 2, 3, 4, 5]
run_tests(test_cases)
