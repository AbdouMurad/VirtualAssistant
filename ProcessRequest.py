import openai
import os
from dotenv import load_dotenv

load_dotenv() #loads env variables
openai.api_key = os.getenv('OpenAi_Api_Key') #open AI key

def TranscribeSpeech(FileName): #speech to text
    File = open(FileName, 'rb')
    Transcribtion = openai.audio.transcriptions.create(model = 'whisper-1', file=File)
    return Transcribtion.text


def processFunctions(functions):
    #keep track of functions here

    FunctionsDict = {
        "send_email":send_email,
        "create_event":create_event,
    }


    for function in functions.split():
        if function in FunctionsDict.keys():
            FunctionsDict[function]()

def send_email():
    print("EMAIl")
def create_event():
    print("EVENT")

def interpertText(text): #gpt-3.5 converts text to a prompt
    functions = "send_email create_event generate_text function_does_not_exist"
    system_message = f"you are assistant.look at user input decide function from:{functions}.respond with function name only seperated by space.can decide to generate_text for conversation" #this prompt is given to GPT almost like background info
    prompt = f"Decide function or to generate text:{text}" #almost like the user is giving it this

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
    
    processFunctions(InterpertedText.choices[0].message.content)
    return InterpertedText.choices[0].message.content