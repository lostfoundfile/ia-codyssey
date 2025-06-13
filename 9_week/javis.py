import os
import datetime
import wave
import csv
import pyaudio
import speech_recognition as sr


def create_records_folder():
    if not os.path.exists('records'):
        os.mkdir('records')


def get_timestamp():
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d-%H%M%S')


def record_audio(duration=5):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    audio = pyaudio.PyAudio()

    stream = audio.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

    print('Recording...')

    frames = []

    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    print('Finished recording.')

    stream.stop_stream()
    stream.close()
    audio.terminate()

    timestamp = get_timestamp()
    filename = f'records/{timestamp}.wav'

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print(f'Saved as {filename}')


def list_recordings_by_date(start_date, end_date):
    files = os.listdir('records')
    files = [f for f in files if f.endswith('.wav')]

    start = datetime.datetime.strptime(start_date, '%Y%m%d')
    end = datetime.datetime.strptime(end_date, '%Y%m%d')

    print(f'Recordings from {start_date} to {end_date}:')

    for f in sorted(files):
        file_date_str = f.split('-')[0]
        file_date = datetime.datetime.strptime(file_date_str, '%Y%m%d')
        if start <= file_date <= end:
            print(f)


def transcribe_audio(file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        print(f'Transcribing {file_path} ...')
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data, language='ko-KR')
        except sr.UnknownValueError:
            text = '[Unrecognized Speech]'
        except sr.RequestError:
            text = '[API Error]'

    return text


def transcribe_all_recordings():
    files = os.listdir('records')
    wav_files = [f for f in files if f.endswith('.wav')]

    for wav_file in wav_files:
        wav_path = os.path.join('records', wav_file)
        text = transcribe_audio(wav_path)

        csv_file = wav_file.replace('.wav', '.csv')
        csv_path = os.path.join('records', csv_file)

        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['시간', '텍스트'])
            writer.writerow(['00:00:00', text])

        print(f'Transcription saved to {csv_path}')


def search_keyword_in_transcripts(keyword):
    files = os.listdir('records')
    csv_files = [f for f in files if f.endswith('.csv')]

    print(f'\nSearching for "{keyword}" in transcripts:')

    for csv_file in csv_files:
        path = os.path.join('records', csv_file)
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                if keyword in row[1]:
                    print(f'{csv_file} [{row[0]}] : {row[1]}')


def main():
    create_records_folder()

    while True:
        print('\n1. Record Audio')
        print('2. List Recordings by Date Range')
        print('3. Transcribe All Recordings to CSV')
        print('4. Search Keyword in Transcripts')
        print('5. Exit')

        choice = input('Choose an option: ')

        if choice == '1':
            duration = input('Enter duration in seconds (default 5): ')
            if not duration.isdigit():
                duration = 5
            else:
                duration = int(duration)
            record_audio(duration)
        elif choice == '2':
            start = input('Enter start date (YYYYMMDD): ')
            end = input('Enter end date (YYYYMMDD): ')
            list_recordings_by_date(start, end)
        elif choice == '3':
            transcribe_all_recordings()
        elif choice == '4':
            keyword = input('Enter keyword to search: ')
            search_keyword_in_transcripts(keyword)
        elif choice == '5':
            break
        else:
            print('Invalid choice. Try again.')


if __name__ == '__main__':
    main()