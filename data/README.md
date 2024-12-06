# Notes for Various files and folders

__audible_fail.csv__
- Data to track not usable asins for scraping

__audible_metadata_filtered.csv__
- Final metadata, including links to mp3 excerpt for download and information for analysis

__audible_mungingdata.csv__
- Data result from csv_data_munging code, contain asins list for scrape_metadata code

__csv__
- Contain converted audio to text data, each csv represent 1 audio exceprts

__Genre name csv in corpus folder__
- Each csv contain full document text and labeling for each genre binary model (1 as main genre, 0 as other genres)

__mp3 folder__
- Contain downloaded mp3 files

__prepared_corpus.csv__
- All document full text and genre label

__researved_test_set.csv__
- Contains documents researved for final multi-classification evaluation

__researved_test_pred.csv__
_ Reserved test set with prediction probability from 6 binary models
