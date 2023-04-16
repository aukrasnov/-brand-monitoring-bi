import requests
from kafka import KafkaProducer
import time


def extract(subbredit):
    """Extracts data about recent blog posts from reddit API and returns a list"""
    # url = " http://www.reddit.com/r/dogs/search.json?q=kittens&sort=new"
    url = f"http://www.reddit.com/r/{subbredit}/new.json"
    response = requests.get(url, headers={'User-agent': 'brand-monitoring-bi on github 0.1'})
    data = response.json()
    posts = data['data']['children']
    return posts


def clean(pushed_posts, posts):
    "Deduplicates already pushed to kafka posts"

    new_posts = []
    for post in posts:
        if post['data']['id'] not in pushed_posts:
            new_posts.append(post)

    return new_posts


def load(list_of_dicts):
    """Pushes list of dicts to kafka"""

    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    for post in list_of_dicts:
        producer.send('reddit', str(post).encode('utf-8'))
        producer.flush()


def main(subbredit, sleep_time):
    f"""Takes new posts from given subreddit and pushes them to kafka every {sleep_time} seconds"""
    pushed_posts = []
    while True:
        posts = extract(subbredit)
        new_posts = clean(pushed_posts, posts)
        load(new_posts)
        pushed_posts += [post['data']['id'] for post in new_posts]
        time.sleep(sleep_time)
