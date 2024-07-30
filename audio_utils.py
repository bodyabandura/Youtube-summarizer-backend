import threading
from pydub import AudioSegment
import ssl
from config import *


ssl._create_default_https_context = ssl._create_stdlib_context


def split_audio(file_path, chunk_length_ms=600000):
    """Splits the audio file into smaller chunks."""
    print("============== SPLIT AUDIO ==============")
    audio = AudioSegment.from_file(file_path)
    chunks = []

    print('AUDIO', audio)
    for i in range(0, len(audio), chunk_length_ms):
        chunks.append(audio[i:i + chunk_length_ms])
        print(i)

    return chunks


def transcribe_audio_chunk(chunk, chunk_index):
    """Transcribes a single audio chunk using OpenAI's Whisper."""
    print("============== TRANSCRIBE AUDIO ==============")
    global thread_count
    global thread_results

    chunk_path = f"chunk_{chunk_index}.mp3"
    chunk.export(chunk_path, format="mp3")
    with open(chunk_path, 'rb') as audio_file:
        transcription = openai_app.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )

    os.remove(chunk_path)
    print(transcription)

    thread_results.append({
        "index": chunk_index,
        "text": transcription
    })

    thread_count += 1
    return transcription


def file_bigger_than_25mb(file_path):
    return os.path.getsize(file_path) > 25 * 1024 * 1024


def transcribe_audio(audio_file_path):
    global thread_count
    global thread_results
    """Transcribes an audio file, handling large files by splitting them into chunks."""
    if file_bigger_than_25mb(audio_file_path):
        audio_chunks = split_audio(audio_file_path)
        print("AUDIO CHUNKS", audio_chunks)
        for index, chunk in enumerate(audio_chunks):
            print(index)
            thread = threading.Thread(target=transcribe_audio_chunk, args=[chunk, index])
            thread.start()
            # transcription = transcribe_audio_chunk(chunk, index)
            # transcriptions.append(transcription)

        while thread_count != len(audio_chunks):
            continue

        print("CONTINUE")
        sorted_data = sorted(thread_results, key=lambda x: x['index'])
        text_array = [transcript["text"] for transcript in sorted_data]
        thread_count = 0
        thread_results = []
        return " ".join(text_array)
    else:
        with open(audio_file_path, 'rb') as audio_file:
            transcription = openai_app.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="text"
            )

        return transcription
