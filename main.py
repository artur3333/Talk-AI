import json
import os
import keyboard
import winsound
import pyaudio
import wave
from pydub import AudioSegment
from pathlib import Path
from openai import OpenAI


def VariableInitialization():
    global OAI_key
    global speak

    try:
        with open("config.json", "r") as json_file:
            data = json.load(json_file)
        OAI_key = data["api"][0]["OAI_key"]
    
    except FileNotFoundError:
        print("config.json file not found.")
        exit()

    speak = False


def record_mic():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    OUTPUT_FILENAME = "record.wav"
    audio = pyaudio.PyAudio()
    audio_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    f = []

    while not keyboard.is_pressed("tab"):
        pass
    while keyboard.is_pressed("tab"):
        data = audio_stream.read(CHUNK)
        f.append(data)
    
    audio_stream.stop_stream()
    audio_stream.close()
    audio.terminate()
    file = wave.open(OUTPUT_FILENAME, 'wb')
    file.setsampwidth(audio.get_sample_size(FORMAT))
    file.setnchannels(CHANNELS)
    file.setframerate(RATE)
    file.writeframes(b''.join(f))
    file.close()
    speech_to_text("record.wav")


def speech_to_text(file):
    client = OpenAI(api_key=OAI_key)
    try:
        with open("record.wav", "rb") as file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=file,
                response_format="text"
            )

        print("> " + transcription)

    except Exception as e:
        print(e)
        return
    
    speech = ("Human said" + transcription)
    text_generator(speech)


def OAI_TTS(message):
    global speak
    client = OpenAI(api_key=OAI_key)
    speech_file_path = Path(__file__).parent / "speech.mp3"
    wav_file_path = Path(__file__).parent / "speech.wav"

    try:
        response = client.audio.speech.create(
            model = "tts-1",
            voice = "nova",
            input = message
        )
        with open(speech_file_path, "wb") as file:
            for chunk in response.iter_bytes():
                file.write(chunk)

        if speech_file_path.exists() and os.path.getsize(speech_file_path) > 0:
            audio = AudioSegment.from_mp3(speech_file_path)
            audio.export(wav_file_path, format="wav")

            # Play the audio
            speak = True
            winsound.PlaySound(wav_file_path, winsound.SND_FILENAME)
            speak = False

        else:
            print("Error in OAI_TTS: No speech file found or file is empty.")

    except Exception as e:
        print("Error in OAI_TTS: " + str(e))


def text_generator(speech):
    client = OpenAI(api_key=OAI_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "max_tokens": 32,
                "content": "This is how a girl responded in a conversation. She would respond in a friendly manner. She would talk about the message and would elaborate on it."
            },
            {
                "role": "user",
                "content": f"\n{speech}\n"
            }
        ]
    )

    try:
        response_text = completion.choices[0].message.content
        OAI_TTS(response_text)
    except Exception as e:
        print(e)


def main():
    VariableInitialization()
    print("Started")
    message_printed = False
    while True:
        if not message_printed:
            print("Hold 'tab' to record. Release it to stop.")
            message_printed = True

        if keyboard.is_pressed("tab"):
            print("Tab key detected, starting recording.")
            record_mic()


if __name__ == "__main__": 
    main()
