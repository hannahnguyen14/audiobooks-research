import wave
import json
import os
import pandas as pd
from vosk import Model, KaldiRecognizer
import soundfile as sf
import time

class Word:
    ''' A class representing a word from the JSON format for vosk speech recognition API '''
    def __init__(self, dict):
        self.conf = dict["conf"]
        self.end = dict["end"]
        self.start = dict["start"]
        self.word = dict["word"]

    def to_string(self):
        ''' Returns a string describing this instance '''
        return "{:20} from {:.2f} sec to {:.2f} sec, confidence is {:.2f}%".format(
            self.word, self.start, self.end, self.conf*100)

# Function to process each wav file and extract word segments
def segment_audio_with_words(audio_path, model_path):
    model = Model(model_path)
    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)
    part_result = json.loads(rec.FinalResult())
    results.append(part_result)
    
    word_segments = {
        'word': [],
        'start': [],
        'end': [],
        'confidence': []
    }

    for result in results:
        if 'result' in result:
            for word_info in result['result']:
                word_segments["word"].append(word_info['word'])
                word_segments["start"].append(word_info['start'])
                word_segments["end"].append(word_info['end'])
                word_segments["confidence"].append(word_info['conf'])

    return word_segments

# Function to process all wav files in batches
def process_all_wav_files(df, wav_dir, model_path, output_dir, batch_size):
    # Create csv folder if not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Add 'csv' column if not exist
    if 'csv' not in df.columns:
        df['csv'] = 0  

    # Filter for rows where 'csv' is 0
    df_to_process = df[df['csv'] == 0]
    total_files = len(df_to_process)
    saved_count = 0
    batch_num = 0

    for i in range(0, total_files, batch_size):
        batch_num += 1
        batch = df_to_process.iloc[i:i + batch_size]
        print(f"Starting batch {batch_num} with {len(batch)} files.")

        for index, row in batch.iterrows():
            asin = row['asin']
            output_csv = os.path.join(output_dir, f"{asin}.csv")
            wav_path = os.path.join(wav_dir, f"{asin}.wav")

            try:
                # Extract word segments
                word_segments = segment_audio_with_words(wav_path, model_path)

                # Create df
                df_word_segments = pd.DataFrame(word_segments)

                # Add duration
                df_word_segments['duration'] = df_word_segments['end'] - df_word_segments['start']

                # Calculate pauses
                pauses = []
                for e, segment_row in df_word_segments.iterrows():
                    try:
                        pauses.append(segment_row['start'] - df_word_segments.loc[e-1]['end'])
                    except:
                        pauses.append(0)
                df_word_segments['pauses'] = pauses

                # Save to CSV
                df_word_segments.to_csv(output_csv, index=False)
                saved_count += 1
                print(f"Done: {saved_count} files")

                # Update the CSV status in the DataFrame
                df.loc[index, 'csv'] = 1

            except:
                print(f"Failed to process {asin}.wav")

        # Save the updated csv to track progress 
        df.to_csv('../data/audible_metadata_filtered.csv', index=False)
        print(f"Completed batch {batch_num}: {saved_count} files converted.")

        time.sleep(60)

    print(f"Total CSV files saved: {saved_count}")

# Define path
wav_dir = '../data/wav/'
model_path = 'vosk-model-en-us-0.22'
output_dir = '../data/csv/'
# Read csv 
df = pd.read_csv('../data/audible_metadata_filtered.csv')

# Process all wav files
process_all_wav_files(df, wav_dir, model_path, output_dir, 100)
