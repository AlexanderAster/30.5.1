import pytest 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # библиотека для вызова ожиданий
from selenium.webdriver.support import expected_conditions as EC # дополнение к WebDriverWait
from selenium.webdriver.common.by import By # для компактности кода и сокращений By.ID/XPATH
 
@pytest.fixture(autouse=True)
def driver(): # отработает в начале каждого теста
   driver = webdriver.Firefox()
   driver.implicitly_wait(10)
   driver.get('https://petfriends.skillfactory.ru/login')
   yield driver
   driver.quit()
 
def test_show_all_pets(driver):
   '''Тест успешной авторизации на сайте'''
   driver.find_element(By.ID, 'email').send_keys('Email')
   driver.find_element(By.ID, 'pass').send_keys('Password')
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

def test_find_card_elements(driver):
   '''Набор тестов для карточек раздела "Все питомцы"'''
   test_show_all_pets(driver)
   images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top') # находит картинки карточек/ожидание
   names = driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-title') # находит имена в карточках/ожидание
   descriptions = driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-text') # находит породу и возраст/ожидание
   for i in range(len(names)): # цикл проверки всех карточек на странице
      image_source = images[i].get_attribute('src') # переменная для проверки картинки
      name_text = names[i].text # переменная для проверки имени
      print(f"Image source: {image_source}") # отобразится в консоли для пояснения объекта упавшего теста - картинка
      print(f"Name text: {name_text}") # отобразится в консоли для пояснения объекта упавшего теста - имя
      assert image_source != '' # проверка,что картинка не пуста
      assert names[i].text != '' # проверка,что имя не пустое
      assert descriptions[i].text != '' # проверка,что строка породы и возраста не пуста
      assert ', ' in descriptions[i] # проверка,что в строке породы и возраста есть запятая
      parts = descriptions[i].text.split(", ") # соединит значения строки породы и возраста,разделив запятой
      assert len(parts[0]) > 0 #  проверка,что первое значение строки породы и возраста - не пустое
      assert len(parts[1]) > 0 #  проверка,что второе значение строки породы и возраста - не пустое

def tests_myPets_table(driver): 
   '''Набор тестов для таблицы "Мои питомцы"'''
   test_show_all_pets(driver) # инициализация авторизации на странице
   wait = WebDriverWait(driver,10) # задаём переменную для работы с явными ожиданиями
   wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Мои питомцы")]')))
   driver.find_element(By.XPATH, '//a[contains(text(), "Мои питомцы")]').click() # переходим к списку личных питомцев
   assert driver.current_url == 'https://petfriends.skillfactory.ru/my_pets' # проверка,что мы на странице личных питомцев
 # Ожидаем загрузку необходимых для теста элементов 
   wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class=".col-sm-4 left"]')))
   wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')))
   wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')))
   wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')))
   wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')))

   statistics = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split("\n") # берём массив 
   # - статистики пользователя
   statistics_split = statistics[1].split(" ")
   quantity_of_pets = int(statistics_split[-1]) # берём из массива счётчик питомцев
   images_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img') # берём фото карточек
   name_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]') # берём имена
   breed_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]') # берём породы
   age_pets = driver.find_elements(By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]') # берём возраст
   assert quantity_of_pets == len(name_pets) # проверка,что счётчик питомцев равен кол-ву питомцев на сайте
   list_name_pets = [None] # заводим список имён питомцев
   count_image = 0 # заводим счётчик картинок
   for i in range(len(name_pets)): # цикл проверки карточек всех питомцев
      assert name_pets[i].text != '' # проверка,что поле имени не пустует
      list_name_pets.append(name_pets[i].text) # добавляем это имя в список
      assert breed_pets[i].text != '' # проверка,что поле породы не пустует
      assert age_pets[i].text != '' # проверка,что поле возраста не пустует
      image_source = images_pets[i].get_attribute('src')
      if image_source != '': # если картинка есть,то пополняем счётчик на единицу
         count_image = count_image + 1 
      else: # иначе проверка,что поле картинки не пустует
         assert image_source != '' 
   assert count_image >= quantity_of_pets/2 # проверка,что картинки есть минимум у половины питомцев
   assert len(set(list_name_pets)) == len(list_name_pets) # проверка,что все имена уникальные
# Запуск : python -m pytest --driver Firefox --driver-path C:\\geckodriver.exe  test_selenium_PetFriendsSet.py