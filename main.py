from ProcessRequest import TranscribeSpeech, interpertText
from recordAudio import Record
import Google
     
if __name__ == "__main__":
    #TranscripeSpeech is function that uses OpenAi api to transcripe audio file using whisper model 

    #uncomment the following line when you want to use it but keep it off on default because it charges per usage
        
    service = Google.authenticate_google_api()
  
   
    Record()
    print("GPT RESPONSE:",interpertText(TranscribeSpeech('Recorded.wav'))) 
    pass                                                                            
    