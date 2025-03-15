import os
import logging


from pydub import AudioSegment #pydub couldnt able to recognize ffmpeg so we hv to directly mention its path
AudioSegment.converter = r"C:\Users\arsam\ffmpeg\bin\ffmpeg.exe"

import speech_recognition as sr
from io import BytesIO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

#Step1: Setup Audio recorder (ffmpeg & portaudio)
# ffmpeg, portaudio, pyaudio
def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.

    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_lfimit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    
    return file_path
#record_audio('test8.mp3')
#audio_filepath ="test8.mp3"


from groq import Groq

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
client_groq = Groq(api_key = GROQ_API_KEY)

def transcribe_with_groq(audio_filepath):
    #client = Groq(api_key = GROQ_API_KEY)
    audio_file =open(audio_filepath,'rb')
    transcription = client_groq.audio.transcriptions.create(
        model='whisper-large-v3',
        file = audio_file,
        language='en'
    )

    return transcription.text




    
