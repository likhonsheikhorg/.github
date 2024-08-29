import requests
import re

# Define the Gravatar profile URL
profile_url = 'https://api.gravatar.com/v3/profiles/likhondotxyz'
response = requests.get(profile_url)
data = response.json()

# Extract relevant data
avatar_url = data.get('avatar_url')
display_name = data.get('display_name')
location = data.get('location')
description = data.get('description')
job_title = data.get('job_title')
company = data.get('company')
github_url = next((v['url'] for v in data.get('verified_accounts', []) if v['service_type'] == 'github'), None)
twitter_url = next((v['url'] for v in data.get('verified_accounts', []) if v['service_type'] == 'twitter'), None)

# Read the existing README.md
with open('profile/README.md', 'r') as file:
    readme_content = file.read()

# Replace placeholders with actual data
readme_content = readme_content.replace('{{location}}', location or 'Not specified')
readme_content = readme_content.replace('{{job_title}}', job_title or 'Not specified')
readme_content = readme_content.replace('{{company}}', company or 'Not specified')
readme_content = readme_content.replace('{{display_name}}', display_name or 'Not specified')

# Write updated content back to README.md
with open('profile/README.md', 'w') as file:
    file.write(readme_content)
