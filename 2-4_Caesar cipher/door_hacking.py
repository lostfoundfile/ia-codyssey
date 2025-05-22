import zipfile
import itertools
import string
import time
from multiprocessing import Process, Event, Value, Queue, cpu_count

ZIP_PATH = "emergency_storage_key.zip"
CHARSET = string.ascii_lowercase + string.digits
LENGTH = 6
NUM_PROCESSES = cpu_count()  # 사용할 CPU 수

def try_passwords(start_idx, end_idx, found_event, result, attempts, queue):
    total = len(CHARSET) ** LENGTH
    charset = CHARSET

    def index_to_password(i):
        pwd = []
        for _ in range(LENGTH):
            i, r = divmod(i, len(charset))
            pwd.append(charset[r])
        return ''.join(reversed(pwd))

    try:
        with zipfile.ZipFile(ZIP_PATH) as zf:
            for i in range(start_idx, end_idx):
                if found_event.is_set():
                    break

                password = index_to_password(i)
                attempts.value += 1

                try:
                    zf.extractall(pwd=bytes(password, 'utf-8'))
                    found_event.set()
                    result.value = 1
                    queue.put(password)
                    break
                except:
                    continue
    except FileNotFoundError:
        print(f"❗ ZIP 파일을 찾을 수 없습니다: {ZIP_PATH}")

def unlock_zip_parallel():
    total = len(CHARSET) ** LENGTH
    chunk_size = total // NUM_PROCESSES
    found_event = Event()
    result = Value('i', 0)
    attempts = Value('i', 0)
    password_queue = Queue()

    print(f"🔓 {ZIP_PATH} 비밀번호 브루트포스 시작 (멀티프로세싱 {NUM_PROCESSES}코어)")
    start_time = time.time()

    processes = []
    for i in range(NUM_PROCESSES):
        start = i * chunk_size
        end = total if i == NUM_PROCESSES - 1 else (i + 1) * chunk_size
        p = Process(target=try_passwords, args=(start, end, found_event, result, attempts, password_queue))
        processes.append(p)
        p.start()

    try:
        while not found_event.is_set():
            time.sleep(5)
            elapsed = time.time() - start_time
            print(f"⏳ {attempts.value}회 시도 중... 경과 시간: {elapsed:.2f}초")
    except KeyboardInterrupt:
        print("⛔ 사용자가 중단했습니다.")
        found_event.set()

    for p in processes:
        p.join()

    if result.value:
        password = password_queue.get()
        print(f"✅ 비밀번호를 찾았습니다: {password}")
        with open('password.txt', 'w') as f:
            f.write(password)
    else:
        print("❌ 비밀번호를 찾지 못했습니다.")

if __name__ == "__main__":
    unlock_zip_parallel()