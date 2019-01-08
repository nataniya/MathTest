from defs import log_game, ask_login, ask_difficult, begin_test, test, calculate_all


if __name__ == "__main__":

    print("Для выхода введите q.\n")

    user_login = ask_login()
    if user_login:
        difficult = ask_difficult()
        begin_game = begin_test()
        answers, errors_num, rights_num, end_test_time = test(difficult, begin_game)
        grade = calculate_all(answers, errors_num)
        log_game(begin_game, end_test_time, difficult, answers, errors_num, rights_num, grade, user_login)
    else:
        print('Выход из теста')
