import requests 
import json
import time
import config
import os
from datetime import datetime

# Check if the API_TOKEN exists in the config module
if hasattr(config, 'API_TOKEN'):
    API_TOKEN = config.API_TOKEN
    print("API Token loaded!")
else:
    print("Error: API Token not found in the config module.")

# URL of the file to transcribe
FILE_URL = str(input("Enter the download link of the episode to be transcribed: "))

# AssemblyAI transcript endpoint (where we submit the file)
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

# request parameters where Speaker Diarization has been enabled
data = {"audio_url": FILE_URL, "speaker_labels": True, "speakers_expected": 3}

# HTTP request headers
headers = {
    "Authorization": config.API_TOKEN,
    "Content-Type": "application/json"
}

# Submit for transcription via HTTP request
response = requests.post(transcript_endpoint, json=data, headers=headers)

# Check if the request was successful
if response.status_code != 200:
    raise RuntimeError(f"Transcription request failed with status code {response.status_code}")

# Get the transcript ID from the response
transcript_id = response.json()['id']
print(f"Transcription request submitted with ID: {transcript_id}")

# Polling for transcription completion
polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

while True:
    transcription_result = requests.get(polling_endpoint, headers=headers).json()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if transcription_result['status'] == 'completed':
        # Extract the file name from the URL
        file_name = os.path.basename(FILE_URL)
        
        # Create the output file name with "_transcription" appended
        output_file_name = "./transcriptions/wip/" + os.path.splitext(file_name)[0] + "_transcription.json"
        
        # Write the results to the output file
        with open(output_file_name, "w") as json_file:
            json.dump(transcription_result, json_file, indent=2)
        
        print(f"[{current_time}] Transcription completed. Results saved to '{output_file_name}'")
        break
    elif transcription_result['status'] == 'failed':
        raise RuntimeError(f"[{current_time}] Transcription failed: {transcription_result['error']}")
    else:
        print(f"[{current_time}] Transcription status: {transcription_result['status']}")
        time.sleep(5)