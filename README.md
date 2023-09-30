# wod-transcribers
The transcribing project for the World of Dragons podcast. We aim to create a transcript for every World of Dragons podcast episode!

## Why?

If you're looking for a certain topic or quote that the podcast hosts have said, this will make it a lot easier than having you relisten through hours of content. It would also make for a good dataset should one wants to perform analysis on the podcast easily (number of times a word has been said, most unique word, amount of curse words, etc.)

~~This project also allows me to improve my python skills along with giving me a good reason to dive into audio-related ML stuff, so why not?~~

## Contributions

This project is widely open for contributions! Found a bug? Want to write actual cleaner code for the project? Send pull requests our way!

## AssemblyAI API Token

You'll need to register with AssemblyAI and acquire an API token. Once you have one create a new `config.py` file like so:

```py
API_TOKEN = "YOUR_API_TOKEN"
```

 The python script will automatically fetch your API token provided that you put it in the same directory.

## How to use:

> Note: Make sure you have done the above steps first or your code *will* fail.

1. Obtain a download link from any provider
> It **has** to be a download link, not the link to the page of the episode.

2. Run the `main.py` script and paste the link
> AssemblyAI handles most of the voice-to-text and speaker diarization part

3. A new JSON file with the raw response data will be saved in `./transcriptions/wip/`

4. Run the `process_api_data.py` and it will create a new `.txt` file using the data from the JSON file
> File is created in `./transcriptions/wip/`

5. A human editor goes through the generated `.txt` file to check for errors
> Additionally add [Indicators] like [Laughter] or [Sighs] as it is not included in the response data 

6. Once complete, finished transcript should moved to `./transcriptions/`

## Buzzsprout link
https://worldofdragons.buzzsprout.com/

Buzzsprout is the ideal provider to get download links for episodes.