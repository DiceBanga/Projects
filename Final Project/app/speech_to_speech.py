"""
Performs speech recognition, translation, and text-to-speech functionality.

This function uses the speech_recognition, deep_translator, and gTTS libraries to:
1. Capture audio input from the microphone.
2. Transcribe the audio to text using Google Speech Recognition.
3. Translate the transcribed text from the detected source language to the specified target language.
4. Generate audio output in the target language from the translated text using Google Text-to-Speech.

Args:
    target_language (str): The target language for translation and text-to-speech. Must be one of the supported languages in the `target_languages` dictionary.

Returns:
    str: A string indicating the success or failure of the process.
"""

# Import necessary libraries
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os

# Define the target languages and their corresponding language codes
target_languages = {
    'english': 'en',
    'spanish': 'es',
    'french': 'fr',
    'german': 'de',
    'italian': 'it',
}

# Function to perform speech-to-speech functionality
def speech_to_speech(target_language):
    # Speech Recognition
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Speak now...")
            audio = recognizer.listen(source, timeout=10)  # Stop after 10 seconds of silence
        except sr.WaitTimeoutError:
            print("No speech detected within the timeout period")
            raise

    
    try:
        transcribed_text = recognizer.recognize_google(audio)
        print(f"Transcribed: {transcribed_text}")
    except sr.UnknownValueError:
        return "Speech recognition could not understand audio"
    
    # Translation
    translator = GoogleTranslator(source='auto', target='es')
    translated_text = translator.translate(transcribed_text)
    print(f"Translated: {translated_text}")
    
    # Text-to-Speech
    tts = gTTS(text=translated_text, lang=target_language)
    tts.save("output.mp3")

    # Play the audio
    audio = AudioSegment.from_file("output.mp3", format="mp3")
    play(audio)
    
    return "Process completed successfully"

# Run the function
if __name__ == "__main__":
    i = 1
    #  List available target languages
    print(f"Target languages:")
    print("-" * 30)
    for language in target_languages.keys():
        print(f"{i}. {language.title()}")
        i += 1

    print("-" * 30)

    try:
        # Get user input for target language
        target_language = input(f"Enter the target language: ")
        if target_language.lower() not in target_languages:
            raise ValueError("Invalid target language")
        result = speech_to_speech(target_language='es')
        print(result)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")