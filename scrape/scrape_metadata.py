import requests
import pandas as pd
import time
import csv


# Function to scrape 1 individual book details based on its asin
def scrape_each_asin(asin):
    # Base URL for the API endpoint
    BASE_URL = "https://api.audible.com/1.0/catalog/products/"
    
    # API response group parameters
    response_groups = "product_plan_details,price,category_ladders,series,media,rating,sample"
    
    # Make a request to the Audible API
    response = requests.get(f"{BASE_URL}{asin}?response_groups={response_groups}")
    
     # Check if the request was successful
    if response.status_code == 200:
            data = response.json()
            product = data.get('product', {})
            
            # Check if necessary data exists before extracting
            required_fields = ['asin', 'title', 'authors', 'sample_url', 'category_ladders']
            if all(field in product for field in required_fields):

                # Check if the book has a only 1 genre
                category_ladders = product.get('category_ladders', [])
                if len(category_ladders) == 1:
                    
                    # initiate price to handle non-numberical value later
                    price = product.get('price', {}).get('list_price', {}).get('base', None)
                    # Extract the book details
                    book_details = {
                            'asin': product.get('asin', ''),
                            'title': product.get('title', ''),
                            'author': ','.join([author.get('name', '') for author in product.get('authors', [])]),
                            'author_asin': ','.join([author.get('asin', '') for author in product.get('authors', [])]),
                            'narrator': ','.join([narrator.get('name', '') for narrator in product.get('narrators', [])]),
                            'publication_datetime': product.get('publication_datetime', ''),
                            'release_date': product.get('release_date', ''),
                            'publisher_name': product.get('publisher_name', ''),
                            'length': product.get('runtime_length_min', ''),
                            'category': category_ladders[0]['ladder'][0].get('name', ''),
                            'mp3_excerpt': product.get('sample_url', ''),
                            'overall_rating': product.get('rating', {}).get('overall_distribution', {}).get('display_average_rating', ''),
                            'overall_num_ratings': product.get('rating', {}).get('overall_distribution', {}).get('num_ratings', ''),
                            'performance_rating': product.get('rating', {}).get('performance_distribution', {}).get('display_average_rating', ''),
                            'performance_num_ratings': product.get('rating', {}).get('performance_distribution', {}).get('num_ratings', ''),
                            'story_rating': product.get('rating', {}).get('story_distribution', {}).get('display_average_rating', ''),
                            'story_num_ratings': product.get('rating', {}).get('story_distribution', {}).get('num_ratings', ''),
                            'num_reviews': product.get('rating', {}).get('num_reviews', ''),
                            'price': round(float(price), 2) if isinstance(price, (int, float)) else '',
                            'series_asin': product['series'][0].get('asin') if isinstance(product.get('series'), list) else '',
                            'series_name': product['series'][0].get('title') if isinstance(product.get('series'), list) else ''
                        }
                        
                    return book_details
    return None


# Function to update progress
def update_progress(output_csv, failed_csv, asin, book_details, status, category_count, author_count, all_categories):
    if status == 'success':
        # Append book details to output_csv
        with open(output_csv, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=book_details.keys())
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(book_details)

        # Update counts for category and author
        category = book_details.get('category', '')
        if category in all_categories: # Only update category_count if the category is in 6 chosen categories
            category_count[category] = category_count.get(category, 0) + 1 
            
        author = book_details.get('author', '')
        author_count[author] = author_count.get(author, 0) + 1

    elif status == 'failed':
        # Log the ASIN in the failed_csv
        with open(failed_csv, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            if csvfile.tell() == 0:
                writer.writerow(['asin'])
            writer.writerow([asin])
        

# Batch scraping function
def batch_scrape(asins, n, max_category, max_author, output_csv, failed_csv, all_categories):
    # Initialize processed ASINs and dictionaries for category and author counts
    try:
        # Read the existing output CSV to get processed ASINs
        output_data = pd.read_csv(output_csv)
        processed_asins = set(output_data['asin'].tolist())
        
        # Initialize category and author counts 
        category_count = output_data['category'].value_counts().to_dict()
        category_count = {cat: count for cat, count in category_count.items() if cat in all_categories} # Only track 6 chosen categories
        author_count = output_data['author'].value_counts().to_dict()
    except FileNotFoundError:
        # If the file does not exist, initialize dictionaries
        processed_asins = None
        category_count = {}
        author_count = {}

    # Initialize failed ASINs set
    try:
        failed_asins = set(pd.read_csv(failed_csv)['asin'].tolist())
    except FileNotFoundError:
        failed_asins = None

    # Initialize all categories if they are not already in category_count
    for category in all_categories:
        if category not in category_count:
            category_count[category] = 0

    # Pre-filter the list of ASINs
    asins = [
        (asin, category, author)
        for asin, category, author in asins
        if asin not in processed_asins and asin not in failed_asins
    ]

    # Loop through asins
    success_count = 0
    while asins:
        # Stop when all categories reach limit
        if all(count >= max_category for count in category_count.values()):
            print("All category limits reached, stop scraping")
            break

        # Determine which categories and authors have reached their limits
        blocked_categories = {cat for cat, count in category_count.items() if count >= max_category}
        blocked_authors = {auth for auth, count in author_count.items() if count >= max_author}

        # Re-filter the full list of ASINs based on updated blocked categories and authors
        asins = [
            (asin, category, author)
            for asin, category, author in asins
            if category not in blocked_categories and author not in blocked_authors
        ]
        
        # Notify when running out of asin
        if not asins:
            print("No valid ASINs left to scrape")
            break

        # Process the batch
        batch = asins[:n] 
        batch_success_count = 0
        for asin, category, author in batch:
            # Scrape the ASIN
            book_details = scrape_each_asin(asin)
            # Update progress for success or failure
            status = 'success' if book_details else 'failed'
            update_progress(output_csv, failed_csv, asin, book_details, status, category_count, author_count, all_categories)

            if status == 'success':
                success_count += 1
                print(f'Total scraped: {success_count}')

        # Remove the processed batch from the list
        asins = asins[n:]

        # Sleep to avoid hitting the API too quickly
        time.sleep(0.2)


def main():
    start_main = time.time()
    # Read the data munging file to get ASINs
    asins_df = pd.read_csv('../data/audible_mungingdata.csv')

    # Tuple of ASIN, category, and author for each book
    asins = asins_df[['asin', 'category', 'author']].values.tolist()

    # Define 6 chosen categories
    all_categories = asins_df['category'].unique().tolist()

    # Initialize output and fail CSV file paths
    output_csv = '../data/audible_metadata.csv'
    failed_csv = '../data/audible_fail.csv'

    # Start the batch scraping process
    batch_scrape(asins, n=15, max_category=200, max_author=24, output_csv=output_csv, failed_csv=failed_csv, all_categories=all_categories)
    total_time = time.time() - start_main
    print(f"Total running time: {total_time:.4f} seconds")

# Call the main function to run the script
if __name__ == '__main__':
    main()
