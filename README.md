# Talk-AI

**Talk-AI** is a Python application that integrates speech recognition, natural language processing, and text-to-speech technologies. By holding the `Right Shift` key, user can record their voice, have it transcribed and analyzed, and receive a spoken AI response—all powered by OpenAI's Whisper-1, GPT-4o-mini, and TTS-1 models.

## Features

- **Voice Input**: Record your voice by holding the `Right Shift` key.
- **Speech-to-Text**: Uses OpenAI's Whisper-1 model to transcribe spoken input.
- **AI Response Generation**: Leverages GPT-4o-mini to create an intelligent and context-aware response.
- **Chat History**: Remembers chat history for context-aware responses.
- **Text-to-Speech**: Utilizes OpenAI's TTS-1 model to vocalize the AI's response.
- **UI interface**: Provides an interface (`ui_app.py`).

## Requirements
- **Python**: 3.x
- **API Key**: OpenAI API key
- **FFmpeg**: Required for audio processing
- **Dependencies**: Install via `requirements.txt`

## Installation

1. **Clone the repository** and navigate to the project folder:
    ```bash
    git clone https://github.com/artur3333/Talk-AI.git
    cd Talk-AI
    ```

2. **Install the required Python packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Install FFmpeg**:
   FFmpeg is needed for audio processing. Follow the instructions below based on your operating system:

   - **Ubuntu or Debian-based systems**:
     ```bash
     sudo apt update && sudo apt install ffmpeg
     ```
   - **macOS (using Homebrew)**:
     ```bash
     brew install ffmpeg
     ```
   - **Windows**:
     - Download FFmpeg from [FFmpeg's official site](https://ffmpeg.org/download.html).
     - Unzip the downloaded file, and add the files (ffmpeg.exe and ffprobe.exe) contained in FFmpeg `bin` directory to the project's PATH. 

4. **Configure your OpenAI API key**:
    - Open the `config.json` file in a text editor.
    - Replace `YOUR_OpenAI_KEY` with your actual OpenAI API key as shown below:
      ```json
      {
          "api": [
              {
                  "OAI_key": "YOUR_OpenAI_KEY"
              }
          ]
      }
      ```

## Directory Tree

```plaintext
Talk-AI
├── main.py                 # Main script to run the application
├── ui_app.py               # GUI application
├── config.json             # Configuration file for storing OAI API key
├── conversation.json       # Stores the conversation history used for generating responses
├── conversation_log.txt    # Saves all chat logs and AI responses
├── ui_main.py              # Main script for ui_app.py
├── ffmpeg.exe              # FFmpeg executable for audio processing (Windows)
├── ffprobe.exe             # FFprobe executable for media information (Windows)
├── icon.ico                # The Icon of the ui_app
├── requirements.txt        # List of Python dependencies
└── README.md               # Project readme with usage instructions and details
```

## Usage
### Command Line Interface (CLI)

Open a terminal in the project directory and run main.py

```bash
python main.py
```

### Graphical User Interface (GUI)

Open a terminal in the project directory and run ui_app.py:

```bash
python ui_app.py
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork** the repository.
2. **Create a new branch** for your feature or bug fix.
3. **Make your changes** and test them.
4. **Submit** a pull request describing your changes.
