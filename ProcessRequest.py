import openai
import os
from dotenv import load_dotenv
import json
import Google

from fuzzywuzzy import process

load_dotenv() #loads env variables
openai.api_key = os.getenv('OpenAi_Api_Key') #open AI key


def TranscribeSpeech(FileName): #speech to text
    File = open(FileName, 'rb')
    Transcribtion = openai.audio.transcriptions.create(model = 'whisper-1', file=File)
    return Transcribtion.text

class InterpertTextObject:
    def __init__(self):
        self.functions = "send_email create_calander_event create_contact function_does_not_exist generate_response"
        self.FunctionsDict = {
            "send_email":self.send_email,
            "create_event":self.create_event,
            "create_contact":self.create_contact,
            "generate_response":self.generate_response,
        }

        self.system_message_text_to_funcitons = f"you are assistant.name is Nova.look at user input decide function from:{self.functions}.respond with function name only seperated by spaced"
        self.prompt_text_to_functions = f"Decide function or to generate text:"

        self.system_message_email = "you are assistant.your name is Nova.fill in info for email api request in following order:(name)-(subject)-(text).Create json format.if info not given leave blank"
        self.prompt_email = "create api request from the following user command:"

        self.system_message_add_contact ="you are assistant.your name is Nova.fill in info for add contact api request in following order:(name)-(email).Create json format.if info not given leave blank"
        self.prompt_add_contact = "create api request from the following user command:"

        self.system_message_generate_response = "you are assistant.name is Nova.respond to user text with conversational text"
        self.prompt_generate_response = "you are assistant.name is benti.respond to user input:"

        self.system_message_generate_response_postfunction = "user text is list of functions you completed. create message saying you completed those functions"
        self.prompt_generate_response_postfunction = "respond to user input confirming tasks complete:"


    def processFunctions(self,functions, text):
        response = ""
        for function in functions.split():
            if function in self.FunctionsDict.keys():
                response += self.FunctionsDict[function](text)
        return self.generate_response_postfunction(text)

    def send_email(self,text):
        services = Google.authenticate_google_api()
        emailService = services[0]
        contactSerive = services[1]
        
        api_request = self.interpertText(text,self.system_message_email,self.prompt_email)
        data = json.loads(api_request)
        contacts = Google.list_google_contacts(contactSerive)
        
        match = process.extractOne(data["name"],list(contacts.keys()))
        name = match[0] if match else data["name"] #selects the closest name otherwise default name given
        try:
            print(f"send email to: {name}(y/n)")
            if input() == "y":
                Google.send_email_gmail(emailService, contacts[name],data["subject"],data["text"])
                return(f"email to {name} about {data["subject"]} ---")
            else:
                print("canceled")
        except Exception as e:
            print(e)

    def create_contact(self,text):
        service = Google.authenticate_google_api()[1]
        api_request = self.interpertText(text,self.system_message_add_contact,self.prompt_add_contact)
        data = json.loads(api_request)
        print(data)
        Google.add_contact(service,data["name"],data["email"])
        return (f"contact made for {data["name"]}")

    def get_contacts(self):
        service = Google.authenticate_google_api()[1]
        Google.list_google_contacts(service)


    def create_event(self,text):
        print("EVENT")

    def generate_response(self,text):
        response = self.interpertText(text,self.system_message_generate_response,self.prompt_generate_response)
        print(response)

    def generate_response_postfunction(self,text):
        response = self.interpertText(text,self.system_message_generate_response_postfunction,self.prompt_generate_response_postfunction)
        return response



    def interpertText(self,text,system_message,prompt): #gpt-3.5 converts text to a prompt
        #system message - pre prompt to gpt - instructions on what to do with prompt
        #prompt - user input

        prompt += text

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
    
