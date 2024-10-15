
def transcription(youtube_link, transcription_name):
    import os
    import tempfile
    import whisper
    from pytubefix import YouTube
    import streamlit as st

    
    # Check if the transcription file with that name already exists
    if os.path.exists(transcription_name + ".txt"):
        return "Transcription file already exists. Remove it first"

    # Get the YouTube video
    youtube = YouTube(youtube_link)
    audio = youtube.streams.filter(only_audio=True).first()

    # Load the Whisper model
    whisper_model = whisper.load_model("base")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Download the audio
        file = audio.download(output_path=tmpdir)
        
        # Transcribe the audio
        transcription = whisper_model.transcribe(file, fp16=False)["text"].strip()

        # Save the transcription to a text file
        with open(transcription_name + ".txt", "w") as file:
            file.write(transcription)

    return transcription