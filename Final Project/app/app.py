"""
The Flask web application provides a translation service that allows users to translate text between supported languages. It also includes functionality for speech-to-text and text-to-speech conversion.

The main features of the application include:

- Translating text between supported languages (English, Spanish, French, German, Italian)
- Converting speech to text using Google Speech Recognition
- Converting text to speech using Google Text-to-Speech

The application uses the following third-party libraries:
- Flask: A lightweight web framework for Python
- speech_recognition: A library for performing speech recognition with various engines and APIs
- deep_translator: A library for translating text between languages
- gTTS: A library for generating speech from text using the Google Text-to-Speech API

The application defines the following routes:
- `/`: The main route that handles text translation
- `/speech-to-text`: A route that accepts an audio file and converts it to text
- `/translate-text`: A route that accepts text and a target language and returns the translated text
- `/text-to-speech`: A route that accepts text and a target language and returns an audio file of the text-to-speech conversion
"""
# Import libraries
import os
import tempfile
import uuid

# Third-party libraries
try:
    from flask import Flask, request, render_template, jsonify, send_file
    import speech_recognition as sr
    from deep_translator import GoogleTranslator
    from gtts import gTTS
except ImportError:
    print("Error: Required libraries are not installed. Please install them using 'pip install -r requirements.txt' command and try again.")
    print("It is recommended to use a virtual environment to avoid conflicts with other projects. To create a virtual environment, run the following command:")
    print("python -m venv venv")
    exit(1)

# Initialize Flask app
app = Flask(__name__)

# Supported languages with their codes
SUPPORTED_LANGUAGES = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it'
}

# Main route for text translation
@app.route('/', methods=['GET', 'POST'])
def translate():
    input_text = ''
    output_text = ''
    target_language = 'English'  # Default language
    error = None

    if request.method == 'POST':
        try:
            input_text = request.form['input_text']
            target_language = request.form.get('target_language', 'English')
            
            if not target_language or target_language not in SUPPORTED_LANGUAGES:
                raise ValueError("Invalid target language selected")

            if input_text:
                # Translate the text
                translator = GoogleTranslator(source='auto', target=SUPPORTED_LANGUAGES[target_language])
                output_text = translator.translate(input_text)

        except Exception as e:
            error = f"Translation error: {str(e)}"

    return render_template('app.html', 
                         input_text=input_text, 
                         output_text=output_text, 
                         target_language=target_language,
                         error=error,
                         supported_languages=SUPPORTED_LANGUAGES)

# Route for speech-to-text conversion
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    try:
        # Initialize recognizer
        recognizer = sr.Recognizer()
        
        # Get audio from the request
        audio_file = request.files.get('audio')
        if not audio_file:
            return jsonify({'error': 'No audio file received'}), 400

        # Save audio file temporarily
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, f"audio_{uuid.uuid4()}.wav")
        audio_file.save(temp_path)

        # Convert speech to text
        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        # Clean up
        os.remove(temp_path)

        return jsonify({'text': text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for text-to-speech conversion
@app.route('/translate-text', methods=['POST'])
def translate_text():
    try:
        data = request.get_json()
        text = data.get('text')
        target_language = data.get('target_language')

        if not text or not target_language:
            return jsonify({'error': 'Missing required parameters'}), 400

        translator = GoogleTranslator(source='auto', target=SUPPORTED_LANGUAGES[target_language])
        translated_text = translator.translate(text)
        
        return jsonify({'translated_text': translated_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for text-to-speech conversion
@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()
        text = data.get('text')
        target_language = data.get('target_language')

        if not text or not target_language:
            return jsonify({'error': 'Missing required parameters'}), 400

        # Generate speech
        temp_dir = tempfile.gettempdir()
        output_path = os.path.join(temp_dir, f"tts_{uuid.uuid4()}.mp3")
        
        tts = gTTS(text=text, lang=SUPPORTED_LANGUAGES[target_language])
        tts.save(output_path)

        # Send file and clean up
        response = send_file(output_path, mimetype='audio/mp3')
        
        @response.call_on_close
        def cleanup():
            if os.path.exists(output_path):
                os.remove(output_path)
        
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)