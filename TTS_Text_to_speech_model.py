
import os
import subprocess
import platform
import time
from playsound import playsound
#from pydub.playback import play
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs
ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')

#from gtts import gTTS

def text_to_speech_with_gtts(input_text):
    language="en"
    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    output_filepath = f"AI_VOICE_OUTPUT/ai_voice_{int(time.time())}.mp3"
    audioobj.save(output_filepath)
    return output_filepath

input_text ='Isaac Newton is the greatest scientist in the world'
#text_to_speech_with_gtts(input_text,'gtts_testing_samuel.mp3')

def text_to_speech_elevenlabs(input_text):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice ='Aria',
        output_format="mp3_22050_32",
        model = "eleven_turbo_v2"
    )
    output_filepath = f"AI_VOICE_OUTPUT/ai_voice_{int(time.time())}.mp3"
    # if os.path.exists(output_filepath):
    #     os.remove(output_filepath)
    elevenlabs.save(audio,output_filepath)
    print('Audio saved successfully')
    return output_filepath

    



#text_to_speech_elevenlabs(input_text,'elevenlabs_testing5_Autoplay.mp3')