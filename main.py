from ProcessRequest import TranscribeSpeech, InterpertTextObject, initializeTree
from Audio import Record,Speak



def main():
    Speak("Hello my name is Nova, how can I help you today?")
    TextProcessor = InterpertTextObject()
    while True:      
        Record()
        
        initializeTree()
        TextProcessor = InterpertTextObject()

        UserText = TranscribeSpeech("Recorded.wav")
        FunctionRequest = TextProcessor.interpertText(UserText,TextProcessor.system_message_text_to_funcitons,TextProcessor.prompt_text_to_functions)
        TextProcessor.splitFunctions(FunctionRequest)
if __name__ == "__main__":

    main()                            
                    