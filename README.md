## Setup Instructions

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the required packages using `pip install -r requirements.txt`.
4. Configure your Reddit and OpenAI API credentials in the script.
5. Run the scripts using `python reddit_scraper.py`, `python analyze_sentiment.py`, `python generate_messages.py`.

## Process Overview

1. Scraping:
The data collection process begins with scraping Reddit posts related to clinical trials using the PRAW (Python Reddit API Wrapper) library. This script connects to Reddit's API with provided credentials and fetches posts from specified subreddits. To filter out irrelevant content, the script includes a list of unwanted words (e.g., "register", "sign up", "donation") and only retains posts that do not contain these terms in their title or body. This ensures that the collected data is relevant to user opinions and experiences rather than promotional content. The filtered posts are then saved in a JSON file named scraped_posts.json for further analysis.

2. Sentiment Analysis:
Once the data is collected, sentiment analysis is performed on the posts to understand the general attitude of users towards clinical trials. This step utilizes the Hugging Face Transformers library, specifically the DistilBERT model fine-tuned for sentiment analysis (distilbert-base-uncased-finetuned-sst-2-english). Each post's body is truncated to fit the model's input size, and the sentiment is analyzed using a pre-trained sentiment pipeline. The results, which include the sentiment label (positive, negative, or neutral) and a confidence score, are appended to each post. The updated posts, now including sentiment analysis results, are saved in a JSON file named posts_with_sentiments.json.

3. Message Generation:
The final step involves generating personalized messages for each post based on the analyzed sentiment. This is done using the OpenAI API with the GPT-3.5-turbo model. A prompt is crafted for each post, incorporating the sentiment label and post title, to generate a message that engages the user based on their expressed sentiments. The script includes error handling for rate limits and retries with exponential backoff to manage OpenAI API usage effectively. The generated messages are added to the respective posts, and the complete data set, now containing original posts, sentiment analysis, and personalized messages, is saved in a JSON file named posts_with_sentiments_and_messages.json. This process ensures that the generated messages are relevant and tailored to the user's sentiments, enhancing the likelihood of user engagement.

4. To evaluate the efficiency and effectiveness of the predictions, run the evaluate_predictions.py script, This script calculates basic metrics, analyzes sentiment distribution, and samples generated messages to ensure quality and relevance.

## Methodology and Challenges
### Methodology

1. Data Collection:

Using PRAW to connect to the Reddit API and fetch posts from specific subreddits.
Filtering posts to exclude those containing unwanted promotional content.

2. Sentiment Analysis:

Utilizing the Hugging Face Transformers library and the DistilBERT model to analyze the sentiment of each post.
Truncating post content to fit the model's input size for accurate sentiment analysis.

3. Message Generation:

Generating personalized messages using the OpenAI API based on the analyzed sentiment.
Implementing error handling and exponential backoff to manage API rate limits.

### Challenges:

1. Rate Limits and Quotas:

- The free tier of OpenAI imposes strict rate limits and usage quotas, leading to frequent RateLimitError and insufficient_quota errors.
- Implemented exponential backoff and retries to handle rate limits, but still faced constraints due to free tier limitations.

2. Filtering Relevant Content:

- Ensuring that only relevant user opinions and experiences were collected by filtering out promotional content based on specific keywords.

3. Handling Large Texts:

- Truncating long post content to fit the input size limit of the sentiment analysis model while preserving the essence of the post.

## Examples:

Example of a scraped post:

   {
        "title": "Covans Dallas TX",
        "body": "Warning about this place\n\nThey don't pick up the phones\n\nThey don't tell you if your in untill the day before or day of\n\nThey pay you LATE really late if at all\n\nThey are extremely unorginazed so you get in trouble because someone didn't tell someone else. \n\nDo not go to covans in Dallas Texas",
        "comments": []
    }

Example of sentiment analysis result:
  {
        "title": "Covans Dallas TX",
        "body": "Warning about this place\n\nThey don't pick up the phones\n\nThey don't tell you if your in untill the day before or day of\n\nThey pay you LATE really late if at all\n\nThey are extremely unorginazed so you get in trouble because someone didn't tell someone else. \n\nDo not go to covans in Dallas Texas",
        "comments": [],
        "sentiment": {
            "label": "NEGATIVE",
            "score": 0.9987788796424866
        }
    }

## Ethical Considerations
1. Privacy and Consent:

Ensured compliance with Reddit's API terms of use, respecting user privacy and data usage policies.
Collected only publicly available data without personal identifiers.

2. Data Relevance and Integrity:

Filtered out promotional content to focus on genuine user opinions and experiences.
Maintained the integrity of user-generated content by preserving the context and meaning in the sentiment analysis and message generation processes.

3. Responsible AI Use:

Implemented error handling and backoff strategies to manage API usage responsibly.


-- still working on generating messages well~