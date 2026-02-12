# Задание 1: тип данных (email)
def check_email(email: str) -> bool:
    """Проверяет, содержит ли email '@', '.' и не содержит пробелов."""
    if ('@' in email) and ('.' in email) and (' ' not in email):
        return True
    return False


# Задание 2: циклы (расчёт времени)
def solve(todo_list: list, workday: float = 8) -> float:
    """
    Принимает список задач [ (название, время), ... ] и рабочий день.
    Возвращает оставшееся время (workday - сумма времени задач).
    """
    worktime = 0.0
    for task in todo_list:
        worktime += task[1]
    return round(workday - worktime, 1)  # округление до 1 знака, как в исходном коде


# Задание 3: словари (анализ курсов)
def analyze_courses(courses, mentors, durations):
    """
    Формирует список курсов (словари с ключами title, mentors, duration).
    Определяет минимальную и максимальную длительность,
    находит все курсы с такой длительностью.
    Возвращает кортеж: (min_duration, max_duration, courses_min, courses_max)
    """
    # Создаём список словарей
    courses_list = []
    for title, mentors_list, duration in zip(courses, mentors, durations):
        course_dict = {
            'title': title,
            'mentors': mentors_list,
            'duration': duration
        }
        courses_list.append(course_dict)

    min_duration = min(durations)
    max_duration = max(durations)

    # Индексы курсов с минимальной/максимальной длительностью
    min_indices = [i for i, d in enumerate(durations) if d == min_duration]
    max_indices = [i for i, d in enumerate(durations) if d == max_duration]

    # Названия курсов
    courses_min = [courses_list[i]['title'] for i in min_indices]
    courses_max = [courses_list[i]['title'] for i in max_indices]

    return min_duration, max_duration, courses_min, courses_max