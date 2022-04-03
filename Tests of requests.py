import datetime
from CustomRequests import registration, delete_user, get_token,\
                           get_student_list, get_all_lessons,\
                           get_relevant_lessons, convert_lessons_to_dict,\
                           create_lesson, update_lesson, delete_lesson,\
                           get_my_lessons

# API tests:
# 0) узнать количество юзеров (админ) -> int
# 0) узнать количество всех уроков (админ) -> int
# 1) создание первого юзера (username=TEST1asfwnfwlhdwnjwejdl) -> True
# 2) создание второго юзера (username=TEST2asfwnfwlhdwnjwejdl) (админ) -> True
# 3) просмотр всех текущих уроков (юзер 1) -> list
# 4) просмотр своих уроков (юзер 1) -> empty list
# 5) создание урока (юзер 1) -> true
# 6) просмотр своих уроков (юзер 1) -> list
# 7) изменение урока (юзер 1) -> true
# 8) изменение чужого урока (юзер 2) -> false
# 9) создание второго урока (юзер 1) -> true
# 10) удаление своего урока (юзер 1) -> true
# 11) удаление чужого урока (юзер 2) -> false
# 12) удаление урока юзера 1 (админ) -> true
# 13) создание урока юзера 1 (админ) -> true
# 14) изменение урока юзера 1 (админ) -> true
# 15) удаление урока юзера 1 (админ) -> true
# 16) удаление юзера 1 (админ) -> true
# 17) проверить наличие текущих уроков (юзер 2) -> list
# 18) проверить наличие уроков (+ прошедших) -> list
# 19) удаление юзера 2 (админ) -> true
# 20) проверить работу сортировки всех уроков -> dict
# 0) проверить количество юзеров (админ) -> true (совпадение с началом)
# 0) проверить количество всех уроков (админ) -> true (совпадение с началом)


# domen = 'http://127.0.0.1:8000/'
domen = 'https://calendarapi-kpa.herokuapp.com/'
with open('credentials.txt', 'r') as file:
    admin_username = file.readline().split(':')[1][:-1]
    admin_password = file.readline().split(':')[1]
username_1, name_1, password_1, phone_1, relation_1 = (
    'TEST1vqeoirhiseneb', 'name 1', 'TEST1wejdl', '89001324567', 'Telegram'
)
username_2, name_2, password_2, phone_2, relation_2 = (
    'TEST2vqeoirhiseneb', 'name 2', 'TEST2wejdl', '89123456789', 'Both'
)
week = str(datetime.date.today() + datetime.timedelta(days=7))
month = str(datetime.date.today() + datetime.timedelta(days=11))
yesterday = str(datetime.date.today() - datetime.timedelta(days=1))


###############################################################################
#                                  API tests                                  #
###############################################################################

if True:
    # 0
    amount_users_1 = len(get_student_list(domen, admin_username,
                                          admin_password))
    # print('0)', amount_users_1)

    # 0
    amount_lessons_1 = len(get_all_lessons(domen, admin_username,
                                           admin_password))
    # print('0)', amount_lessons_1)

    # 1
    student_1 = registration(domen, username_1, name_1, password_1,
                             phone_1, relation_1)
    if type(student_1) is dict and len(student_1) == 6:
        print('1)', True)
    else:
        print('1)', False)

    # 2
    student_2 = registration(domen, username_2, name_2, password_2,
                             phone_2, relation_2)
    if type(student_2) is dict and len(student_2) == 6:
        print('2)', True)
    else:
        print('2)', False)

    # 3
    lst = get_relevant_lessons(domen, username_1, password_1)
    if type(lst) is list:
        print('3)', True)
    else:
        print('3)', False)

    # 4
    lst = get_my_lessons(domen, username_1, password_1)
    if type(lst) is list and len(lst) == 0:
        print('4)', True)
    else:
        print('4)', False)

    # 5
    time_1 = '15:00:00'
    data = {'theme': 'Consultation', 'salary': 700, 'time': time_1,
            'date': week}
    lesson_1 = create_lesson(domen, username_1, password_1, data, admin=False)
    time_1 = lesson_1['time']
    if type(lesson_1) is dict and len(lesson_1) == 6:
        print('5)', True)
    else:
        print('5)', False)

    # 6
    lst = get_my_lessons(domen, username_1, password_1)
    if type(lst) is list and len(lst) == 1:
        print('6)', True)
    else:
        print('6)', False)

    # 7
    time_2 = '16:00:00'
    data = {'id': lesson_1['id'], 'theme': 'Consultation',
            'salary': 700, 'time': time_2, 'date': week}
    lesson_1 = update_lesson(domen, username_1, password_1, data, admin=False)
    time_2 = lesson_1['time']
    if type(lesson_1) is dict and len(lesson_1) == 6 and time_1 != time_2:
        print('7)', True)
    else:
        print('7)', False)

    # 8
    data = {'id': lesson_1['id'], 'theme': 'Consultation',
            'salary': 700, 'time': '15:00:00', 'date': week}
    update_lesson_1 = update_lesson(domen, username_2, password_2, data,
                                    admin=False)
    if update_lesson_1.get('detail') == 'Not found.':
        print('8)', True)
    else:
        print('8)', False)

    # 9
    data = {'theme': 'Consultation', 'salary': 700, 'time': '17:00:00',
            'date': week}
    lesson_2 = create_lesson(domen, username_1, password_1, data, admin=False)
    if type(lesson_2) is dict and len(lesson_2) == 6:
        print('9)', True)
    else:
        print('9)', False)

    # 10
    if delete_lesson(domen, username_1, password_1, lesson_1, admin=False):
        print('10)', True)
    else:
        print('10)', False)

    # 11
    if not delete_lesson(domen, username_2, password_2, lesson_2, admin=False):
        print('11)', True)
    else:
        print('11)', False)

    # 12
    if delete_lesson(domen, admin_username, admin_password, lesson_2,
                     admin=True):
        print('12)', True)
    else:
        print('12)', False)

    # 13
    time_3 = '18:00:00'
    data = {'student': student_1['id'], 'theme': 'Consultation',
            'salary': 700, 'time': time_3, 'date': week}
    lesson_3 = create_lesson(domen, admin_username, admin_password, data,
                             admin=True)
    time_3 = lesson_3['time']
    if type(lesson_3) is dict and len(lesson_3) == 6:
        print('13)', True)
    else:
        print('13)', False)

    # 14
    time_4 = '19:00:00'
    data = {'id': lesson_3['id'], 'student': student_1['id'],
            'theme': 'Consultation', 'salary': 700, 'time': time_4,
            'date': week}
    lesson_3 = update_lesson(domen, admin_username, admin_password, data,
                             admin=True)
    time_4 = lesson_3['time']
    if type(lesson_3) is dict and len(lesson_3) == 6 and time_3 != time_4:
        print('14)', True)
    else:
        print('14)', False)

    # 15
    if delete_lesson(domen, admin_username, admin_password, lesson_3,
                     admin=True):
        print('15)', True)
    else:
        print('15)', False)

    # 16
    if delete_user(domen, admin_username, admin_password,
                   student_1['username']):
        print('16)', True)
    else:
        print('16)', False)

    # 17
    if type(get_relevant_lessons(domen, username_2, password_2)) is list:
        print('17)', True)
    else:
        print('17)', False)

    # 18
    all_lessons = get_all_lessons(domen, admin_username, admin_password)
    if type(all_lessons) is list:
        print('18)', True)
    else:
        print('18)', False)

    # 19
    if delete_user(domen, admin_username, admin_password,
                   student_2['username']):
        print('19)', True)
    else:
        print('19)', False)

    # 20
    if type(convert_lessons_to_dict(all_lessons)) is dict:
        print('20)', True)
    else:
        print('20)', False)

    # 0
    amount_users_2 = len(get_student_list(domen, admin_username,
                                          admin_password))
    if amount_users_2 == amount_users_1:
        print('0)', True)
    else:
        print('0)', False)

    # 0
    amount_lessons_2 = len(get_all_lessons(domen, admin_username,
                                           admin_password))
    if amount_lessons_2 == amount_lessons_1:
        print('0)', True)
    else:
        print('0)', False)


###############################################################################
#                              Validation  tests                              #
###############################################################################

# Validation tests:

if True:
    # 1
    amount_users_1 = len(get_student_list(domen, admin_username,
                         admin_password))
    # print('0)', amount_users_1)
    print('1)', True)

    # 2
    amount_lessons_1 = len(get_all_lessons(domen, admin_username,
                           admin_password))
    # print('0)', amount_lessons_1)
    print('2)', True)

    # 3
    student_1 = registration(domen, username_1, name_1, password_1,
                             phone_1, relation_1)
    if type(student_1) is dict and len(student_1) == 6:
        print('3)', True)
    else:
        print('3)', False)

    # 4
    time_1 = '15:00:00'
    data = {'theme': 'Consultation', 'salary': 700, 'time': time_1,
            'date': week}
    lesson_1 = create_lesson(domen, username_1, password_1, data, admin=False)
    if type(lesson_1) is dict and len(lesson_1) == 6:
        time_1 = lesson_1['time']
        print('4)', True)
    else:
        print('4)', False, lesson_1['non_field_errors'][0])

    # 5
    time_2 = '15:00:00'
    data = {'theme': 'Consultation', 'salary': 700, 'time': time_2,
            'date': week}
    lesson_2 = create_lesson(domen, username_1, password_1, data, admin=False)
    if lesson_2.get('non_field_errors'):
        print('5)', True, lesson_2['non_field_errors'][0])
    else:
        print('5)', False)

    # 6
    time_2 = '15:55:00'
    data = {'theme': 'Consultation', 'salary': 700, 'time': time_2,
            'date': week}
    lesson_2 = create_lesson(domen, username_1, password_1, data, admin=False)
    if lesson_2.get('non_field_errors'):
        print('6)', True, lesson_2['non_field_errors'][0])
    else:
        print('6)', False)

    # 7
    time_2 = '15:55:00'
    data = {'id': student_1['id'], 'theme': 'Consultation', 'salary': 700,
            'time': time_2, 'date': week}
    lesson_2 = create_lesson(domen, admin_username, admin_password, data,
                             admin=False)
    if lesson_2.get('non_field_errors'):
        print('7)', True, lesson_2['non_field_errors'][0])
    else:
        print('7)', False)

    # 8
    time_2 = '16:00:00'
    data = {'theme': 'Consultation', 'salary': 700, 'time': time_2,
            'date': week}
    lesson_2 = create_lesson(domen, username_1, password_1, data, admin=False)
    if type(lesson_2) is dict and len(lesson_2) == 6:
        time_2 = lesson_2['time']
        print('8)', True)
    else:
        print('8)', False, lesson_2['non_field_errors'][0])

    # 9
    time_3 = '16:00:00'
    data = {'theme': 'Consultation', 'salary': 700, 'time': time_3,
            'date': yesterday}
    lesson_3 = create_lesson(domen, username_1, password_1, data, admin=False)
    if lesson_3.get('non_field_errors'):
        print('9)', True, lesson_3['non_field_errors'][0])
    else:
        print('9)', False)

    # 10
    time_3 = '16:00:00'
    data = {'theme': 'Consultation', 'salary': 700, 'time': time_3,
            'date': month}
    lesson_3 = create_lesson(domen, username_1, password_1, data, admin=False)
    if lesson_3.get('non_field_errors'):
        print('10)', True, lesson_3['non_field_errors'][0])
    else:
        print('10)', False)

    # 11
    time_3 = '7:30:00'
    data = {'theme': 'Consultation', 'salary': 1000, 'time': time_3,
            'date': week}
    lesson_3 = create_lesson(domen, username_1, password_1, data, admin=False)
    if lesson_3.get('non_field_errors'):
        print('11)', True, lesson_3['non_field_errors'][0])
    else:
        print('11)', False)

    # 12
    time_3 = '23:30:00'
    data = {'theme': 'Consultation', 'salary': 1000, 'time': time_3,
            'date': week}
    lesson_3 = create_lesson(domen, username_1, password_1, data, admin=False)
    if lesson_3.get('non_field_errors'):
        print('12)', True, lesson_3['non_field_errors'][0])
    else:
        print('12)', False)

    # 13
    time_3 = '8:30:00'
    data = {'theme': 'Consultation', 'salary': 700, 'time': time_3,
            'date': week}
    lesson_3 = create_lesson(domen, username_1, password_1, data, admin=False)
    if lesson_3.get('non_field_errors'):
        print('13)', True, lesson_3['non_field_errors'][0])
    else:
        print('13)', False)

    # 14
    time_3 = '8:30:00'
    data = {'theme': 'Consultation', 'salary': 1000, 'time': time_3,
            'date': week}
    lesson_3 = create_lesson(domen, username_1, password_1, data, admin=False)
    if type(lesson_3) is dict and len(lesson_3) == 6:
        time_3 = lesson_3['time']
        print('14)', True)
    else:
        print('14)', False, lesson_3['non_field_errors'][0])

    # 15
    time_4 = '22:00:00'
    data = {'theme': 'Consultation', 'salary': 1000, 'time': time_4,
            'date': week}
    lesson_4 = create_lesson(domen, username_1, password_1, data, admin=False)
    if type(lesson_4) is dict and len(lesson_4) == 6:
        time_4 = lesson_4['time']
        print('15)', True)
    else:
        print('15)', False, lesson_4['non_field_errors'][0])

    # 16
    time_5 = '21:00:00'
    data = {'theme': 'Consultation', 'salary': 700, 'time': time_5,
            'date': week}
    lesson_5 = create_lesson(domen, username_1, password_1, data, admin=False)
    if lesson_5.get('non_field_errors'):
        print('16)', True, lesson_5['non_field_errors'][0])
    else:
        print('16)', False)

    # 17
    time_5 = datetime.datetime.now() + datetime.timedelta(hours=5)
    data = {'theme': 'Consultation', 'salary': 1000,
            'time': time_5.time().strftime("%H:%M:%S"),
            'date': str(time_5.date())}
    lesson_5 = create_lesson(domen, username_1, password_1, data, admin=False)
    if lesson_5.get('non_field_errors'):
        print('17)', True, lesson_5['non_field_errors'][0])
    else:
        print('17)', False)

    # 18
    time_5 = '16:00:00'
    data = {'theme': 'Consultation', 'salary': 699, 'time': time_5,
            'date': week}
    lesson_5 = create_lesson(domen, username_1, password_1, data, admin=False)
    if lesson_5.get('non_field_errors'):
        print('18)', True, lesson_5['non_field_errors'][0])
    else:
        print('18)', False)

    # 19
    if delete_lesson(domen, username_1, password_1, lesson_1, admin=False):
        print('19)', True)
    else:
        print('19)', False)

    if delete_lesson(domen, username_1, password_1, lesson_2, admin=False):
        print('19)', True)
    else:
        print('19)', False)

    if delete_lesson(domen, username_1, password_1, lesson_3, admin=False):
        print('19)', True)
    else:
        print('19)', False)

    if delete_lesson(domen, username_1, password_1, lesson_4, admin=False):
        print('19)', True)
    else:
        print('19)', False)

    # 20
    if delete_user(domen, admin_username, admin_password,
                   student_1['username']):
        print('20)', True)
    else:
        print('20)', False)

    # 21
    amount_users_2 = len(get_student_list(domen, admin_username,
                                          admin_password))
    if amount_users_2 == amount_users_1:
        print('21)', True)
    else:
        print('21)', False)

    # 22
    amount_lessons_2 = len(get_all_lessons(domen, admin_username,
                                           admin_password))
    if amount_lessons_2 == amount_lessons_1:
        print('22)', True)
    else:
        print('22)', False)
