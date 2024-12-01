import openai
import os
from dotenv import load_dotenv
import json
import Google
from transformers import pipeline
from fuzzywuzzy import process

load_dotenv() #loads env variables
openai.api_key = os.getenv('OpenAi_Api_Key') #open AI key

class DecisionTreeNode:
    def __init__(self, function = None, name = None):
        self.name = name
        self.function = function
        self.children = {}

def initializeTree():
    DecisionTreeDictionary = json.load(open('DecisionTree.json', 'r'))
    root = DecisionTreeNode()
    build_tree(root,DecisionTreeDictionary)

    
    return root

def build_tree(node,dict): #build decision tree
    if dict["children"]:
        for child in dict["children"]:
            new_node = DecisionTreeNode(
                function = dict["children"][child]["function"],
                name = dict["children"][child]["name"]
                )
            node.children[new_node.name] = new_node
            build_tree(new_node,dict["children"][child])



def TranscribeSpeech(FileName): #speech to text
    File = open(FileName, 'rb')
    Transcribtion = openai.audio.transcriptions.create(model = 'whisper-1', file=File)
    return Transcribtion.text

class InterpertTextObject:
    def __init__(self):
        self.rootDecisionTreeRoot = initializeTree()
        self.functions = "send_email create_calander_event create_contact function_does_not_exist generate_response"
        self.FunctionsDict = {
            "send_email":self.send_email,
            "create_event":self.create_event,
            "create_contact":self.create_contact,
            "generate_text":self.generate_text,
            "read_event":self.read_event,
        }
        self.Assitant_name = "Nova"
        self.TimeZone = "America/Edmonton" #Hard coded right now

        self.classifier = pipeline('zero-shot-classification',  model="facebook/bart-large-mnli")

        self.system_message_email = "you are assistant.your name is Nova.fill in info for email api request in following order:(name:persons_name,subject:summary,text:text_to_send).Create json format.if info not given leave blank"
        self.prompt_email = "create api request from the following user command:"

        self.system_message_add_contact ="you are assistant.your name is Nova.fill in info for add contact api request in following order:(name:persons_name,email:persons_email).Create json format.if info not given leave blank"
        self.prompt_add_contact = "create api request from the following user command:"

        self.system_message_generate_response = "you are assistant.name is Nova.respond to user text with conversational text"
        self.prompt_generate_response = "you are assistant.name is Nova.respond to user input:"

        self.system_message_generate_response_postfunction = "user text is list of functions you completed. create message saying you completed those functions"
        self.prompt_generate_response_postfunction = "respond to user input confirming tasks complete:"

        #####UPDATED PROMPTS#######
        self.system_message_text_to_funcitons = f"you are assistant. name is {self.Assitant_name}.classify task into one of:{list(self.rootDecisionTreeRoot.children.keys())} return in json format: (task_name:name, text:simplified_text)"
        self.prompt_text_to_functions = f"respond to user input strictly in the format you were given. if you find multiple tasks create multiple json outputs seperated by star (*)"
        
        self.system_message_add_event = f"user text is request to create event in google calander. fill in info for api request in following json format:(summary:Title,location:location_of_event,description:summary,start:(dateTime:data_time,timeZone:TimeZone),end:(dateTime:data_time,timeZone:Timezone))"
        self.prompt_add_event = f"fill in the api request in jason form. the time zone is {self.TimeZone}. Put date_time in this form: ex. 2024-12-01-T21:00:00 for both start and end. Assume event length is one hour unless specified and whatever else is not given leave empty"

    def splitFunctions(self,functions):
        #UPDATED
        FunctionsToProcess = []
        for Function in functions.split("*"):
            print(Function)
            FunctionsToProcess.append(json.loads(Function))
        
        for Function in FunctionsToProcess:
            self.processFunction(Function,self.rootDecisionTreeRoot.children[Function["task_name"]])
    
    def processFunction(self,function,node):
        print(node.name)
        input_text = function['text']
        if node.function == None:
            labels = list(node.children.keys())
            result = self.classifier(input_text,labels)['labels'][0]
            self.processFunction(function, node.children[result])
        else:
            self.FunctionsDict[node.name](input_text)


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
        print(text)
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
        service = Google.authenticate_google_api()[2]
        api_request = self.interpertText(text,self.system_message_add_event,self.prompt_add_event)
        data = json.loads(api_request)
        
        data["reminders"] = {}
        data["reminders"]["useDefault"] = True
        Google.create_event(service,data)
    
    def read_event(self,text):
        print("EVENT")


    def generate_text(self,text):
        response = self.interpertText(text,self.system_message_generate_response,self.prompt_generate_response)
        print(response)
        #return response

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
    
