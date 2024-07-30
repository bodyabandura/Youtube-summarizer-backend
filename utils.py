from config import *
from youtube_transcript_api import YouTubeTranscriptApi
from video_utils import *
from audio_utils import *


def generate_summary(data):
    url_, email = data['url'], data['email']

    try:
        yt = YouTube(url_)
        print("1")
        audio_stream = yt.streams.filter(only_audio=True).first()

        print("2")
        video_title = get_video_title(url_)
        print(f'The title of the video is: {video_title}')
        print("3")

        output_path, filename = "YoutubeAudios", "audio.mp3"

        audio_stream.download(output_path=output_path, filename=filename)
        print("4")

        audio_url = output_path + "/" + filename
        print("5")

        transcribed_text = transcribe_audio(audio_url)
        print("6")

        with open("audio_text.txt", 'w') as f:
            f.write(transcribed_text)
        print(transcribed_text)
        print("7")

        final_summary = summarize_text()
        print("8")

        with open('summary.txt', 'w', encoding='utf-8') as summary_f:
            summary_f.write(final_summary)
        print("9")

        thumbnail = get_video_thumbnail(url_)
        print("10")
    except Exception as e:
        return {
            "message": f"An error occured in generate_summary: {e}"
        }

    return {
        "video_title": video_title,
        "thumbnail": thumbnail,
        "content": final_summary,
        "url": url_
    }


def get_or_create_assistant():
    if os.path.exists(ASSISTANT_ID_FILE):
        with open(ASSISTANT_ID_FILE, 'r') as f:
            assistant_id = f.read().strip()
            if assistant_id:
                return assistant_id

    assistant = openai_app.beta.assistants.create(
        name="Video summarizer",
        tools=[{'type': 'file_search'}],
        instructions=MESSAGE_INSTRUCTION,
        model=GPT_MODEL,
    )
    assistant_id = assistant.id
    print("Assistant created with ID:", assistant)

    with open(ASSISTANT_ID_FILE, 'w') as f:
        f.write(assistant_id)

    return assistant_id


def summarize_text():
    with open(AUDIO_TEXT_TXT, 'r') as f:
        content = f.read()
    print("7.1")
    assistant_id = get_or_create_assistant()
    print("7.2")

    thread = openai_app.beta.threads.create()
    print("7.3")

    message = openai_app.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content
    )
    print("7.4")

    run = openai_app.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )
    print("7.5")

    while run.status != "completed":
        run = openai_app.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
    print("7.6")

    all_messages = openai_app.beta.threads.messages.list(thread_id=thread.id)
    print("7.7")

    assistant = all_messages.data[0].content[0].text.value
    print("7.8")

    print(f"User: {message.content[0].text.value}")
    print(f"Assistant: {assistant}")

    return assistant


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=5qm8PH4xAss"
    result = generate_summary("example@example.com", url, 0)
    print(result)
