import openai
import os
from dotenv import load_dotenv

def TranscribeSpeech(FileName):
    load_dotenv() #loads env variables
    openai.api_key = os.getenv('OpenAi_Api_Key') #open AI key

    File = open(FileName, 'rb')

    Transcribtion = openai.audio.transcriptions.create(model = 'whisper-1', file=File)
    return Transcribtion.text