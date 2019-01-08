from random import randint, choice
from datetime import datetime
import re


def set_grade(shots, errors_num):
    """Фунцкия выставления оценки.
      Считает отношение числа неправильных ответов к числу попыток и выставляет
      соответствующую оценку
      shots - число попыток.
      errors_num - число неправильных ответов.
      Возвращает string
    """
    errors_prop = errors_num / shots
    if errors_prop == 0:
        grade = '5'
    elif errors_prop < 0.15:
        grade = '5-'
    elif errors_prop < 0.3:
        grade = '4'
    elif errors_prop <= 0.5:
        grade = '3'
    else:
        grade = '2'
    return grade


def new_task(difficult = 1):
  """Фунцкия генерирования задания для теста.
    Выбирает случайным образом два числа, операцию между ними, считает
    правильное решение и просит пользователя решить это же задание.
    difficult - сложность задания (по умолчанию = 1)
    Возвращает int
  """
  number_1 = randint(1, 10**difficult)
  number_2 = randint(1, 10**difficult)
  operation = choice(['+','-','*','/'])
  if operation == '/':
    number_1 *= number_2
  request = '{} {} {}'.format(number_1, operation, number_2)
  right_result = eval(request)
  print("Сколько будет {}?".format(request))
  return int(right_result)


def begin_test():
    """Функция возвращает время начала теста
    """
    begin_test_time = datetime.now()
    return begin_test_time


def end_test(begin_test_time):
    """Функция подсчитывает общее время прохождения теста
        begin_test_time - время начала тестирования
    """
    time_log = datetime.now()
    game_time = time_log - begin_test_time
    return game_time


def ask_login():
    """Функция запроса логина и пароля у пользователя
    """
    while True:
        login_input = input('Введите логин: ')
        if login_input == 'q':
            return False
            break
        pass_input = input('Введите пароль: ')
        if pass_input == 'q':
            return False
            break
        user_login = check_in(login_input, pass_input)
        if user_login:    # сверка введенного логина со списком логинов прошла успешно
            return user_login


def ask_difficult():
    """Функция запроса сложности прохождения теста у пользователя
    """
    while True:         # проверяем корректность выбора трудости задачи
      dif_input = input('Введите уровень сложности от 1 до 3: ')
      difficult, flag = check_difficult(dif_input)
      if flag:
        break
      else:
        print('Введите корректное значение...\n')
    return difficult


def check_difficult(user_input):
    """Функция проверки корректности введеной пользователем сложности теста
        user_input - пользовательский ввод
    """
    try:
      difficult = int(user_input)
      if 1 <= difficult <= 3:    # если введенная сложность от 1 до 3х
        return difficult, True
      else:
        return '', False
    except ValueError:
      return '', False


def check_answer(user_input):
    """Функция проверки корректности введеного пользователем ответа
        user_input - пользовательский ввод
    """
    while True:
      try:
        if user_input == 'q':
          return '', True
          break
        else:
          user_result = int(user_input)
          return user_result, False
          break
      except ValueError:
        print('Неверный ввод...')
        user_input = input('Введите, ответ >>')


def test(difficult, begin_test_time, answers=0, errors_num=0):
    """Функция прохождения теста пользователем
        difficult - сложность теста
        begin_test_time - время начала теста
        Возвращает:
        answers - количество ответов пользователя
        errors_num - количество неправильных ответов пользователя
        rights_num - количество правильных ответов
        end_test_time - общее время выполнения теста
    """
    while True:
        right_result = new_task(difficult) # задаем новую задачку
        user_input = input('Введите, ответ >> ')
        user_result, exit = check_answer(user_input)   # просим ввести ответ
        if exit:
          end_test_time = end_test(begin_test_time)
          break
        if user_result == right_result: # если ответ правильный
          answers += 1
          print("Правильно!\n")
        else:                           # если ответ неверный
          errors_num += 1
          answers += 1
          print("Не правильно!\nПравильный ответ: {}\n".format(str(right_result)))
    rights_num = answers - errors_num
    return answers, errors_num, rights_num, end_test_time


def log_game(begin_test_time, end_test_time, difficult, answers, errors_num, rights_num, grade, login):
    """Функция записи лога теста для каждого пользователя
        begin_test_time - время начала теста
        end_test_time - общее время выполнения теста
        difficult - сложность теста
        answers - количество ответов пользователя
        errors_num - количество неправильных ответов пользователя
        rights_num - количество правильных ответов
        grade - оценка, полученная пользователем за теста
        login - логин пользователя, проходившего тест
    """
    name_file = login + '.txt'
    with open(name_file, 'a') as output_file:
        output_file.write('Начало игры: {}, Общее время игры: {} секунд(ы), сложность: {}, всего ответов: {}, правильных ответов: {}, неправильных ответов: {}, оценка: {}\n'.format(begin_test_time.strftime("%Y.%m.%d %H:%M:%S"), end_test_time.seconds, difficult, answers, rights_num, errors_num, grade))


def calculate_all(answers, errors_num):
    """Функция подсчета ответов пользователя и вывод этой информации на экран
        answers - количество ответов пользователя
        errors_num - количество неправильных ответов пользователя
    """
    if answers == 0:                    # если нажат сразу выход
      print('Bы не ответили ни на один вопрос!')
      grade = 2
    if answers > 0:                     # подсчитываем результат и ставим оценку
        grade = set_grade(answers, errors_num)
        print("\nВсего ответов: {}\nПравильных ответов: {}\
               \nНеправильных ответов: {}\nОценка: {}".format(
               answers, answers-errors_num, errors_num, grade))
    return grade

def users_logins():
    """Функция чтения списка логинов пользователей из файла
    """
    with open('logins.txt') as f:
        logins = f.read().split('\n')
    return logins


def users_passwords():
    """Функция чтения списка паролей пользователей из файла
    """
    with open('passwords.txt') as f:
        passwords = f.read().split('\n')
    return passwords


def list_of_users(logins, passwords):
    """Функция создания словаря из логинов и паролей пользователей
    """
    return dict(zip(logins, passwords))


def check_in(login, password):
    """Функция проверки корректности ввода логина и пароля пользователя
        Если пользователь не найден, предлагает создать пользователя с таким логином и паролем
        login - логин пользователя
        password - пароль пользователя
    """
    search = False
    logins = users_logins()
    passwords = users_passwords()
    users_data = list_of_users(logins, passwords)
    for search_login in logins:
        if search_login == login:
            search = True
            break
    if search == False:
        print('Пользователь с таким логином не найден!')
        reg = input('Хотите зарегистрировать пользователя с таким логином? y - да, n - нет ')
        if reg == 'n':
            print("Регистрация отменена....")
        elif reg == 'y':
            login = registration()
        else:
            print('Пользователь не зарегистрирован!')
    else:
        if password == users_data.get(login):
            return login
        else:
          print('Неверный пароль!')


def registration():
    """Функция регистрации нового пользователя
    """
    new_login_input = input('Введите логин нового пользователя: ')
    logins = users_logins()
    if re.match("^[A-Za-z0-9_-]*$", new_login_input):
        if new_login_input in logins:
            print('Пользователь с таким логином уже зарегестрирован!')
        else:
            with open('logins.txt', 'a') as output_file:
                output_file.write('\n' + new_login_input)
            while True:
                new_pass_input = input('Введите пароль нового пользователя: ')
                if re.match("^[A-Za-z0-9_-]*$", new_pass_input):
                    with open('passwords.txt', 'a') as output_file:
                        output_file.write('\n' + new_pass_input)
                        print('Пользователь успешно зарегестрирован!')
                    break
                else:
                    print('Введены недопустимые символы. Повторите ввод пароля.')
            return new_login_input
    else:
        print('Введены недопустимые символы. Повторите ввод логина.')
        registration()
