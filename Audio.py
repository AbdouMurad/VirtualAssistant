import pyaudio
import keyboard
import time
import wave
from gtts import gTTS
import io
import pygame


def Speak(text):
    tts = gTTS(text=text, lang="en", slow=False)
    
    # Create a BytesIO object to hold the speech data in memory
    fp = io.BytesIO()  # Instantiate BytesIO correctly
    tts.write_to_fp(fp)  # Write the speech directly to the BytesIO object
    fp.seek(0)  # Reset the pointer to the beginning of the BytesIO object
    
    # Initialize pygame mixer (for audio playback)
    pygame.mixer.init()
    
    # Load the audio from the BytesIO object
    pygame.mixer.music.load(fp)
    
    # Play the audio
    pygame.mixer.music.play()

    # Wait for the sound to finish before exiting
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
def Record():
    chunk = 1024
    format = pyaudio.paInt16
    channels = 2
    rate = 44100
    Output_Filename = "Recorded.wav"
    
    p = pyaudio.PyAudio() 

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    frames = []
    print("Press SPACE to start recording")
    keyboard.wait('space')
    print("Recording... Press SPACE to stop.")
    time.sleep(0.2)

    while True:
        try:
            data = stream.read(chunk)  
            frames.append(data)
        except KeyboardInterrupt:
            break
        if keyboard.is_pressed('space'):
            print("stopping recording") 
            time.sleep(0.2)
            break   

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(Output_Filename, 'wb')  
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()