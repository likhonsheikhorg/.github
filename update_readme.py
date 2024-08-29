import requests
import json
import os
from pathlib import Path

def fetch_gravatar_data(profile_url):
    try:
        response = requests.get(profile_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data from Gravatar: {e}")
        return None

def extract_profile_data(data):
    if not data:
        return {}
    
    return {
        'avatar_url': data.get('avatar_url', ''),
        'display_name': data.get('display_name', 'Not specified'),
        'location': data.get('location', 'Not specified'),
        'description': data.get('description', ''),
        'job_title': data.get('job_title', 'Not specified'),
        'company': data.get('company', 'Not specified'),
        'github_url': next((v['url'] for v in data.get('verified_accounts', []) if v['service_type'] == 'github'), ''),
        'twitter_url': next((v['url'] for v in data.get('verified_accounts', []) if v['service_type'] == 'twitter'), '')
    }

def update_readme(profile_data, readme_path):
    try:
        with open(readme_path, 'r') as file:
            content = file.read()
        
        for key, value in profile_data.items():
            placeholder = f'{{{{{key}}}}}'
            content = content.replace(placeholder, value)
        
        with open(readme_path, 'w') as file:
            file.write(content)
        print(f"README updated successfully at {readme_path}")
    except IOError as e:
        print(f"Error updating README: {e}")

def main():
    profile_url = 'https://api.gravatar.com/v3/profiles/likhondotxyz'
    readme_path = Path('profile/README.md')

    # Ensure the profile directory exists
    readme_path.parent.mkdir(parents=True, exist_ok=True)

    data = fetch_gravatar_data(profile_url)
    if data:
        profile_data = extract_profile_data(data)
        update_readme(profile_data, readme_path)
    else:
        print("Failed to update README due to data fetching error.")

if __name__ == "__main__":
    main()
