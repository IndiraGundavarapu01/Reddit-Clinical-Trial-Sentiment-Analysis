import os
import json
import openai
import time
from openai import RateLimitError, OpenAIError
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')


client = openai.OpenAI(api_key=api_key)

def generate_message_with_openai(sentiment_label, post_title, model="gpt-3.5-turbo"):
    prompt = (
        f"Based on the following sentiment '{sentiment_label}' and post title '{post_title}', "
        "generate a personalized message aimed at users who express interest in or could potentially "
        "benefit from participating in a clinical trial."
    )

    retry_count = 0
    while retry_count < 3:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100
            )
            return response.choices[0].message['content'].strip()
        except RateLimitError as e:
            retry_count += 1
            wait_time = 2 ** retry_count
            print(f"Rate limit exceeded: {e}. Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        except OpenAIError as e:
            print(f"OpenAI API error: {e}")
            break
    return "message."

def add_generated_messages(posts):
    valid_posts = []
    for post in posts:
        sentiment_label = post['sentiment']['label']
        post['message'] = generate_message_with_openai(sentiment_label, post['title'])
        print(f"Generated message for post '{post['title']}': {post['message']}")
        valid_posts.append(post)
    return valid_posts

def process_posts_in_batches(posts, batch_size=1):
    all_valid_posts = []
    for i in range(0, len(posts), batch_size):
        batch = posts[i:i+batch_size]
        valid_posts = add_generated_messages(batch)
        all_valid_posts.extend(valid_posts)
        print("Sleeping for 60 seconds to respect rate limits :')...")
        time.sleep(60)
    return all_valid_posts

if __name__ == "__main__":
    with open('posts_with_sentiments.json', 'r') as f:
        posts = json.load(f)
    print(f"Loaded {len(posts)} posts from posts_with_sentiments.json")  
    processed_posts = process_posts_in_batches(posts, batch_size=1) 
    with open('posts_with_sentiments_and_messages.json', 'w') as f:
        json.dump(processed_posts, f, indent=4)








