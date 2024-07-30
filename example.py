# from flask import Flask,g,session, request, jsonify, send_file
# from flask_cors import CORS
# import os
# from langdetect import detect
# from pytube import YouTube
# from openai import OpenAI
#
# from dotenv import load_dotenv
# from pymongo import MongoClient
# from flask_bcrypt import check_password_hash, generate_password_hash
# from youtube_transcript_api import YouTubeTranscriptApi
# import threading
# from flask_mail import Mail, Message
# from pydub import AudioSegment
# app = Flask(__name__)
# load_dotenv()
# app.secret_key = '123'
# CORS(app)
# openai_app = OpenAI(
#     api_key=os.getenv('OPENAI_API_KEY')
# )
#
# client = MongoClient('')
# # client  = MongoClient('mongodb://localhost:27017')
# db = client['summarizer']
# print(db)
# thread_count =0
# thread_results = []
#
#
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = 'danielhan04125@gmail.com'
# app.config['MAIL_PASSWORD'] = 'kvla yorb ydcj accf'
#
# mail = Mail(app)
#
# def generate_token(user):
#     # Definir las opciones y configuraciones del token
#     token_payload = {
#         'user_id': str(user['_id']),
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expira en 1 hora
#     }
#     secret_key = 'tuclavesecretadeltoken'  # Cambia esto a tu clave secreta real
#
#     # Generar el token JWT utilizando PyJWT
#     token = jwt.encode(token_payload, secret_key, algorithm='HS256')
#     return token
#
#
#
# def generate_summary(email,url,type):
#
#     user = db['user']
#     existing_user = user.find_one({ "email": email })
#     if(len(existing_user['summary'])>=150):
#         return jsonify({ 'msg': "150 is limitation to generate new summary"}), 409
#
#     def get_video_id_from_url(url):
#         parsed_url = urllib.parse.urlparse(url)
#         return urllib.parse.parse_qs(parsed_url.query)['v'][0]
#
#     try:
#         video_url = url
#         video_id = get_video_id_from_url(video_url)
#     except Exception as e:
#         parsed_url = urllib.parse.urlparse(url)
#         video_id = parsed_url.path.strip('/')
#
#
#     if existing_user:
#         for data in existing_user['summary']:
#             if(data['url'] == video_id):
#                 return { 'video_title': data['data']['video_title'], 'url':video_id ,'isExist':True}
#
#     yt = YouTube(url)
#     audio_stream = yt.streams.filter(only_audio=True).first()
#     thumbnail = ""
#
#     def get_video_title(url):
#         try:
#             yt = YouTube(url)
#             thumbnail = yt.thumbnail_url
#             return yt.title
#         except Exception as e:
#             return f"An error occurred: {e}"
#
#     def get_video_thumnail(url):
#         try:
#             yt = YouTube(url)
#             return yt.thumbnail_url
#         except Exception as e:
#             return f"An error occurred: {e}"
#
#
#     def split_audio(file_path, chunk_length_ms=600000):
#         """Splits the audio file into smaller chunks."""
#         print("split_audio``````````````")
#         audio = AudioSegment.from_file(file_path)
#         chunks = []
#         print(audio)
#         print('audio')
#         for i in range(0, len(audio), chunk_length_ms):
#             chunks.append(audio[i:i + chunk_length_ms])
#             print(i)
#         return chunks
#
#     def transcribe_audio_chunk(chunk, chunk_index):
#         """Transcribes a single audio chunk using OpenAI's Whisper."""
#
#         print("transcribe_audio```````````")
#         global thread_count
#         global thread_results
#         chunk_path = f"chunk_{chunk_index}.mp3"
#         chunk.export(chunk_path, format="mp3")
#         with open(chunk_path, 'rb') as audio_file:
#             transcription = openai_app.audio.transcriptions.create(
#                 model="whisper-1",
#                 file=audio_file,
#                 response_format="text"
#             )
#         os.remove(chunk_path)  # Clean up the temporary chunk file
#         print(transcription)
#         thread_results.append({
#             "index": chunk_index,
#             "text": transcription
#         })
#
#         thread_count += 1
#         return transcription
#
#     def transcribe_audio(audio_file_path):
#         global thread_count
#         global thread_results
#         """Transcribes an audio file, handling large files by splitting them into chunks."""
#         if os.path.getsize(audio_file_path) > 25 * 1024 * 1024:  # Check if the file size is larger than 25MB
#             audio_chunks = split_audio(audio_file_path)
#             print("audio_chunks",audio_chunks)
#             for index, chunk in enumerate(audio_chunks):
#                 print(index)
#                 thread = threading.Thread(target=transcribe_audio_chunk, args=[chunk, index])
#                 thread.start()
#                 # transcription = transcribe_audio_chunk(chunk, index)
#                 # transcriptions.append(transcription)
#             while thread_count != len(audio_chunks):
#                 continue
#             print("continue")
#             sorted_data = sorted(thread_results, key=lambda x: x['index'])
#             text_array = [transcript["text"] for transcript in sorted_data]
#             thread_count = 0
#             thread_results = []
#             return " ".join(text_array)
#         else:
#             with open(audio_file_path, 'rb') as audio_file:
#                 transcription = openai_app.audio.transcriptions.create(
#                     model="whisper-1",
#                     file=audio_file,
#                     response_format="text"
#                 )
#
#             return transcription
#
#
#     def summarize_text():
#
#         file = openai_app.files.create(file= open("./audio_text.txt", 'rb'),purpose= "assistants")
#         assistant = openai_app.beta.assistants.create(name= "Workflow Builder",
#             # instructions= ASSISTANT_INSTRUCTION,
#             tools= [{'type':'retrieval'}],
#             file_ids = [file.id],
#             model= "gpt-4-1106-preview",
#         )
#         thread = openai_app.beta.threads.create()
#         message = openai_app.beta.threads.messages.create(
#             thread_id= thread.id,
#             role= "user",
#             content= """You are a highly skilled AI trained in Youtube video comprehension and summarization.   you will summarize in English
#                         You will response like "This video discussed about..."
#                         you will response the summary of  the video in English. you should talk about the video summary.
#                         For the long videos, you will provide the long summary.
#                         Please Provide the long summary as much as you can if you think video is not short. It's important feature.
#                         you don't mention about text or transcription.
#                         summary  should contain <br/><br/> tags to make some paragraphs and separate each paragraphs.
#                      """
#         )
#         MESSAGE_INSTRUCTION = """
#            You are a highly skilled AI trained in Youtube video comprehension and summarization.you will summarize in English
#            You will response like "This video discussed about..."
#            You will response a coherent and readable summary that could help a person understand the summary of Youtube video.
#            you should talk about the video summary. you don't mention about text or transcription.
#            Please Provide the long summary as much as you can if you think video is not short. It's important feature.
#            summary  should contain <br/><br/> tags to make some paragraphs and separate each paragraphs.
#            For the long videos, you will provide the long summary.
#            and summary  should contain <br/><br/> tags to make some paragraphs and separate each paragraphs.
#         """
#         run = openai_app.beta.threads.runs.create(
#             thread_id= thread.id,
#             assistant_id= assistant.id,
#             instructions= MESSAGE_INSTRUCTION,
#         )
#
#         while run.status != "completed":
#             run = openai_app.beta.threads.runs.retrieve(
#                 thread_id= thread.id,
#                 run_id= run.id
#             )
#             if run.status == "completed":
#                 break
#         all_messages = openai_app.beta.threads.messages.list(
#             thread_id=thread.id
#         )
#         res_message = all_messages.data[0].content[0].text.value
#         return res_message
#
#     video_url = url
#     video_title = get_video_title(video_url)
#     print(f'The title of the video is: {video_title}')
#     if type == 1:
#         print('whisper')
#         output_path = "YoutubeAudios"
#         filename = "audio.mp3"
#         audio_stream.download(output_path=output_path, filename=filename)
#         audio_url = output_path+"/"+filename
#         if os.path.getsize(audio_url) > 25 * 1024 * 1024:
#             print("long text exception")
#             thumbnail = get_video_thumnail(video_url)
#             long_text_summary = "It's too difficult to get the summary. Please contact to me: summary@tldw.ai/"
#             new_summary = { 'video_title': video_title,'thumbnail':thumbnail, 'content':long_text_summary}
#             result = user.update_one({ "email": email }, { "$push": { "summary": {'data':new_summary, 'url':video_id,'isExist':False} }},)
#             return { 'video_title': video_title, 'url':video_id}
#         transcribed_text = transcribe_audio(audio_url)
#         with open("./audio_text.txt", 'w') as file:
#             file.write(transcribed_text)
#         final_summary =  summarize_text()
#         with open('./summary.txt', 'w', encoding='utf-8') as summary_file:
#             summary_file.write(final_summary)
#         thumbnail = get_video_thumnail(video_url)
#         new_summary = { 'video_title': video_title,'thumbnail':thumbnail, 'content':final_summary}
#         result = user.update_one({ "email": email }, { "$push": { "summary": {'data':new_summary, 'url':video_id,'isExist':False} }},)
#         return { 'video_title': video_title, 'url':video_id}
#     else:
#         print("YouTubeAPI")
#         text = YouTubeTranscriptApi.get_transcript(video_id)
#         transcribed_text = ' '.join([entry['text'] for entry in text])
#         with open("./audio_text.txt", 'w') as file:
#             file.write(transcribed_text)
#         final_summary =  summarize_text()
#         with open('./summary.txt', 'w', encoding='utf-8') as summary_file:
#             summary_file.write(final_summary)
#         thumbnail = get_video_thumnail(video_url)
#         new_summary = { 'video_title': video_title,'thumbnail':thumbnail, 'content':final_summary}
#         result = user.update_one({ "email": email }, { "$push": { "summary": {'data':new_summary, 'url':video_id,'isExist':False} }},)
#         return { 'video_title': video_title, 'url':video_id}
#
#
#
#
#
#
#
# @app.route('/user/getsummarydata', methods=['POST'])
# def getSummary():
#     print("getSummarydata")
#     email = request.json['email']
#     url = request.json['url']
#     print(email, url)
#     # userData= User.objects(email = email).first()
#     user = db['user']
#     userData = user.find_one({ "email": email })
#
#     if not userData:
#         print('no data')
#         return jsonify({'error': 'not userdata found'}), 409
#
#     for data in userData['summary']:
#         if(data['url'] == url):
#             print(data)
#             return jsonify({ 'data': data})
#     video_URL = "https://youtu.be/"+url
#     data = generate_summary(email,video_URL)
#     userData = user.find_one({ "email": email })
#     print(userData)
#     for data in userData['summary']:
#         if(data['url'] == url):
#
#             return jsonify({ 'data': data})
#
# @app.route('/sendmail', methods=['POST'])
# def send_email():
#     print("mail")
#     email = request.json['email']
#     name = request.json['name']
#     message = request.json['message']
#     print("sent")
#     msg = Message(f'Contact message from {name}',
#                   sender='radu.vrabie@gmail.com',
#                   recipients=[f'radu.vrabie@gmail.com'])
#     msg.body = f"{message}\n User Email:{email}"
#     mail.send(msg)
#
#     return jsonify("success"), 200
#
#
# @app.route('/user/getalltitle', methods=['POST'])
# def getAllTitle():
#
#     email = request.json['email']
#     print(email)
#     user = db['user']
#     userData = user.find_one({ "email": email })
#
#     if not userData:
#         print('no data')
#         return jsonify({'error': 'not userdata found'}), 409
#     result = []
#     for data in reversed(userData['summary'][-5:]):
#         result.append({'video_title':data['data']['video_title'],'url':data['url']})
#     print(result)
#     return jsonify({ 'data': result})
#
#
#
# @app.route('/user/getalltitle', methods=['Get'])
# def getTitle():
#
#     email = request.json['email']
#     print(email)
#     user = db['user']
#     userData = user.find_one({ "email": email })
#
#     if not userData:
#         print('no data')
#         return jsonify({'error': 'not userdata found'}), 409
#     result = []
#     for data in userData['summary']:
#         result.append({'video_title':data['data']['video_title'],'url':data['url']})
#     print(result)
#     return jsonify({ 'data': result})
#
#
#
# @app.route('/user/signup', methods=['POST'])
# def create_user():
#     print("signup request")
#     email = request.json['email']
#     password = generate_password_hash(request.json['password'])
#
#     user = db['user']
#     existing_email = user.find_one({ "email": email })
#     if existing_email:
#         print('existing email')
#         return jsonify({'error': 'email is already used'}), 409
#     user.insert_one({ "email": email, "password": password,"summary":[]})
#     return jsonify({ "msg": "okay" })
#
#
# @app.route('/user/signin', methods=['POST'])
# def login():
#     print("login")
#     data = request.get_json()
#     email = data['email']
#     password = data['password']
#
#     # user = User.objects(email=email).first()
#     user = db['user']
#     existUser = user.find_one({ "email": email })
#     if existUser and check_password_hash(existUser['password'], password):
#         token = generate_token(existUser)
#         print("registered user")
#         return jsonify({'token': token, "email": str(existUser['email'])}), 200
#
#     print("invalid uer")
#     return jsonify({'error': 'invalid user'}), 401
#
#
#
#
# @app.route('/getSummery', methods=['POST'])
# def getSummery():
#     try:
#         data = request.get_json()
#         url = data['url']
#         email = data['email']
#         print(email)
#         data = generate_summary(email, url,0)
#         print("youtube api end")
#         return jsonify(data),200
#     except Exception as e:
#         print(f"{e}")
#         data = request.get_json()
#         url = data['url']
#         email = data['email']
#         print(email)
#         data = generate_summary(email, url,1)
#         print('whisper end')
#         return jsonify(data),200
#
# if __name__ == '__main__':
#    app.run(host='0.0.0.0',port=5000)
#    app.run(debug=True)
#