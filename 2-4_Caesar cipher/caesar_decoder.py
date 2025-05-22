def caesar_cipher_decode(target_text):
    """
    Caesar cipher 디코딩 함수
    각 자리수(1~25)를 시도하며 디코딩 결과를 출력
    """
    for shift in range(1, 26):
        decoded_text = ''
        for char in target_text:
            if 'a' <= char <= 'z':
                decoded_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            elif 'A' <= char <= 'Z':
                decoded_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decoded_char = char
            decoded_text += decoded_char
        print(f'[자리수 {shift:2}] → {decoded_text}')


def read_password():
    """
    password.txt 파일에서 암호 읽기
    """
    try:
        with open('password.txt', 'r') as f:
            password = f.read().strip()
            print(f'[INFO] password.txt 에서 읽은 암호: {password}')
            return password
    except FileNotFoundError:
        print('[ERROR] password.txt 파일이 없습니다.')
        return None
    except Exception as e:
        print(f'[ERROR] 파일 읽기 오류: {e}')
        return None


def save_result(result_text):
    """
    result.txt에 해독된 최종 암호 저장
    """
    try:
        with open('result.txt', 'w') as f:
            f.write(result_text)
        print('[INFO] result.txt 에 최종 결과 저장 완료.')
    except Exception as e:
        print(f'[ERROR] 결과 저장 실패: {e}')


def main():
    password = read_password()
    if password is None:
        return

    print('\n🔓 가능한 Caesar 해독 결과:\n')
    caesar_cipher_decode(password)

    print('\n👁️ 위 결과 중 정답으로 보이는 "자리수"를 입력하세요 (예: 3):')
    try:
        shift = int(input('>> '))
        if not (1 <= shift <= 25):
            print('[ERROR] 1~25 사이의 정수를 입력하세요.')
            return
    except ValueError:
        print('[ERROR] 숫자가 아닌 입력입니다.')
        return

    # 사용자가 선택한 자리수로 최종 해독
    final_result = ''
    for char in password:
        if 'a' <= char <= 'z':
            decoded_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
        elif 'A' <= char <= 'Z':
            decoded_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:
            decoded_char = char
        final_result += decoded_char

    print(f'\n✅ 선택한 자리수 {shift} → 최종 해독 결과: {final_result}')
    save_result(final_result)


if __name__ == '__main__':
    main()