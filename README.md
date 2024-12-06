# Unveiling Genre Patterns: A Computational Study of Audible Excerpts

## Overview
This repository contains the complete pipeline and analysis for a project aimed at classifying audiobook genres using computational techniques. The project explores the relationship between linguistic patterns in audiobook excerpts and their respective genres, leveraging machine learning models to identify predictive features and evaluate classification performance across six main genres.

## Key Features
- Data Collection: Scraped audiobook metadata and audio samples from the Audible API, utilizing publicly available datasets ([provide link/source]) for initial ASIN listings.
- Audio Processing: Converted audio samples to text using the Vosk model, capturing word-level details.
- Feature Engineering: Applied TF-IDF to extract top predictive terms for each genre and utilized the Mann-Whitney U test to rank and filter terms for binary classification models.
- Genre Classification: Built binary logistic regression models for each genre, optimizing classification thresholds and normalizing probabilities to evaluate inter-genre misclassification patterns.
- Results Analysis: Visualized accuracy, misclassification rates, and key predictive terms across genres, highlighting connections and distinctions among fiction and non-fiction genres.

## Repository Structure
data/: Contains raw and processed datasets, including scraped audiobook metadata and text-transcribed excerpts.
scrape/: Includes Python scripts for data scraping.
dev/: Includes Python scripts for data preprocessing.
ultilities/: Includes Python scripts for feature extraction, model training, and evaluation.

## Key Results
Top predictive terms for each genre reveal genre-specific linguistic patterns.
Binary models demonstrate high accuracy with threshold optimization, highlighting distinct and overlapping characteristics among genres.
Inter-genre misclassification analysis provides insights into genre relationships, such as the strong connection between Science Fiction & Fantasy and Romance.

## Limitations and Future Work
- Limitations: Some documents with all-zero vectors were excluded, reflecting a trade-off between specificity and generalizability.
- Future Directions:
Explore consumer behavior data (e.g., ratings and reviews) to analyze its relationship with genre misclassification.
Incorporate audio features like spacing and word duration for improved classification.
Extend the analysis to multi-class classification for a holistic understanding of genre dynamics.

## Contributions:
- Researcher: Hannah Nguyen - email: nguyen_n4@denison.edu
- Advisor: Dr. Matthew Lavin - email: lavinm@denison.edu
If you'd like to contribute to this project, feel free to fork the repository and submit a pull request.

Contact
For any inquiries, please contact Hannah Nguyen at nguyen_n4@denison.edu.