from config import *
from youtube_transcript_api import YouTubeTranscriptApi
from video_utils import *
from audio_utils import *


def generate_summary(data):
    # user = db['users']
    # existing_user = user.find_one({"email": email})
    # if len(existing_user['summary']) >= 150:
    #     return jsonify({'msg': "150 is limitation to generate new summary"}), 409

    # if existing_user:
    #     for data in existing_user['summary']:
    #         if data['url'] == video_id:
    #             return {
    #                 'video_title': data['data']['video_title'],
    #                 'url': video_id,
    #                 'isExist': True
    #             }

    url_, email = data['url'], data['email']

    try:
        yt = YouTube(url_)
        audio_stream = yt.streams.filter(only_audio=True).first()

        video_title = get_video_title(url_)
        print(f'The title of the video is: {video_title}')

        output_path = "YoutubeAudios"
        filename = "audio.mp3"

        audio_stream.download(output_path=output_path, filename=filename)
        audio_url = output_path + "/" + filename

        transcribed_text = transcribe_audio(audio_url)
        print(transcribed_text)

        with open("audio_text.txt", 'w') as f:
            f.write(transcribed_text)

        final_summary = summarize_text()

        with open('summary.txt', 'w', encoding='utf-8') as summary_f:
            summary_f.write(final_summary)

        thumbnail = get_video_thumbnail(url_)

        return {
            "video_title": video_title,
            "thumbnail": thumbnail,
            "content": final_summary,
            "url": url_
        }
    except Exception as e:
        return {
            "message": f"An error occured in generate_summary: {e}"
        }

        # if file_bigger_than_25mb(audio_url):
        #     print("long text exception")
        #     thumbnail = get_video_thumbnail(video_url)
        #     new_summary = {
        #         'video_title': video_title,
        #         'thumbnail': thumbnail,
        #         'content': LONG_TEXT_SUMMARY
        #     }
    #
    #         result = user.update_one({
    #             "email": email
    #         },
    #             {
    #                 "$push": {
    #                     "summary": {
    #                         'data': new_summary,
    #                         'url': video_id,
    #                         'isExist': False
    #                     }
    #                 }
    #             }
    #         )
    #         return {
    #             'video_title': video_title,
    #             'url': video_id
    #         }
    #



    #
    #     result = user.update_one(
    #         {
    #             "email": email
    #         },
    #         {
    #             "$push":
    #                 {
    #                     "summary":
    #                         {
    #                             'data': new_summary,
    #                             'url': video_id,
    #                             'isExist': False
    #                         }
    #                 }
    #         }
    #     )
    #     return {
    #         'video_title': video_title,
    #         'url': video_id
    #     }
    # else:
    #     print("YouTubeAPI")
    #     text = YouTubeTranscriptApi.get_transcript(video_id)
    #     # transcribed_text = ' '.join(entry['text'] for entry in text)
    #
    #     with open(AUDIO_TEXT_TXT, 'w') as f:
    #         f.write(url)
    #
    #     final_summary = summarize_text()
    #
    #     with open(SUMMARY_TXT, 'w', encoding='utf-8') as summary_file:
    #         summary_file.write(final_summary)
    #
    #     thumbnail = get_video_thumbnail(url)

        # new_summary = {'video_title': video_title, 'thumbnail': thumbnail, 'content': final_summary}

        # result = user.update_one(
        #     {
        #         "email": email
        #     },
        #     {
        #         "$push": {
        #             "summary": {
        #                 'data': new_summary,
        #                 'url': video_id,
        #                 'isExist': False
        #             }
        #         }
        #     }
        # )

        # return {
        #     'video_title': video_title,
        #     'url': video_id
        # }


def get_or_create_assistant():
    if os.path.exists(ASSISTANT_ID_FILE):
        with open(ASSISTANT_ID_FILE, 'r') as f:
            assistant_id = f.read().strip()
            if assistant_id:
                return assistant_id

    # Create a new assistant if not already created
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

    assistant_id = get_or_create_assistant()
    thread = openai_app.beta.threads.create()

    message = openai_app.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content
    )

    run = openai_app.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    while run.status != "completed":
        run = openai_app.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

    all_messages = openai_app.beta.threads.messages.list(thread_id=thread.id)
    assistant = all_messages.data[0].content[0].text.value

    print(f"User: {message.content[0].text.value}")
    print(f"Assistant: {assistant}")

    return assistant


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=5qm8PH4xAss"
    result = generate_summary("example@example.com", url, 0)
    print(result)
