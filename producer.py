import requests
from confluent_kafka import Producer
import time
import os
import logging


KAFKA_BOOTSTRAP_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVER')
KAFKA_KEY = os.getenv('KAFKA_KEY')
KAFKA_SECRET = os.getenv('KAFKA_SECRET')


def extract(search_phrase):
    """Extracts data about recent blog posts from reddit API and returns a list"""
    url = f'https://www.reddit.com/search.json?q={search_phrase}&sort=new'
    response = requests.get(url, headers={'User-agent': 'brand-monitoring-bi on github 0.1'})
    data = response.json()
    posts = data['data']['children']
    return posts


def clean(pushed_posts, posts):
    """Deduplicates already pushed to kafka posts"""

    new_posts = []
    for post in posts:
        if post['data']['id'] not in pushed_posts:
            new_posts.append(post)

    return new_posts


def load(list_of_dicts, topic):
    """Pushes list of dicts to kafka"""
    pushed_posts = []
    confluent_conf = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVER,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'PLAIN',
        'sasl.username': KAFKA_KEY,
        'sasl.password': KAFKA_SECRET,
    }
    producer = Producer(confluent_conf)
    for post in list_of_dicts:
        if post['data']['selftext'] and post['data']['id'] not in pushed_posts:
            p = dict()
            p['id'] = post['data']['id']
            p['subreddit'] = post['data']['subreddit']
            p['selftext'] = post['data']['selftext']
            p['title'] = post['data']['title']
            p['created_utc'] = post['data']['created_utc']
            p['url'] = post['data']['url']
            producer.produce(topic, key=post['data']['id'], value=str(p).encode('utf-8'))
            pushed_posts.append(post['data']['id'])
            logging.debug(f"Pushed post {post['data']['id']} to kafka")
            producer.flush()


def main(search_phrase, sleep_time):
    f"""Takes new posts from given subreddit and pushes them to kafka every {sleep_time} seconds"""

    pushed_posts = []
    while True:
        posts = extract(search_phrase)
        new_posts = clean(pushed_posts, posts)
        load(new_posts, 'reddit')
        pushed_posts += [post['data']['id'] for post in new_posts]
        time.sleep(sleep_time)


logging.basicConfig(level=logging.DEBUG)
if __name__ == '__main__':
    main('dogs', 30)
