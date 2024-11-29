from ProcessRequest import TranscribeSpeech, InterpertTextObject
from Audio import Record,Speak


def main():
    Speak("Hello my name is Nova, how can I help you today?")
    while True:      
        Record()
        
        TextProcessor = InterpertTextObject()
        
        UserText = TranscribeSpeech("Recorded.wav") #text as speech  
        
        FunctionsRequest = TextProcessor.interpertText(UserText,TextProcessor.system_message_text_to_funcitons,TextProcessor.prompt_text_to_functions)   
        

        SystemText = TextProcessor.processFunctions(FunctionsRequest,UserText)

        if FunctionsRequest == "generate_text":
            pass 
        Speak(SystemText)
if __name__ == "__main__":
    main()                            
                    