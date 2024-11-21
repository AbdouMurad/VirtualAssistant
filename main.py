from SpeechToText import TranscribeSpeech, interpertText
from recordAudio import Record

if __name__ == "__main__":
    #TranscripeSpeech is function that uses OpenAi api to transcripe audio file using whisper model 

    #uncomment the following line when you want to use it but keep it off on default because it charges per usage
    
    Record()
    print(interpertText(TranscribeSpeech('Recorded.wav'))) 
    
    pass  
  