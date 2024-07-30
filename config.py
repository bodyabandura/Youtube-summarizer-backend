import os
import certifi

from pymongo import MongoClient
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
MONGO_URI = os.getenv('MONGO_URI', )
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

UPDATE_CONFIG_DICT = dict(
    MAIL_SERVER=MAIL_SERVER,
    MAIL_PORT=MAIL_PORT,
    MAIL_USE_SSL=MAIL_USE_SSL,
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD
)

thread_count, thread_results = 0, []
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
openai_app = OpenAI(api_key=OPENAI_API_KEY)

db = client['summarizer']

AUDIO_TEXT_TXT = "audio_text.txt"
SUMMARY_TXT = 'summary.txt'
GPT_MODEL = "gpt-4-1106-preview"
ASSISTANT_ID_FILE = "assistant_id.txt"
_ERROR = "======================== ERROR ========================"
LONG_TEXT_SUMMARY = "It's too difficult to get the summary. Please contact to me: summary@tldw.ai/"
MESSAGE_INSTRUCTION = """
   You are a highly skilled AI trained in Youtube video comprehension and summarization. 
   You will summarize in English
   You will response like "This video discussed about..."
   You will response a coherent and readable summary that could help a person understand the summary of Youtube video. 
   you should talk about the video summary. you don't mention about text or transcription.
   Please Provide the long summary as much as you can if you think video is not short. It's important feature.
   summary  should contain <br/><br/> tags to make some paragraphs and separate each paragraphs.
   For the long videos, you will provide the long summary.
   and summary  should contain <br/><br/> tags to make some paragraphs and separate each paragraphs.
"""
CONTENT = """
    You are a highly skilled AI trained in Youtube video comprehension and summarization. 
    You will summarize in English
    You will response like "This video discussed about..."
    You will response the summary of the video in English. you should talk about the video summary.
    For the long videos, you will provide the long summary. 
    Please Provide the long summary as much as you can if you think video is not short. It's important feature.
    You don't mention about text or transcription.
    Summary  should contain <br/><br/> tags to make some paragraphs and separate each paragraphs.
 """
INSTRUCTIONS_BACKUP = """
        You are given a large piece of text. Your task is to summarize this text by focusing on the main ideas and key points. 
Please ensure the summary captures the essential information and conveys the main message of the text concisely.

1. Identify the main themes and ideas from the text.
2. Provide a brief overview of the text's content.
3. Ensure that the summary is clear and easy to understand.
4. Aim to keep the summary as brief as possible while still conveying the necessary information.

Do not include any unnecessary details or repetitive information in the summary.
"""
