from ProcessRequest import TranscribeSpeech, InterpertTextObject, initializeTree
from Audio import Record,Speak
from Memory import log_data


def main():
    first_text = True

    Speak("Hello my name is Nova, how can I help you today?")
    TextProcessor = InterpertTextObject()
    while True:      
        Record()
        
        initializeTree()
        TextProcessor = InterpertTextObject()

        UserText = TranscribeSpeech("Recorded.wav")
        SystemText = "Hello"  # Sample text for now

        # Logs user and system inputs into memory_log.txt
        log_data("User", UserText, first_text)
        log_data("System", SystemText, first_text)

        FunctionRequest = TextProcessor.interpertText(UserText,TextProcessor.system_message_text_to_funcitons,TextProcessor.prompt_text_to_functions)
        TextProcessor.splitFunctions(FunctionRequest)

        first_text = False
if __name__ == "__main__":
    main()                            
                    