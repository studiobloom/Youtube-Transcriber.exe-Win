import sys
import os
import warnings

# Function to create a temporary directory
def create_temp_dir():
    temp_dir = tempfile.mkdtemp()
    return temp_dir

# Function to create and open a txt file
def create_and_open_txt(text, filename):
    # Create and write the text to a txt file
    with open(filename, "w") as file:
        file.write(text)

    # Open the txt file
    os.startfile(filename)

# Function to display a loading prompt
def show_loading_prompt(message):
    sys.stdout.write(message + " ")
    sys.stdout.flush()

# Function to import the required libraries
def import_libraries():
    global shutil, whisper, detect, YouTube, tempfile

    import shutil
    import whisper
    from langdetect import detect
    from pytube import YouTube
    import tempfile

# Function to ask the user if they want to run the program again
def ask_to_run_again():
    return input("\n\nPress Enter to run the program again:")

# Display loading prompt
show_loading_prompt("Transcribing audio from a YouTube video to text with language detection. \nAuthor: Javed Ali (www.javedali.net)\nWindows Build packaged by https://github.com/studiobloom\nDescription: This script will ask the user for a YouTube video URL, download the audio from the video, transform it to text, detect the language of the file, and save it to a txt file.")


# Import the required libraries
import_libraries()

# Display loading prompt
show_loading_prompt("\n\nInitializing the application... Please Wait.")

# Loop to ask the user if they want to run the program again
while True:
    # Ask user for the YouTube video URL
    url = input("\n\nEnter the YouTube video URL: ")

    # Display loading prompt
    show_loading_prompt("Downloading the audio... Please Wait.")

    # Create a temporary directory to store the audio
    output_path = create_temp_dir()
    filename = "audio.mp3"

    # Create a YouTube object from the URL
    yt = YouTube(url)

    # Get the audio stream
    audio_stream = yt.streams.filter(only_audio=True).first()

    # Download the audio stream to the temporary directory
    audio_stream.download(output_path=output_path, filename=filename)

    print(f"\rAudio downloaded to {output_path}/{filename}")

    # Load the base model and transcribe the audio
    model = whisper.load_model("base")

    # Suppress the UserWarning raised by whisper
    warnings.filterwarnings("ignore", category=UserWarning)

    # Display loading prompt
    show_loading_prompt("Transcribing the audio... Please Wait.")

    result = model.transcribe(os.path.join(output_path, filename))
    transcribed_text = result["text"]
    print("\rTranscription complete!")

    # Detect the language
    language = detect(transcribed_text)

    # Display loading prompt
    show_loading_prompt("Detecting the language... Please Wait.")

    print(f"\rDetected language: {language}")

    # Create and open a txt file with the text
    transcription_filename = f"output_{language}.txt"
    create_and_open_txt(transcribed_text, transcription_filename)

    # Remove temporary files
    shutil.rmtree(output_path)

    print(f"\nTranscription saved to {transcription_filename}")

    run_again = ask_to_run_again().strip().lower()
    if run_again == "exit":
        break

    # Display loading prompt
    show_loading_prompt("Initializing the application... Please Wait.")
    # Import the required libraries again for the next iteration
    import_libraries()
