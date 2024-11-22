import openai
import os
from dotenv import load_dotenv

load_dotenv() #loads env variables
openai.api_key = os.getenv('OpenAi_Api_Key') #open AI key

def TranscribeSpeech(FileName): #speech to text
    File = open(FileName, 'rb')
    Transcribtion = openai.audio.transcriptions.create(model = 'whisper-1', file=File)
    return Transcribtion.text


def interpertText(text): #gpt-3.5 converts text to a prompt
    system_message = "you are an assistant who turn user commands into api requests, Put it in JSON structure" #this prompt is given to GPT almost like background info
    prompt = f"Interpert this user request into an api request:{text}" #almost like the user is giving it this

    #max_tokens is the response length
    #temperature is meassurement of 'randomness' of response
    InterpertedText = openai.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages= [
            {"role":"system","content":system_message},
            {"role":"user","content":prompt}
        ],
        max_tokens = 150,
        temperature = 0.5)
                        
    return InterpertedText.choices[0].message.content