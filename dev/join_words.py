import os
import pandas as pd

# Paths to required files and folders
metadata_file = '../data/audible_metadata_filtered.csv'
csv_folder = '../data/csv/'

# Load metadata to identify genres
metadata_df = pd.read_csv(metadata_file)

# Define the genres
genres = ["Science Fiction & Fantasy", "Mystery, Thriller & Suspense", "Romance", 
          "Business & Careers", "Biographies & Memoirs", "History"]

# Separate ASINs by genre
genre_asins = {genre: metadata_df[metadata_df['category'] == genre]['asin'].tolist() for genre in genres}

# Function to concatenate words from a CSV file
def load_words_from_csv(file_path):
    df = pd.read_csv(file_path)
    if 'word' in df.columns:
        words = ' '.join(df['word'].astype(str).tolist())
        return words
    return ''  # Return an empty string if 'word' column is missing

# Initialize lists to hold documents, labels, ASINs, and excluded ASINs
documents = []
labels = []
asins = []
excluded_asins = []

# Aggregate documents and labels
for genre, asins_list in genre_asins.items():
    for asin in asins_list:
        file_path = os.path.join(csv_folder, f"{asin}.csv")
        if os.path.exists(file_path):
            document = load_words_from_csv(file_path)
            if document.strip():  # Only include non-empty documents
                documents.append(document)
                labels.append(genre)
                asins.append(asin)
            else:
                excluded_asins.append(asin)

# Combine documents, labels, and ASINs into a DataFrame
corpus_df = pd.DataFrame({
    'asin': asins,
    'document': documents,
    'label': labels
})

# Save to CSV
corpus_df.to_csv('../data/corpus/prepared_corpus.csv', index=False)
print(f"Total documents in corpus: {len(corpus_df)}")

# Print the list of excluded ASINs
print(f"Excluded ASINs (total {len(excluded_asins)}): {excluded_asins}")

