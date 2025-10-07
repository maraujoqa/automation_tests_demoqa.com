import requests
import json
import random
import string


# Function to generate random username

def generate_random_username(length=8):
    return "user_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


# 1. Create a new user
url_create_user = "https://demoqa.com/Account/v1/User"

new_user = {
    "userName": generate_random_username(),
    "password": "Test@1234"  # You can change password rules if needed
}

response_create_user = requests.post(url_create_user, json=new_user)
if response_create_user.status_code == 201:
    user_info = response_create_user.json()
    user_id = user_info['userID']
    print(f"[STEP 1] User created successfully! UserID: {user_id}, Username: {new_user['userName']}")
else:
    print(f"[STEP 1] Failed to create user: {response_create_user.text}")
    exit()

# 2. Generate access token
url_generate_token = "https://demoqa.com/Account/v1/GenerateToken"
payload_token = {
    "userName": new_user['userName'],
    "password": new_user['password']
}

response_token = requests.post(url_generate_token, json=payload_token)
if response_token.status_code == 200:
    token_info = response_token.json()
    access_token = token_info['token']
    print(f"[STEP 2] Access token generated.")
else:
    print(f"[STEP 2] Failed to generate token: {response_token.text}")
    exit()

# 3. Check if the user is authorized (Using POST as per API spec for this endpoint)
url_authorized = "https://demoqa.com/Account/v1/Authorized"

# The /Authorized endpoint expects userName and password in the body
# It returns a simple 'true' or 'false' in plain text, NOT JSON
payload_auth = {
    "userName": new_user['userName'],
    "password": new_user['password']
}

# No need for Authorization header here, only the credentials are required
response_auth = requests.post(url_authorized, json=payload_auth)

# Print status code and raw content for debugging
print(f"[DEBUG] Status code: {response_auth.status_code}")
print(f"[DEBUG] Response text: {response_auth.text}")

# Check the text content directly, as it's not JSON
if response_auth.status_code == 200:
    # The API returns 'true' or 'false' as plain text
    authorized_status = response_auth.text.strip().lower() == 'true'
    print(f"[STEP 3] Is the user authorized? {authorized_status}")
else:
    print(f"[STEP 3] Failed to check authorization status. Response: {response_auth.text}")

# 4. List available books
url_books = "https://demoqa.com/BookStore/v1/Books"

response_books = requests.get(url_books)
if response_books.status_code == 200:
    books_list = response_books.json()['books']
    print(f"[STEP 4] Found {len(books_list)} books available.")
else:
    print(f"[STEP 4] Failed to list books: {response_books.text}")
    exit()

# 5. Rent two random books
url_rent_books = "https://demoqa.com/BookStore/v1/Books"
headers_rent_books = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# Select 2 random books
books_to_rent = random.sample(books_list, 2)
payload_rent_books = {
    "userId": user_id,
    "collectionOfIsbns": [{"isbn": book['isbn']} for book in books_to_rent]
}

response_rent_books = requests.post(url_rent_books, headers=headers_rent_books, json=payload_rent_books)
if response_rent_books.status_code == 201:
    print(f"[STEP 5] Rented books successfully: {[book['title'] for book in books_to_rent]}")
else:
    print(f"[STEP 5] Failed to rent books: {response_rent_books.text}")
    exit()

# 6. Get user details including rented books
url_user_details = f"https://demoqa.com/Account/v1/User/{user_id}"
headers_auth = {"Authorization": f"Bearer {access_token}"}

response_user_details = requests.get(url_user_details, headers=headers_auth)
if response_user_details.status_code == 200:
    user_details = response_user_details.json()
    print(f"[STEP 6] User details including rented books:")
    print(json.dumps(user_details, indent=4))
else:
    print(f"[STEP 6] Failed to fetch user details: {response_user_details.text}")