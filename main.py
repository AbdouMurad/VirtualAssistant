from ProcessRequest import TranscribeSpeech, InterpertTextObject, initializeTree
import Audio
from Memory import log_data

def main():
    first_text = True
    AudioDevice = Audio.AudioDevice()
    AudioDevice.Speak("Hello my name is Nova, how can I help you today?")
    TextProcessor = InterpertTextObject()
    while True:      
        AudioDevice.Record()
        initializeTree()
        UserText = TranscribeSpeech("Recorded.wav")

        FunctionRequest = TextProcessor.interpertText(UserText,TextProcessor.system_message_text_to_funcitons,TextProcessor.prompt_text_to_functions)
        SystemResponse = TextProcessor.splitFunctions(FunctionRequest)
        AudioDevice.Speak(SystemResponse)

        # Logs user and system inputs into memory_log.txt
        log_data("User", UserText, first_text)
        log_data("System", SystemResponse, first_text)
        first_text = False
if __name__ == "__main__":
    main()                         
                    