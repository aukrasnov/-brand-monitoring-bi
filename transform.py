#!/usr/bin/python
# -*- coding: utf-8 -*-
import openai
import json

with open('terraform/terraform.tfstate') as f:
    config = data = json.load(f)

OPEN_API_KEY = config['outputs']['open_api_key']['value']


def chat2msg(messages_history):
    response = openai.ChatCompletion.create(
        api_key=OPEN_API_KEY,
        model="gpt-3.5-turbo",
        messages=messages_history
    )

    return response.get('choices', [])[0].get('message', {}).get('content', '')


def get_relevance_mark(content):
    try:
        messages = [
            {"role": "system", "content": " You are a usefill person."},
            {"role": "user", "content": f"We are a dog goods company called Pup Essentials (http://pupessentials.com). Our products are designed to make life easier and more enjoyable for both dogs and their owners.We like articles about: our brand, competition within the dog goods industry, topics related to canine health and wellness, or when certain pet care brands receive negative press. Is the following article interesting for us? Reply with a single number between 0 and 100. 0 being not interesting at all, 100 being super interesting. After this number, add a dash (-), following by a short explanation. This is the crawled article: {content}"},
        ]

        answer = chat2msg(messages)
        return int(answer.split('-')[0])

    except:
        return 0
