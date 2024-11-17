import json
import os
import sys
import time
import keyboard
import winsound
import pyaudio
import wave
from pydub import AudioSegment
from pathlib import Path
from openai import OpenAI
from colorama import Fore, Back
from colorama import init

init()


def VariableInitialization():
    global OAI_key
    global speak
    global now
    global prev
    global characters
    global conversation
    global history_conversation

    try:
        with open("config.json", "r") as json_file:
            data = json.load(json_file)
        OAI_key = data["api"][0]["OAI_key"]
    
    except FileNotFoundError:
        print(Fore.RED + "config.json file not found.")
        exit()

    conversation = []
    history_conversation = {"history": conversation}

    now = ""
    prev = ""

    speak = False
    characters = 0


def message_with_history():
    global conversation
    global history_conversation

    message = [{"role": "system", "content": "Below is the conversation history.\n"}]

    try:
        with open("conversation.json", "r") as json_file:
            data = json.load(json_file)
            conversation = data.get("history", [])
    
    except FileNotFoundError:
        print(Fore.RED + "conversation.json file not found.")
    
    for msg in history_conversation["history"][:-1]:
        message.append(msg)

    if history_conversation:
        message.append({"role": "system", "content": "This is the last message.\n"})
        message.append(history_conversation["history"][-1])
    
    return message


def record_mic():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    OUTPUT_FILENAME = "record.wav"
    audio = pyaudio.PyAudio()
    audio_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    f = []

    message_printed = False

    while not keyboard.is_pressed("tab"):
        pass

    if not message_printed:
        print(Fore.CYAN + "\nTab key detected, starting recording.")
        message_printed = True

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
    global now
    global prev
    client = OpenAI(api_key=OAI_key)
    try:
        with open("record.wav", "rb") as file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=file,
                response_format="text"
            )

        now = transcription
        print(Back.WHITE + Fore.BLACK + "\n> " + now)
        print(Back.BLACK)

    except Exception as e:
        print(e)
        return

    time.sleep(1)

    if speak == False and now != prev:
        conversation.append({"role": "user", "content": now})
        prev = now

    responce = text_generator()
    print(Back.WHITE + Fore.BLACK + responce)
    print(Back.BLACK)

    OAI_TTS(responce)

    time.sleep(1)


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
            print(Fore.RED + "Error in OAI_TTS: No speech file found or file is empty.")

    except Exception as e:
        print(Fore.RED + "Error in OAI_TTS: " + str(e))


def text_generator():
    global conversation
    global history_conversation
    global characters

    characters = sum(len(d['content']) for d in conversation)

    while characters > 2000:
        try:
            conversation.pop(2)
            characters = sum(len(d['content']) for d in conversation)
        except Exception as e:
            print("Error in popping older messages: " + str(e))

    with open("conversation.json", "w", encoding="utf-8") as json_file:
        json.dump(history_conversation, json_file, indent=4)

    history_and_speech = message_with_history()

    client = OpenAI(api_key=OAI_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "This is how a girl responded in a conversation with the user, like they are talking in a voice chat. She would respond in a friendly manner. She would talk about the message and would elaborate on it."
            },
            {
                "role": "user",
                "content": f"\n{history_and_speech}\n"
            }
        ]
    )

    try:
        response_text = completion.choices[0].message.content

        response_text_for_history = (f"you responded: {response_text}")
        conversation.append({"role": "assistant", "content": response_text_for_history})
        history_conversation["history"] = conversation

        with open("conversation.json", "w", encoding="utf-8") as f:
            json.dump(history_conversation, f, indent=4)

        return response_text

    except Exception as e:
        print(e)


def main():
    VariableInitialization()
    print(Fore.BLUE + "Initilization complete.\n")
    print(Fore.GREEN + "Hold 'tab' to record. Release it to stop.")

    try:
        while True:
            if keyboard.is_pressed("tab"):
                record_mic()

            time.sleep(1)

    except KeyboardInterrupt:
        print(Fore.RED + "Program terminated by user.")
        sys.exit()


if __name__ == "__main__": 
    main()
