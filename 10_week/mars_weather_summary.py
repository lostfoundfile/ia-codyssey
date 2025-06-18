import csv
import mysql.connector

def create_connection():
    connection = mysql.connector.connect(
        host='localhost',        # 자신의 MySQL 호스트 주소
        user='your_username',    # MySQL 사용자명
        password='your_password',# MySQL 비밀번호
        database='your_database' # 사용할 데이터베이스 이름
    )
    return connection

def create_table(cursor):
    create_table_query = (
        'CREATE TABLE IF NOT EXISTS mars_weather ('
        'weather_id INT AUTO_INCREMENT PRIMARY KEY, '
        'mars_date DATETIME NOT NULL, '
        'temp INT, '
        'storm INT'
        ');'
    )
    cursor.execute(create_table_query)

def insert_data_from_csv(cursor, file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip header
        for row in reader:
            mars_date = row[1]
            temp = int(float(row[2]))  # float → int
            storm = int(row[3])
            insert_query = (
                'INSERT INTO mars_weather (mars_date, temp, storm) '
                'VALUES (%s, %s, %s);'
            )
            cursor.execute(insert_query, (mars_date, temp, storm))

def main():
    file_path = 'mars_weathers_data.CSV'  # 같은 디렉토리에 있어야 함
    connection = create_connection()
    cursor = connection.cursor()

    create_table(cursor)
    insert_data_from_csv(cursor, file_path)

    connection.commit()
    cursor.close()
    connection.close()

if __name__ == '__main__':
    main()