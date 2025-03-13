from datetime import datetime

def read_and_sort_log(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()

            # 첫 번째 줄은 헤더이므로 제외
            headers = lines[0]
            log_entries = lines[1:]

            # 로그 항목을 timestamp 기준으로 내림차순 정렬
            sorted_log_entries = sorted(log_entries, key=lambda x: datetime.strptime(x.split(',')[0], "%Y-%m-%d %H:%M:%S"), reverse=True)

            # 역순으로 출력
            print(headers.strip())
            for entry in sorted_log_entries:
                print(entry.strip())

            # 문제 있는 부분 저장 (예: 산소탱크 폭발)
            with open('problem_logs.txt', 'w', encoding='utf-8') as problem_file:
                for entry in sorted_log_entries:
                    if 'Oxygen tank explosion' in entry:
                        problem_file.write(entry)

    except FileNotFoundError:
        print(f'Error: {file_name} 파일을 찾을 수 없습니다.')
    except Exception as e:
        print(f'예외 발생: {str(e)}')

if __name__ == "__main__":
    # 로그 파일을 읽고 역순 정렬 후 출력
    read_and_sort_log('mission_computer_main.log')
