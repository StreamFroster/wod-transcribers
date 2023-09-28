import requests 
import json
import time

# replace with your API token
YOUR_API_TOKEN = "111f93b614d648e5a5c984dd3b8b04b9"

# URL of the file to transcribe
FILE_URL = "https://www.buzzsprout.com/1826458/13456157-2nd-anniversary.mp3?client_source=buzzsprout_site&download=true"

# AssemblyAI transcript endpoint (where we submit the file)
transcript_endpoint = "https://api.assemblyai.com/v2/transcript"

# request parameters where Speaker Diarization has been enabled
data = {"audio_url": FILE_URL, "speaker_labels": True, "speakers_expected": 3}

# HTTP request headers
headers = {
    "Authorization": "111f93b614d648e5a5c984dd3b8b04b9",
    "Content-Type": "application/json"
}

# submit for transcription via HTTP request
response = requests.post(transcript_endpoint, json=data, headers=headers)

# polling for transcription completion
polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{response.json()['id']}"

while True:
    transcription_result = requests.get(polling_endpoint, headers=headers).json()

    if transcription_result['status'] == 'completed':
        # Write the results to a JSON file
        with open("transcription_result.json", "w") as json_file:
            json.dump(transcription_result, json_file, indent=2)
        break
    elif transcription_result['status'] == 'error':
        raise RuntimeError(
            f"Transcription failed: {transcription_result['error']}")
    else:
        time.sleep(3)
