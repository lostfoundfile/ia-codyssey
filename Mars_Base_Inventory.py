import csv
import struct

# CSV 파일을 읽어서 리스트로 변환하는 함수
def read_csv(file_name):
    try:
        with open(file_name, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader)  # 첫 번째 줄은 헤더이므로 건너뛴다
            data = []
            for row in reader:
                data.append(row)
            return header, data
    except FileNotFoundError:
        print(f"Error: {file_name} not found.")
        return [], []
    except Exception as e:
        print(f"Error: {str(e)}")
        return [], []

# CSV 파일을 리스트 형태로 읽어오는 함수 호출
header, data = read_csv('Mars_Base_Inventory_List.csv')

# 데이터를 플래밍 가능 지수(Flammability) 기준으로 내림차순 정렬하는 함수
def sort_by_flammability(data):
    try:
        data_sorted = sorted(data, key=lambda x: float(x[4]), reverse=True)
        return data_sorted
    except ValueError:
        print("Error: Flammability data conversion failed.")
        return []

# 인화성 지수가 0.7 이상인 물질만 필터링
def filter_dangerous_items(data):
    dangerous_items = []
    for item in data:
        try:
            flammability = float(item[4])
            if flammability >= 0.7:
                dangerous_items.append(item)
        except ValueError:
            continue
    return dangerous_items

# CSV 파일로 저장하는 함수
def write_to_csv(file_name, header, data):
    try:
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # 헤더 작성
            writer.writerows(data)   # 데이터 작성
    except Exception as e:
        print(f"Error: {str(e)}")

# 출력
print("전체 물질 목록:")
for row in data:
    print(row)

# 1. 화물 목록을 인화성 지수 순으로 정렬
sorted_data = sort_by_flammability(data)

# 2. 인화성 지수가 0.7 이상인 목록 필터링
dangerous_items = filter_dangerous_items(sorted_data)

# 3. 인화성 지수가 0.7 이상인 목록을 CSV 포맷으로 저장
write_to_csv('Mars_Base_Inventory_danger.csv', header, dangerous_items)

# 4. 필터링된 위험한 물질 목록 출력
print("\n인화성 지수가 0.7 이상인 물질 목록:")
for row in dangerous_items:
    print(row)

# 보너스 과제: 이진 파일로 저장 (인화성 순으로 정렬된 배열 저장)
def save_as_binary(file_name, data):
    try:
        with open(file_name, 'wb') as file:
            for row in data:
                # 각 항목을 이진 형식으로 변환하여 저장
                for item in row:
                    # 데이터를 utf-8로 인코딩한 뒤 이진 형식으로 변환하여 저장
                    encoded_item = item.encode('utf-8')
                    file.write(struct.pack('I', len(encoded_item)))  # 길이 정보 저장
                    #file.write(encoded_item)  # 실제 데이터 저장
                file.write(b'\n')  # 각 행의 끝에 줄바꿈 추가
    except Exception as e:
        print(f"Error: {str(e)}")

# 인화성 순으로 정렬된 데이터를 이진 파일로 저장
save_as_binary('Mars_Base_Inventory_List.bin', sorted_data)

def read_binary(file_name):
    try:
        with open(file_name, 'rb') as file:
            while True:
                # 한 항목의 길이를 먼저 읽어들임
                length_data = file.read(4)  # 길이는 4바이트
                if not length_data:
                    break  # 파일 끝에 도달했을 경우 종료

                length = struct.unpack('I', length_data)[0]  # 길이 정보 해석
                item_data = file.read(length)  # 해당 길이만큼 읽음

                # 읽어들인 데이터는 그대로 출력 (바이너리 데이터)
                print(item_data, end=' ')
            print()  # 마지막에 줄바꿈 추가
    except Exception as e:
        print(f"Error: {str(e)}")


# 이진 파일에서 읽어들여 UTF-8로 변환하여 출력하는 함수
'''
def read_binary(file_name):
    try:
        with open(file_name, 'rb') as file:
            while True:
                # 한 항목의 길이를 먼저 읽어들임
                length_data = file.read(4)  # 길이는 4바이트
                if not length_data:
                    break  # 파일 끝에 도달했을 경우 종료

                length = struct.unpack('I', length_data)[0]  # 길이 정보 해석
                item_data = file.read(length)  # 해당 길이만큼 읽음

                # 읽어들인 데이터는 utf-8로 디코딩하여 출력
                print(item_data.decode('utf-8'), end=' ')
            print()  # 마지막에 줄바꿈 추가
    except Exception as e:
        print(f"Error: {str(e)}")
'''        
# 이진 파일 내용 읽기
read_binary('Mars_Base_Inventory_List.bin')

