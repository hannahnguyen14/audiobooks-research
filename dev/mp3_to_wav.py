import os
import librosa
import soundfile as sf

# Function to convert 1 mp3 to wav
def convert_mp3_to_wav(mp3_path, wav_path):
    try:
        # Load mp3 file
        y, sr = librosa.load(mp3_path, sr=None)
        # Write wav file 
        sf.write(wav_path, y, sr)
        return True
    except:
        print(f"Failed to convert {mp3_path}")
        return False

# Function to convert all mp3s in a folder to wavs in another folder
def batch_convert_mp3_to_wav(mp3_folder, wav_folder):
    if not os.path.exists(wav_folder):
        os.makedirs(wav_folder)

    converted_count = 0

    for filename in os.listdir(mp3_folder):
        mp3_path = os.path.join(mp3_folder, filename)
        wav_path = os.path.join(wav_folder, filename.replace(".mp3", ".wav"))

        # Check if the .wav file already exists
        if os.path.exists(wav_path):
            continue  
        
        # Convert
        if convert_mp3_to_wav(mp3_path, wav_path):
            converted_count += 1

        # Print status after every 100 files
        if converted_count % 100 == 0:
            print(f"Converted {converted_count} files")

    # Print total files converted at the end
    print(f"Conversion completed: {converted_count} files ")

# Paths to the folders
mp3_folder = '../data/mp3'
wav_folder = '../data/wav'

# Start the batch conversion process
batch_convert_mp3_to_wav(mp3_folder, wav_folder)
