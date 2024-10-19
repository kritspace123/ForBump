from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import threading

url = 'https://ultisport.ru/winterleague2025/games/game/11176'

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(options=options)

Team_Name = []


def Timer(minut, sec):
   # Преобразуем минуты в секунды
   total_seconds = minut * 60 + sec
   # Запускаем обратный отсчет
   while total_seconds > 0:
      # Преобразуем секунды в минуты и секунды
      mins, secs = divmod(total_seconds, 60)
      timer = f'{mins:02}:{secs:02}'  # Форматируем строку в формате MM:SS
      # Открываем файл и записываем оставшееся время
      with open('timer.txt', 'w') as file:
         file.write(timer)
      # Ждем 1 секунду
      time.sleep(1)
      # Уменьшаем количество секунд
      total_seconds -= 1
   # По завершению таймера записываем "00:00" в файл
   with open("countdown_timer.txt", "w") as file:
      file.write("00:00")

def Score():
   # Задаем время, в течение которого будем проверять счет (в секундах, например, 20 минут = 1200 секунд)
   check_time_seconds = 1200
   interval_seconds = 30  # Интервал между проверками в секундах
   
   previous_score = ""

   start_time = time.time()
   while time.time() - start_time < check_time_seconds:
      try:
         score_element = driver.find_element(By.CSS_SELECTOR, 'div._score_3e05930')
         current_score = score_element.text

         if current_score != previous_score:
            score = current_score.split(":")
            
            # Открываем файлы в режиме перезаписи
            with open("Score_Team1.txt", 'w', encoding="utf-8") as Score_Team1, open("Score_Team2.txt", 'w', encoding="utf-8") as Score_Team2:
               # Запись текущего счета в файлы
               Score_Team1.write(score[0].replace(' ', '') + '\n')
               Score_Team2.write(score[1].replace(' ', '') + '\n')
            print(f"Счёт изменился: {current_score}")
            previous_score = current_score  # Обновляем предыдущий счёт
      
      except Exception as e:
         print(f"Ошибка : {e}")
      
      # Ждем указанный интервал перед следующей проверкой
      time.sleep(interval_seconds)


if __name__ == "__main__":
   
   
   try:
      driver.get(url)
      time.sleep(5)
      
      #Парсим название команд
      elements = driver.find_elements(By.CSS_SELECTOR, 'div._info_8c7665c > span._title_b20918a')
      
      for elem in elements:
         Team_Name.append(elem.text)
      
      for index, element in enumerate(Team_Name):
      # Формируем имя файла с индексом элемента
         filename = f"Team{index+1}.txt"
         # Открываем файл с уникальным именем и записываем элемент
         with open(filename, "w", encoding="utf-8") as file:
            file.write(element)
      
      #Парсим таймер      
      time_element = driver.find_element(By.CSS_SELECTOR, 'span._timeLeftUser_ea83b0a._game-status_9395f01')
      
      # Получаем текст элемента
      time_left = time_element.text
      
      time_left_elements = time_left.split(":")

      # Получаем количество минут и секунд
      minutes = int(time_left_elements[0])
      seconds = int(time_left_elements[1])
      
      
      #TODO Нужно запустить таймер во втором потоке
      # Timer(minutes, seconds)
      thread1 = threading.Thread(target=Score)
      thread2 = threading.Thread(target=Timer, args=(minutes, seconds))
      
      thread2.start()
      thread1.start()
      
      # Дожидаемся завершения потоков
      thread1.join()
      thread2.join()      
            
            
   except Exception as ex:
      print(ex)
   finally:
      driver.close()
      driver.quit()