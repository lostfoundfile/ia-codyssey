import random
import time
import json
import threading

class DummySensor:
    def __init__(self):
        # 환경 데이터를 저장할 사전 초기화
        self.env_values = {
            'mars_base_internal_temperature': 0,  # 내부 온도
            'mars_base_external_temperature': 0,  # 외부 온도
            'mars_base_internal_humidity': 0,     # 내부 습도
            'mars_base_external_illuminance': 0,  # 외부 광량
            'mars_base_internal_co2': 0,          # 내부 CO2
            'mars_base_internal_oxygen': 0        # 내부 산소
        }

    def set_env(self):
        # 랜덤 값으로 환경 데이터 설정
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)  # 18~30도
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)   # 0~21도
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)     # 50~60%
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)  # 500~715 W/m2
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)       # 0.02~0.1%
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)         # 4~7%

    def get_env(self):
        # 환경 데이터를 반환
        return self.env_values


class MissionComputer:
    def __init__(self, sensor):
        self.env_values = {}
        self.sensor = sensor
        self.running = True
        self.time_interval = 5  # 5초 간격
        self.env_history = []  # 5분 평균을 계산할 데이터 기록용 리스트
        self.last_avg_time = time.time()  # 마지막 평균 출력 시간을 추적
        self.stop_command = False  # 종료 플래그

    def get_sensor_data(self):
        start_time = time.time()
        while not self.stop_command:
            self.sensor.set_env()
            current_data = self.sensor.get_env()
            self.env_values = current_data
            self.env_history.append(current_data)

            # 5초마다 환경 정보 출력
            print('Mars Base Environmental Data:')
            print(json.dumps(self.env_values, indent=4))

            # 5분마다 평균값 출력
            if (time.time() - start_time) >= 300:  # 5분 (300초) 이상 경과 후
                self.print_average_values()
                start_time = time.time()  # 평균값 출력 후 타이머 초기화

            # 5초 대기
            time.sleep(self.time_interval)

    def print_average_values(self):
        # 5분간의 데이터를 평균내어 출력
        avg_values = {
            'mars_base_internal_temperature': sum([entry['mars_base_internal_temperature'] for entry in self.env_history]) / len(self.env_history),
            'mars_base_external_temperature': sum([entry['mars_base_external_temperature'] for entry in self.env_history]) / len(self.env_history),
            'mars_base_internal_humidity': sum([entry['mars_base_internal_humidity'] for entry in self.env_history]) / len(self.env_history),
            'mars_base_external_illuminance': sum([entry['mars_base_external_illuminance'] for entry in self.env_history]) / len(self.env_history),
            'mars_base_internal_co2': sum([entry['mars_base_internal_co2'] for entry in self.env_history]) / len(self.env_history),
            'mars_base_internal_oxygen': sum([entry['mars_base_internal_oxygen'] for entry in self.env_history]) / len(self.env_history)
        }

        print("5분 평균치:")
        print(json.dumps(avg_values, indent=4))

        # 5분치 데이터가 쌓였으므로 기록 초기화
        self.env_history = []

    def stop(self):
        self.stop_command = True
        print("System stopped...")


class RunComputer:
    def __init__(self):
        self.ds = DummySensor()
        self.mission_computer = MissionComputer(self.ds)

    def start(self):
        # 스레드를 사용하여 get_sensor_data를 백그라운드에서 실행
        data_thread = threading.Thread(target=self.mission_computer.get_sensor_data)
        data_thread.start()

        # 사용자 입력을 받아 "stop"이 입력되면 시스템을 종료
        while True:
            stop_command = input("Type 'stop' to terminate the system: ").strip().lower()
            if stop_command == 'stop':
                self.mission_computer.stop()
                data_thread.join()  # 데이터 스레드 종료 기다리기
                break


# 프로그램 실행
if __name__ == "__main__":
    run_computer = RunComputer()
    run_computer.start()
