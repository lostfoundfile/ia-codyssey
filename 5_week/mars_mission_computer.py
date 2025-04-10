import random
import time
import json
import threading
import platform
import os
import psutil


class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.uniform(18, 30)
        self.env_values['mars_base_external_temperature'] = random.uniform(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.uniform(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.uniform(500, 715)
        self.env_values['mars_base_internal_co2'] = random.uniform(0.02, 0.1)
        self.env_values['mars_base_internal_oxygen'] = random.uniform(4, 7)

    def get_env(self):
        return self.env_values


class MissionEnvironmentMonitor:
    def __init__(self, sensor):
        self.env_values = {}
        self.sensor = sensor
        self.time_interval = 5
        self.env_history = []
        self.stop_command = False

    def get_sensor_data(self):
        start_time = time.time()
        while not self.stop_command:
            self.sensor.set_env()
            current_data = self.sensor.get_env()
            self.env_values = current_data
            self.env_history.append(current_data)

            print('Mars Base Environmental Data:')
            print(json.dumps(self.env_values, indent=4))

            if (time.time() - start_time) >= 300:
                self.print_average_values()
                start_time = time.time()

            time.sleep(self.time_interval)

    def print_average_values(self):
        avg_values = {
            key: sum(entry[key] for entry in self.env_history) / len(self.env_history)
            for key in self.env_values
        }

        print("5분 평균치:")
        print(json.dumps(avg_values, indent=4))
        self.env_history = []

    def stop(self):
        self.stop_command = True
        print("Environmental monitoring stopped...")


class MissionComputer:
    def __init__(self):
        # 설정 파일 없이 모든 항목을 출력하도록 고정
        self.settings = []  # 이제 settings는 항상 빈 리스트로 설정

    def get_mission_computer_info(self):
        try:
            full_info = {
                '운영체계': platform.system(),
                '운영체계 버전': platform.version(),
                'CPU 타입': platform.processor(),
                'CPU 코어 수': os.cpu_count(),
                '메모리 크기(GB)': round(psutil.virtual_memory().total / (1024 ** 3), 2)
            }

            print('[미션 컴퓨터 시스템 정보]')
            print(json.dumps(full_info, ensure_ascii=False, indent=4))
            return full_info

        except Exception as e:
            print('시스템 정보를 가져오는 중 오류가 발생했습니다:', str(e))
            return {}

    def get_mission_computer_load(self):
        try:
            full_load = {
                'CPU 실시간 사용량(%)': psutil.cpu_percent(interval=1),
                '메모리 실시간 사용량(%)': psutil.virtual_memory().percent
            }

            print('[미션 컴퓨터 실시간 부하]')
            print(json.dumps(full_load, ensure_ascii=False, indent=4))
            return full_load

        except Exception as e:
            print('부하 정보를 가져오는 중 오류가 발생했습니다:', str(e))
            return {}


class RunComputer:
    def __init__(self):
        self.ds = DummySensor()
        self.env_monitor = MissionEnvironmentMonitor(self.ds)
        self.mission_computer = MissionComputer()

    def start(self):
        # 시스템 정보 및 부하 먼저 출력
        print("\n--- 시스템 정보 및 부하 출력 ---")
        self.mission_computer.get_mission_computer_info()
        self.mission_computer.get_mission_computer_load()

        # 환경 모니터링 시작
        data_thread = threading.Thread(target=self.env_monitor.get_sensor_data)
        data_thread.start()

        while True:
            stop_command = input("Type 'stop' to terminate the system: ").strip().lower()
            if stop_command == 'stop':
                self.env_monitor.stop()
                data_thread.join()
                break


# 실행
if __name__ == '__main__':
    run_computer = RunComputer()
    run_computer.start()