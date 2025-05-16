
#Setup Groq API key
import os
import base64
from groq import Groq


os.environ['KMP_DUPLICATE_LIB_OK']= 'True'

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

#convert image to required format:
#Base64 converts binary image data into a textual format, making it safe to send via HTTP requests in JSON payloads.
#Web protocols and most REST APIs expect data to be encoded in text, not binary.Base64 ensures that image data doesn’t break the structure or expectations of the web request format.

image_path ='acne.jpg'

def encode_image(image_path):
    image_file = open(image_path,'rb')
    return base64.b64encode(image_file.read()).decode('utf-8')




#Multimodal LLM


query = 'Is there anything wrong in face in given image'
client =Groq()
#payload to the model
def analyse_image_with_query(query,encoded_image):

    messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                        },
                    },
                ],
            }]

    chat_completion = client.chat.completions.create(
        messages = messages, model = 'llama-3.2-90b-vision-preview'
    )

    return chat_completion.choices[0].message.content


def process_text_only(query):

    messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": query
                    }
                    
                ]
            }]

    chat_completion = client.chat.completions.create(
        messages = messages, model = 'llama-3.2-90b-vision-preview'
    )

    return chat_completion.choices[0].message.content

