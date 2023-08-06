"""Provides ring for ChatOpenAI models, such as gpt-3.5-turbo"""
from langchain.chat_models import ChatOpenAI

from .openai import OpenAIRing


class ChatOpenAIRing(OpenAIRing):

    MODEL = ChatOpenAI
