import os
from datetime import datetime
from typing import Any, Dict, List, Optional
import logging

import requests

# Настройки логгера
logging.basicConfig(level=logging.INFO, filename="MyApp.log", filemode="w")
logger = logging.getLogger("MyApp")


class User:
    """
    Представление пользователя

    - id - Идентификатор пользователя
    - name - Имя пользователя
    - username - Юзернейм\логин пользователя
    - email - Адрес эл. почты
    - company - Название компании
    """

    def __init__(self, id: int,
                 name: str,
                 username: str,
                 email: str,
                 company: str):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.company = company


class Task:
    """
    Представление задач

    - id - Идентификатор задачи
    - title - Название задачи
    - completed - Завершенная\Незавершенная задача
    """

    def __init__(self, id: int,
                 title: str,
                 completed: bool):
        self.id = id
        self.title = title
        self.completed = completed


class ReportManager:
    """
    Представление менеджера отчетов

    - users_url - Ссылка на API содержащая всех пользователей и их данные
    - todos_url - Ссылка на API содержащая задачи конкретного пользователя
    """

    def __init__(self, users_url: str, todos_url: str):
        self.users_url = users_url
        self.todos_url = todos_url

    @staticmethod
    def get_data(url: str) -> Optional[List[Dict[str, Any]]]:
        """
        Получаем данные по указанной ссылке в формате Json.

        Параметры:
        - url: str - Url для запроса данных.

        Возвращает:
        List[Dict[str, Any]] или None: Данные в формате Json или None в случае ошибки.
        """
        try:
            response = requests.get(url, timeout=10, headers={"User-Agent": "MyApp/1.0"})
            response.raise_for_status()

            try:
                return response.json()
            except ValueError:
                logger.error("Ответ не в формате Json")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при получении данных: {e}")
            return None

    @staticmethod
    def create_report(user_data: User, tasks_data: List[Task]) -> str:
        """
        Функция получает на вход объект класса User, а так же
        список задач данного пользователя.

        В данной функции возвращается отчет в виде строки,
        который содержит: шапку, актуальные и завершенные задачи.
        """
        company = user_data.company
        email = user_data.email
        name = user_data.name
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")

        report = f"# Отчёт для {company}.\n"
        report += f"{name} <{email}> {current_time}\n"
        report += f"Всего задач: {len(tasks_data)}\n\n"

        unfinished_tasks = [task for task in tasks_data if not task.completed]
        report += f"## Актуальные задачи ({len(unfinished_tasks)}):\n"

        for task in unfinished_tasks:
            title = task.title[:46] + "…" if len(task.title) > 46 else task.title
            report += f"- {title}\n"

        report += f"\n## Завершённые задачи ({len(tasks_data) - len(unfinished_tasks)}):\n"
        for task in tasks_data:
            if task.completed:
                title = task.title[:46] + "…" if len(task.title) > 46 else task.title
                report += f"- {title}\n"

        return report

    @staticmethod
    def save_report(username: str, report: str):
        """
        Функция получает на вход логин\юзернейм человека
        и готовый отчет.

        В данной функции происходит проверка на существование предыдущих отчетов
        и их переименования, с последующим добавлением нового отчета.
        """
        directory = "tasks"

        # Создание директории отчетов, если ее не существует
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = f"{username}.txt"

        # Определения пути для нового отчета
        path_file = os.path.join(directory, filename)

        # Переименование файла отчета, если он уже существует
        if os.path.exists(path_file):
            creation_time = os.path.getctime(path_file)
            old_filename = (f"old_{username}_"
                            f"{datetime.fromtimestamp(creation_time).strftime('%Y-%m-%dT%H:%M')}.txt")
            os.rename(path_file, os.path.join(directory, old_filename))

        with open(path_file, "w", encoding="utf-8") as file:
            file.write(report)


def main():
    report_manager = ReportManager("https://json.medrocket.ru/users", "https://json.medrocket.ru/todos")

    users_data: List[Dict[str, Any]] = report_manager.get_data(report_manager.users_url)
    if not users_data:
        return

    for user_data in users_data:
        user = User(user_data["id"], user_data["name"], user_data["username"], user_data["email"],
                    user_data["company"]["name"])
        task_url = f"{report_manager.todos_url}?userId={user.id}"
        tasks_data = report_manager.get_data(task_url)

        if tasks_data:
            tasks: list[Task] = [Task(task_data["id"], task_data["title"], task_data["completed"])
                                 for task_data in tasks_data]
            report = report_manager.create_report(user, tasks)
            report_manager.save_report(user.username, report)
            logger.info(f"Отчёт для {user.name} создан и сохранен")


if __name__ == "__main__":
    main()
