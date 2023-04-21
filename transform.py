#!/usr/bin/python
# -*- coding: utf-8 -*-
import openai
import os

OPEN_API_KEY = os.environ["OPEN_API_KEY"]

RULES = '''Я буду задавать вопросы о  %(name)s. Отвечай как сценарист видео рассказывающего о %(name)s в третьем лице как о профессионале. Видео должно оставлять хорошее впечатление. Ответ должен включать закадровый голос не больше двух предложений и описание слайда не больше 6 слов. В каде должен описываться обычный предмет, который можно купить в магазине или пейзаж. Формат ответов
Закадровый голос: текст для закадрового голоса для первой сцены
Кадр: короткое описание не больше 6 слов
'''

INITIAL_QUESTION = '''Первый вопрос: Какие услуги оказывает %(name)s?'''


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
