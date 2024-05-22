import praw
import json

reddit = praw.Reddit(
    client_id='EfULoAP4Z35EJFP1wFDNUQ',
    client_secret='6B_PvQOFeVo8UDi33QWRV5WYrNiI5g',
    user_agent='Clinical Trial Sentiment Analyzer'
)

unwanted_words =  ["register", "sign up", "donation", "recruiting", "conducting", "evaluation", "compensation"]

def contains_unwanted_words(text, unwanted_words):
    text = text.lower()
    return any(word in text for word in unwanted_words)

def scrape_subreddit(subreddit_name, limit=100, fetch_limit=200):
        subreddit = reddit.subreddit(subreddit_name)
        posts = []
        fetched_posts = 0
        for post in subreddit.top(limit=fetch_limit):
            fetched_posts += 1
            title = post.title.lower()
            body = post.selftext.lower()
            
            if not (contains_unwanted_words(title, unwanted_words) or contains_unwanted_words(body, unwanted_words)):
                post_data = {
                    'title': post.title,
                    'body': post.selftext,
                    'comments': [comment.body for comment in post.comments if hasattr(comment, 'body')]
                }
                posts.append(post_data)
                print(f"Title: {post.title}")
                print(f"Body: {post.selftext}")
                print("Comments:")
                for comment in post_data['comments']:
                    print(f" - {comment}")
                print("\n")
            if len(posts) >= limit:
                break
        print(f"Fetched {fetched_posts} posts from r/{subreddit_name}")
        return posts

if __name__ == "__main__":
    subreddit_name = 'clinicaltrials'  
    limit = 100  
    fetch_limit = 200  
    data = scrape_subreddit(subreddit_name, limit, fetch_limit)
    if data:
        print(f"Scraped {len(data)} posts from r/{subreddit_name}")
        with open('scraped_posts.json', 'w') as f:
            json.dump(data, f, indent=4)
