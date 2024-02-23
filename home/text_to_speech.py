import os
import io
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play


class TTS: 
    
    def __init__(self):
            
        # Load environment variables from .env file
        load_dotenv()

        # Set your OpenAI GPT-3 API key
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)

    def generate_and_play_audio(self, voice, model, input_text):
        try:
            response = self.client.audio.speech.create(
                model=model,
                voice=voice,
                input=input_text
            )

            # Convert the response content to an AudioSegment
            audio_segment = AudioSegment.from_mp3(io.BytesIO(response.content))

            # Play the audio
            play(audio_segment)

        except Exception as e:
            print(f"An error occurred: {e}")

    def select_voice_model(self):
        voice_options = {"1": "nova", "2": "echo", "3": "fable", "4": "onyx", "5": "shimmer"}
        model_options = {"1": "tts-1", "2": "tts-1-hd"}

        # Voice selection
        print("Select Voice:")
        for key, value in voice_options.items():
            print(f"{key}: {value}")

        selected_voice_key = input("Enter the number corresponding to the desired voice: ")
        selected_voice = voice_options.get(selected_voice_key)

        # Model selection
        print("Select Model:")
        for key, value in model_options.items():
            print(f"{key}: {value}")

        selected_model_key = input("Enter the number corresponding to the desired model: ")
        selected_model = model_options.get(selected_model_key)

        return selected_voice, selected_model





    def ask_question_and_play(self, selected_voice, selected_model,text_from_prompt):
        # Ask a question
        input_text = text_from_prompt
        print(text_from_prompt)
        print("please wait you audio is generating please check you internet !")
        
        self.generate_and_play_audio(selected_voice, selected_model, input_text)
        
        return True
    
    

