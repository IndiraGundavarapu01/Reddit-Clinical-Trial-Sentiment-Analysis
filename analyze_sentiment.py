import json
from transformers import pipeline, DistilBertTokenizerFast

sentiment_pipeline = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')
tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

def truncate_text(text, max_length=512):
    tokens = tokenizer.encode(text, truncation=True, max_length=max_length)
    return tokenizer.decode(tokens, skip_special_tokens=True)

def analyze_sentiments(posts):
    for post in posts:
        truncated_body = truncate_text(post['body'])
        result = sentiment_pipeline(truncated_body)
        post['sentiment'] = result[0]  
        print(f"Sentiment for post '{post['title']}': {post['sentiment']}")

if __name__ == "__main__":
    with open('scraped_posts.json', 'r') as f:
        posts = json.load(f)
    print(f"Loaded {len(posts)} posts from scraped_posts.json")
    analyze_sentiments(posts)
    with open('posts_with_sentiments.json', 'w') as f:
        json.dump(posts, f, indent=4)

