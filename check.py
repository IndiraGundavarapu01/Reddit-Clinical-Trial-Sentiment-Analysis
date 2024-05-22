import json

def load_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def calculate_basic_metrics(posts):
    total_posts = len(posts)
    messages_generated = sum(1 for post in posts if 'message' in post and post['message'])
    errors = sum(1 for post in posts if 'message' in post and post['message'] == "Error generating message.")
    
    print(f"Total posts processed: {total_posts}")
    print(f"Messages generated successfully: {messages_generated}")
    print(f"Errors encountered: {errors}")

def analyze_sentiment_distribution(posts):
    sentiments = [post['sentiment']['label'] for post in posts if 'sentiment' in post]
    sentiment_distribution = {label: sentiments.count(label) for label in set(sentiments)}
    
    print("Sentiment distribution:")
    for sentiment, count in sentiment_distribution.items():
        print(f"{sentiment}: {count}")

def sample_generated_messages(posts, sample_size=5):
    sampled_posts = [post for post in posts if 'message' in post and post['message'] != "Error generating message."]
    sampled_posts = sampled_posts[:sample_size]
    
    print("Sampled generated messages:")
    for post in sampled_posts:
        print(f"Post Title: {post['title']}")
        print(f"Sentiment: {post['sentiment']['label']}")
        print(f"Generated Message: {post['message']}")
        print("----------")

def main():
    file_path = 'posts_with_sentiments_and_messages.json'
    posts = load_json(file_path)
    
    calculate_basic_metrics(posts)
    analyze_sentiment_distribution(posts)
    sample_generated_messages(posts, sample_size=5)

if __name__ == "__main__":
    main()
