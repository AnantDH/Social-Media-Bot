# Social Media Bot

This project is an automated social media content generator that creates videos by combining audio, text, and visuals. It can automatically generate videos based on parameters and assets provided via a Google Drive link. It also utilizes various APIs for converting text to speech, generating subtitles, and filtering content. While the bot is currently an interactive terminal application, it is highly versatile and customizable.

## Table of Contents
- [About the Project](#about-the-project)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)

## About the Project
The Social Media Bot automates video creation by:
- Generating videos using text, audio, and visuals.
- Fetching visuals from a Google Drive link.
- Converting text to speech using TTS (Text-to-Speech).
- Adding automatically generated subtitles to videos.
- Performing profanity filtering and determining the gender of the text input using OpenAI’s API.

## Features
- **Automatic Video Generation**: Uses JSON2Video API and Google Drive assets to create videos.
- **Text-to-Speech**: Converts text into speech using Elevenlabs and Google TTS APIs.
- **Subtitle Generation**: Auto-generates subtitles for the videos.
- **Reddit Story Integration**: Fetches stories automatically from Reddit for use in videos.
- **Profanity Filtering**: Utilizes OpenAI API to filter inappropriate content.
- **Gender Determination**: Uses OpenAI API to infer the gender of the story writer if text input is provided.
- **Interactive Terminal Bot**: Currently, the bot is operated through an interactive command-line interface.

## Technologies Used
- **Programming Language**: Python
- **APIs**:
  - [JSON2Video API](https://json2video.com/)
  - [Elevenlabs](https://elevenlabs.io/)
  - [Google Drive API](https://developers.google.com/drive)
  - [Google TTS API](https://cloud.google.com/text-to-speech)
  - [YouTube API](https://developers.google.com/youtube/)
  - [Reddit API](https://www.reddit.com/dev/api/)
  - [OpenAI API](https://openai.com/api/)
- **Other Services**: Google Drive, YouTube

## Getting Started
To set up the project locally, follow these steps.

### Prerequisites
- Python 3.x installed
- Google API credentials for Drive, TTS, and YouTube
- API keys for JSON2Video, Elevenlabs, Reddit, and OpenAI
- `pip` for Python package installations

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/AnantDH/Social-Media-Bot.git
2. Navigate to project directory:
   ```bash
   cd Social-Media-Bot
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
4. Set up the required API keys and credentials in a .env file or configure them within the script as needed.

### Usage
1. Run the script in the terminal:
   ```bash
   python program.py
2. Follow the interactive prompts to provide necessary video generation components
3. Wait for generation to occurr, then access the file when prompted

### Contact
- Email: anantd@uw.edu
- GitHub: [AnantDH](https://github.com/AnantDH)


