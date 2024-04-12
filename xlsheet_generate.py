import requests
import pandas as pd

def fetch_survey_responses(api_token):
    url = "https://data.g2.com/api/v1/survey-responses"
    headers = {
        "Authorization": f"Token token={api_token}",
        "Content-Type": "application/vnd.api+json"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        survey_responses = response.json()
        return survey_responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching survey responses: {e}")
        return None

api_token = "e3673b695738435827b8a487bc289295f6cf0ea568ba450e620275fe8037ccae"
survey_responses = fetch_survey_responses(api_token)

if survey_responses:
    
    df = pd.json_normalize(survey_responses['data'])

    excel_filename = "survey_responses.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"Survey responses saved to {excel_filename}")
else:
    print("Failed to fetch survey responses.")
