import os
import pandas as pd
import random

def main():
    # Load prepared corpus
    corpus_df = pd.read_csv('../data/corpus/prepared_corpus.csv')

    # Set number of documents per binary corpus
    num_documents_per_corpus = 180  # Easily adjustable number

    # Define genres for binary classification
    genres = [
        "Science Fiction & Fantasy",
        "Romance",
        "Biographies & Memoirs",
        "Business & Careers",
        "Mystery, Thriller & Suspense",
        "History"
    ]

    # Set seed for reproducibility
    random.seed(42)

    # Track used ASINs to prevent overlap
    used_asins = set()

    # Create binary corpora for each genre
    for genre in genres:
        used_asins = create_binary_corpus(corpus_df, genre, num_documents_per_corpus, used_asins)

    # Create and save the remaining data as reserved corpus
    remaining_corpus = corpus_df[~corpus_df['asin'].isin(used_asins)]
    remaining_corpus.to_csv('../data/corpus/reserved_test_set.csv', index=False)
    print(f"Reserved corpus created with {len(remaining_corpus)} documents.")

def create_binary_corpus(corpus_df, main_genre, num_documents, used_asins):
    # Select main genre documents excluding already used ASINs
    main_genre_docs = corpus_df[(corpus_df['label'] == main_genre) & (~corpus_df['asin'].isin(used_asins))]
    main_genre_docs = main_genre_docs.sample(n=num_documents // 2, random_state=42)

    # Label main genre as 1
    main_genre_docs['label'] = 1

    # Update used ASINs
    used_asins.update(main_genre_docs['asin'].tolist())

    # Select non-main genre documents excluding already used ASINs
    non_main_genre_docs = corpus_df[(corpus_df['label'] != main_genre) & (~corpus_df['asin'].isin(used_asins))]
    non_main_genres = [g for g in corpus_df['label'].unique() if g != main_genre]

    # Select documents for each non-main genre evenly
    docs_per_non_main_genre = (num_documents // 2) // len(non_main_genres)
    non_main_selected = []

    for genre in non_main_genres:
        genre_docs = non_main_genre_docs[non_main_genre_docs['label'] == genre].sample(
            n=min(docs_per_non_main_genre, len(non_main_genre_docs[non_main_genre_docs['label'] == genre])),
            random_state=42
        )
        non_main_selected.append(genre_docs)

    # Combine selected non-main genre documents
    non_main_genre_docs = pd.concat(non_main_selected)

    # Label non-main genres as 0
    non_main_genre_docs['label'] = 0

    # Update used ASINs
    used_asins.update(non_main_genre_docs['asin'].tolist())

    # Combine main and non-main genre documents into a binary corpus
    binary_corpus = pd.concat([main_genre_docs, non_main_genre_docs]).sample(frac=1, random_state=42).reset_index(drop=True)

    # Save the binary corpus
    output_path = f'../data/corpus/{main_genre.replace(" ", "_")}.csv'
    binary_corpus.to_csv(output_path, index=False)
    print(f"Binary corpus for {main_genre} created with {len(binary_corpus)} documents.")

    return used_asins

if __name__ == "__main__":
    main()
