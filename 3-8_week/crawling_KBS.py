from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def login_to_naver(driver, user_id, user_pw)
    driver.get('httpswww.naver.com')
    time.sleep(2)

    login_button = driver.find_element(By.CLASS_NAME, 'MyView-module__link_login___HpHMW')
    login_button.click()
    time.sleep(2)

    id_field = driver.find_element(By.ID, 'id')
    pw_field = driver.find_element(By.ID, 'pw')

    id_field.send_keys(user_id)
    pw_field.send_keys(user_pw)
    time.sleep(1)

    pw_field.send_keys(Keys.RETURN)
    time.sleep(5)

def get_naver_pay_point(driver)
    driver.get('httpspay.naver.com')
    time.sleep(3)

    try
        point_element = driver.find_element(By.CLASS_NAME, 'MyPoint')
        return [point_element.text]
    except Exception
        return ['로그인된 상태가 아니거나 포인트 정보를 찾을 수 없습니다.']

def main()
    user_id = 'your_naver_id'   # 본인의 네이버 아이디
    user_pw = 'your_naver_pw'   # 본인의 네이버 비밀번호

    driver = webdriver.Chrome()  # 크롬드라이버 PATH 지정 가능
    driver.implicitly_wait(10)

    try
        login_to_naver(driver, user_id, user_pw)
        contents = get_naver_pay_point(driver)

        for content in contents
            print(content)
    finally
        driver.quit()

if __name__ == '__main__'
    main()