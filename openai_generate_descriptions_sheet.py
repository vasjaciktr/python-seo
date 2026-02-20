import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai
import time
import os
import csv

# Define the scope for Google Sheets API access
scope = [
    "https://www.googleapis.com/auth/spreadsheets",  # Read and write access to Sheets
    "https://www.googleapis.com/auth/drive"  # Access to Drive files if needed
]

# Authenticate using the service account JSON key file
creds = ServiceAccountCredentials.from_json_keyfile_name(
    r'c:\Users\Vasyl\Desktop\ChatGPT Google Sheets\europafoodxb-450709-9eb45dda71fa.json', scope)
clientDrive = gspread.authorize(creds)

# Open the Google Sheet by name
sheet = clientDrive.open("ChatGPTapi").sheet1

# Fetch all prompts from the first column
prompts = sheet.col_values(1)

# Set up the OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY2")

def get_response(prompt):
    for attempt in range(3):  # Retry 3 times in case of errors
        try:
            response = openai.ChatCompletion.create(
                model="gpt-5.1",  # Specify the model
                messages=[
                    {"role": "system", "content": "You are a high-qualified writer that specializes in the grocery industry and grocery products."},
                    {"role": "user", "content": prompt}
                ]
            )
            # Access the content correctly
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error {e}")
            time.sleep(2)  # Wait before retrying
    return "Error: Failed to get response after 3 attempts"

# Process prompts and collect responses
responses = []
for prompt in prompts:
    response = get_response(prompt)
    responses.append(response)
    time.sleep(1)  # To avoid hitting rate limits for OpenAI API, adjust as needed

print(response)

# Update Google Sheet in batches
try:
    batch_size = 10  # Number of rows to update in one batch
    for i in range(0, len(responses), batch_size):
        batch_range = f"B{i + 1}:B{i + batch_size}"
        batch_data = [[response] for response in responses[i:i + batch_size]]
        sheet.update(batch_range, batch_data)
        print(f"Batch {i // batch_size + 1} updated.")
        time.sleep(5)  # Adjust the delay between batches if needed
    print("All requests processed and written to the Google Sheet.")
except Exception as e:
    print(f"Failed to update Google Sheet: {e}")
    # Write the responses to a CSV file as a backup
    backup_filename = "responses_backup.csv"
    with open(backup_filename, mode='w', newline='', encoding='utf-8') as backup_file:
        writer = csv.writer(backup_file)
        writer.writerow(['Prompt', 'Response'])  # Header
        for prompt, response in zip(prompts, responses):
            writer.writerow([prompt, response])
    print(f"Backup saved to {backup_filename}.")
