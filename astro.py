import requests
import json

# Your API key from Astrometry.net
api_key = 'Enter_API_KEY'

# Authenticate using the API key (if not already authenticated)
login_url = 'http://nova.astrometry.net/api/login'
login_data = {'request-json': json.dumps({"apikey": api_key})}

response = requests.post(login_url, data=login_data)

# Check if login was successful
if response.status_code == 200:
    print("Login successful.")
else:
    print("Login failed.")
    exit()  # Exit if login fails

# URL for retrieving your submissions
submissions_url = 'https://nova.astrometry.net/api/submissions'

# URL for adding submissions to the album
add_to_album_url = 'https://nova.astrometry.net/api/albums/FOV13_JALNA_IMAGES/add'

# Parameters for the API request to get submissions
params = {'request-json': json.dumps({"apikey": api_key})}

# Album ID of the existing album where you want to move the images
album_id = 'FOV13_JALNA_IMAGES'  # Replace with your existing album ID

# Retrieve submissions
submissions_response = requests.get(submissions_url, params=params)
print(submissions_response.text)

# Check if submissions retrieval was successful
if submissions_response.status_code == 200:
    submissions_data = submissions_response.json()
    print(submissions_response.text)
    if submissions_data.get('status') == 'success':
        submissions = submissions_data.get('submissions')
        if submissions:
            submission_ids = [submission.get('id') for submission in submissions]

            # Add submissions to the album
            add_to_album_data = {
                'request-json': json.dumps({"apikey": api_key, "sub_ids": submission_ids})
            }
            add_to_album_response = requests.post(add_to_album_url.format(album_id=album_id),
                                                  data=add_to_album_data)

            # Check if adding submissions to the album was successful
            if add_to_album_response.status_code == 200:
                add_to_album_json = add_to_album_response.json()
                if add_to_album_json.get('status') == 'success':
                    print("Submissions moved to the album successfully.")
                else:
                    print("Failed to move submissions to the album.")
                    print(add_to_album_json.get('message'))
            else:
                print("Failed to move submissions to the album.")
                print(add_to_album_response.text)
        else:
            print("No submissions found.")
    else:
        print("Failed to retrieve submissions.")
        print(submissions_data.get('message'))
else:
    print(f"Failed to retrieve submissions. Status code: {submissions_response.status_code}")
