import requests
import time
import pandas as pd

# Function to save 1 individual mp3 
def save_mp3(url, filename):
    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)
    return True

# Function to save mp3 in batches
def save_mp3_in_batches(df, batch_size):
    downloaded = 0

    # Filter for rows where 'downloaded' is 0
    df_to_download = df[df['downloaded'] == 0]

    for index, row in df_to_download.iterrows():
        asin = row['asin']
        url = row['mp3_excerpt']

        # Stop once batch size is reached
        if downloaded == batch_size:
            break

        try:
            # Download and save the MP3 file
            save_mp3(url, f'../data/mp3/{asin}.mp3')
            downloaded += 1
            print(f"Downloaded {downloaded} mp3s")

            # Update 'downloaded' column to 1 after successful download
            df.loc[index, 'downloaded'] = 1
        except:
            print(f"Failed to download {asin}")
    
        time.sleep(0.5)

    # Save the DataFrame after each batch to ensure progress is tracked
    df.to_csv('../data/audible_metadata_filtered.csv', index=False)

    # Return True if no new files were downloaded
    if downloaded == 0:
        return True
    else:
        return False

# Read csv 
df = pd.read_csv('../data/audible_metadata_filtered.csv')

# Start saving mp3s
count = 0
while True:
    print(f"Batch {count + 1}: Starting download...")
    
    result = save_mp3_in_batches(df, 40)  
    count += 1

    if result:  
        break
    time.sleep(2)  
