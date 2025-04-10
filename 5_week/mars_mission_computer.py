import platform
import os
import json
import psutil


class MissionComputer:
    def __init__(self):
        self.settings = self.load_settings()

    def load_settings(self):
        """
        setting.txt 파일을 읽어 필요한 출력 항목을 리스트로 반환
        """
        try:
            with open('setting.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()
                return [line.strip() for line in lines if line.strip()]
        except FileNotFoundError:
            print('설정 파일(setting.txt)을 찾을 수 없습니다. 전체 항목을 출력합니다.')
            return []

    def get_mission_computer_info(self):
        """
        시스템 기본 정보를 가져오고 설정에 따라 JSON 형식으로 출력합니다.
        """
        try:
            full_info = {
                '운영체계': platform.system(),
                '운영체계 버전': platform.version(),
                'CPU 타입': platform.processor(),
                'CPU 코어 수': os.cpu_count(),
                '메모리 크기(GB)': round(psutil.virtual_memory().total / (1024 ** 3), 2)
            }

            filtered_info = {
                key: value for key, value in full_info.items()
                if not self.settings or key in self.settings
            }

            json_info = json.dumps(filtered_info, ensure_ascii=False, indent=4)
            print('[미션 컴퓨터 시스템 정보]')
            print(json_info)
            return filtered_info

        except Exception as e:
            print('시스템 정보를 가져오는 중 오류가 발생했습니다:', str(e))
            return {}

    def get_mission_computer_load(self):
        """
        시스템 실시간 부하 정보를 가져오고 설정에 따라 JSON 형식으로 출력합니다.
        """
        try:
            full_load = {
                'CPU 실시간 사용량(%)': psutil.cpu_percent(interval=1),
                '메모리 실시간 사용량(%)': psutil.virtual_memory().percent
            }

            filtered_load = {
                key: value for key, value in full_load.items()
                if not self.settings or key in self.settings
            }

            json_load = json.dumps(filtered_load, ensure_ascii=False, indent=4)
            print('[미션 컴퓨터 실시간 부하]')
            print(json_load)
            return filtered_load

        except Exception as e:
            print('부하 정보를 가져오는 중 오류가 발생했습니다:', str(e))
            return {}


if __name__ == '__main__':
    runComputer = MissionComputer()
    runComputer.get_mission_computer_info()
    runComputer.get_mission_computer_load()
