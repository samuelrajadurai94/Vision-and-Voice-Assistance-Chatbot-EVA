import os
import gradio as gr
import time
import shutil
from playsound import playsound

#from gradio import ChatMessage
from Image_Analysing_Model import encode_image,analyse_image_with_query,process_text_only
from Users_Voice_to_text import record_audio,transcribe_with_groq
from TTS_Text_to_speech_model import text_to_speech_elevenlabs,text_to_speech_with_gtts

system_prompt="""You have to act as a professional doctor. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them.
            Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

system_prompt2 = '''If No Image provided for u , You have to give response for the text given . 
            you have to act as good doctor.
            Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""'''


i=1
def save_input_audio(mic_audio):
    if not mic_audio:
        return None   
    # Generate a unique filename using timestamp
    input_audio_save_path = f"USER_INPUT_VOICE/recorded_audio_{int(time.time())}.wav"    
    # Copy the recorded file to the saved location
    shutil.copy(mic_audio, input_audio_save_path)   
    return input_audio_save_path

def process_inputs(audio_filepath, text_input, image_filepath, chat_history):
    global i
    i+=1
    transcript=''
    if audio_filepath:

        transcript = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
                
    user_message = transcript if transcript else text_input
    
    if image_filepath:
        reply = analyse_image_with_query(
            query=system_prompt + user_message,
            encoded_image=encode_image(image_filepath),
            model="llama-3.2-11b-vision-preview"
        )
    else:
        reply = process_text_only(
            query=system_prompt2 + user_message,
            model="llama-3.2-11b-vision-preview"
        )  # Function to generate LLM response
    

    #voice_reply = text_to_speech_elevenlabs(input_text=reply)
    voice_reply = text_to_speech_with_gtts(reply)
    if audio_filepath:
        globals()[f'voice_reply_{i}']=audio_filepath     
        chat_history.append({"role": "user", "content": gr.Audio(globals()[f'voice_reply_{i}'])})
        i+=1
    chat_history.append({"role": "user", "content": user_message})
    if image_filepath:
        chat_history.append({"role": "user", "content":gr.File(image_filepath)})
    
    globals()[f'voice_reply_{i}']=voice_reply

    chat_history.append({"role": "assistant", "content": gr.Audio(globals()[f'voice_reply_{i}'])})

    chat_history.append({"role": "assistant", "content": reply})
    
    return chat_history,globals()[f'voice_reply_{i}'], None, "", None



# Define Gradio UI
def chatbot_ui():
    global i
    with gr.Blocks(css="""
        /* Chat Interface Styling */
        .chatbot-container {
            background-color: #E0F7FA; /* Dark Background */
            border-radius: 10px;
            padding: 15px;
            color: #101010; /* White text */
            font-family: 'Arial', sans-serif;
            overflow-y: auto;
            max-height: 400px;
        }
        
              
        .user-message {
            background-color: #3E8ACC; /* Blue for User */
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            color: #101010;
            text-align: right;
        }
        .ai-message {
            background-color: #5C5CFF; /* Purple for AI */
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
            color: #101010;
            text-align: left;
        }
        .audio-box {background-color: #FFDDC1; padding: 10px;min-height: 100px; border-radius: 10px;
                    max-height: 200px;overflow: auto;}
        .text-box {background-color: #D1E8E2; padding: 10px; height: 100px;border-radius: 10px;}
        .image-box {background-color: #F9C5D1; padding: 10px; height: 100px;border-radius: 10px;
                    overflow: auto;}
        
        .send-btn {
            background-color: #4CAF50 !important;  /* Green background */
            color: white !important;              /* White text */
            font-size: 16px !important;            /* Adjust text size */
            border-radius: 8px !important;         /* Rounded corners */
            padding: 10px 20px !important;         /* Adjust padding */
            border: none !important;
            cursor: pointer;
        }

        .send-btn:hover {
            transform: scale(1.05);
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
            border: 2px solid #ffffff;
            transition: all 0.3s ease-in-out;
        }
    
    """) as demo:
        gr.Markdown('<div align="center"><h1><strong>VOICE AND VISION ASSISTANCE CHATBOT - EVA</strong></h1></div>')
        chat_history = gr.Chatbot(type = 'messages',elem_classes="chatbot-container",
                                  show_label=True,
                                  avatar_images=('man1.png','eva2_cropped1.jpg'))
        
        with gr.Row():
                audio_input = gr.Audio(sources=["microphone"], type="filepath", label="🎙️ Speak", elem_classes="audio-box",min_width=1)
                text_input = gr.Textbox(placeholder="Type a message...", label="💬 Text Input", elem_classes="text-box")

                image_input = gr.File(type="filepath", label="📷 Upload Image", elem_classes="image-box",min_width=1)

        send_button = gr.Button("Send",elem_classes="send-btn")
        voice_output = gr.Audio(label="🔊 AI Response Voice",interactive=False,visible=False,autoplay=True)

        send_button.click(
            process_inputs,
            inputs=[audio_input, text_input, image_input, chat_history],
            outputs=[chat_history,voice_output,audio_input, text_input, image_input]
    
        )

    return demo

chatbot_ui().launch(debug=True)