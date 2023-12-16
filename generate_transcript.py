import json

# Ask the user for the file to process

targetFile = str(input("Provide the path of the file that contains the API response data that you want to process: "))
print("Looking for file " + targetFile)

# Load the JSON response from the API
with open(targetFile, "r") as json_file:
    transcription_result = json.load(json_file)

# Extract the "words" array from the JSON
words = transcription_result.get("words", [])

# Create a list to store alternating speaker lines with timestamps
alternating_lines = []

# Initialize variables for alternating lines
current_speaker = None
current_line = ""
current_start_time = None

# Speaker mapping
speaker_mapping = {
    "A": "Rei",
    "B": "Bantam",
    "C": "Dillitan"
}

# Function to convert milliseconds to hours, minutes, and seconds
def ms_to_hms(milliseconds):
    seconds = milliseconds / 1000
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

# Iterate through the words and build alternating lines with timestamps in hours, minutes, and seconds
for word in words:
    speaker = word.get("speaker", "Unknown")
    text = word.get("text", "")
    start_time_ms = word.get("start", None)

    # Convert milliseconds to hours, minutes, and seconds
    start_time_hms = ms_to_hms(start_time_ms) if start_time_ms is not None else None
    
    if current_speaker is None:
        current_speaker = speaker
    
    if speaker == current_speaker:
        current_line += " " + text
    else:
        if current_start_time is not None:
            alternating_lines.append((current_speaker, start_time_hms, current_line.strip()))
        current_speaker = speaker
        current_line = text
        current_start_time = start_time_hms

# Add the last alternating line
if current_start_time is not None:
    alternating_lines.append((current_speaker, current_start_time, current_line.strip()))

outputFile = str(input("Provide the name for the output file: "))
destinationTargetFile = "transcriptions/" + outputFile + ".txt"

print(destinationTargetFile)

f = open(destinationTargetFile, "x")
f.close()

# Write alternating lines with timestamps in hours, minutes, and seconds to a text file
with open(destinationTargetFile, "w") as txt_file:
    for speaker, start_time_hms, line in alternating_lines:
        speaker_name = speaker_mapping.get(speaker, "Unknown")
        txt_file.write(f"{speaker_name} ({start_time_hms}): {line}\n\n")
