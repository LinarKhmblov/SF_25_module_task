from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from settings import USER_EMAIL, USER_PASSWORD, USER_NAME



def test_check_users_pets_data(driver):
    """Проверка списка питомцев пользователя"""

    # Ввод email
    driver.find_element(By.ID, 'email').send_keys(USER_EMAIL)

    # Ввод пароля
    driver.find_element(By.ID, 'pass').send_keys(USER_PASSWORD)

    # Нажимаем на кнопку входа в аккаунт
    enter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
    enter_button.click()

    # Проверка перехода на главную страницу пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Нажимаем на кнопку "Мои питомцы"
    mypets_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nav-link')))
    mypets_button.click()

    # Проверка перехода во раздел "Мои питомцы"
    assert driver.find_element(By.TAG_NAME, 'h2').text == USER_NAME

    # Получения значения счетчика количества питомцев пользователя
    pet_info = driver.find_element(By.CSS_SELECTOR, 'div.left:nth-child(1)').text.split('\n')[1]
    number_of_pets = int("".join(filter(str.isdigit, pet_info)))

    # Проверяем соответствие счетчика количества питомцев количеству строк с питомцами пользователя
    assert len(driver.find_elements(By.CSS_SELECTOR, 'tbody tr')) == number_of_pets

    image = driver.find_elements(By.CSS_SELECTOR, 'tr th[scope=row] img')
    name = driver.find_elements(By.CSS_SELECTOR, 'td:nth-child(2)')
    breed = driver.find_elements(By.CSS_SELECTOR, 'td:nth-child(3)')
    age = driver.find_elements(By.CSS_SELECTOR, 'td:nth-child(4)')

    num_photos_pets = 0
    count_names = len(name)
    name_list = []
    age_list = []
    breed_list = []

    for i in range(count_names):
        assert name[i].text != ''
        name_list.append(name[i].text)
        if image[i].get_attribute('src'):
            num_photos_pets += 1
        assert breed[i].text != ''
        breed_list.append(breed[i].text)
        assert age[i].text != ''
        age_list.append(age[i].text)

        # Проверка данных питомцев соответствию граничным значениям
        assert 0 <= len(age[i].text) < 100, 'Данные возраста не соответствуют граничным значениям'
        assert 0 < len(name[i].text) <= 255, 'Данные имени не соответствуют граничным значениям'
        assert 0 < len(breed[i].text) <= 255, 'Данные породы не соответствуют граничным значениям'

    # Проверка уникальности имен, возроста, породы
    assert len(name_list) == len(set(name_list)), 'Есть не уникальные имена питомцев'
    assert len(age_list) == len(set(age_list)), 'Есть не уникальные возраста питомцев'
    assert len(breed_list) == len(set(breed_list)), 'Есть не уникальные породы питомцев'

    # Проверка, что хотя бы у половины питомцев есть фото
    assert count_names / 2 >= float(num_photos_pets), 'Фотографии есть больше чем у половины питомцев'



