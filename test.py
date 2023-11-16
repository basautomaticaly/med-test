import unittest

from main import ReportManager, User, Task


class TestMyApp(unittest.TestCase):

    def test_get_data_valid_url(self):
        url = "https://json.medrocket.ru/users"
        data = ReportManager.get_data(url)
        self.assertIsInstance(data, list)

    def test_get_data_invalid_url(self):
        url = "https://json.example.ru/users"
        data = ReportManager.get_data(url)
        self.assertIsNone(data)

    def test_create_report(self):
        user = User(22,
                    "Sergey Popov",
                    "wxksy",
                    "azooro.manager@example.com",
                    "Мед Рокет")

        tasks = [Task(22, "Выполненное задание N1", True),
                 Task(22, "Не выполненное задание N2", False)]

        report = ReportManager.create_report(user, tasks)

        self.assertIn(user.name, report)
        self.assertIn("Актуальные задачи (1)", report)
        self.assertIn("Завершённые задачи (1)", report)
        self.assertIn("Всего задач: 2", report)

    def test_create_report_no_task(self):
        user = User(22,
                    "Sergey Popov",
                    "wxksy",
                    "azooro.manager@example.com",
                    "Мед Рокет")

        tasks = []
        report = ReportManager.create_report(user, tasks)

        self.assertIn(user.name, report)
        self.assertIn("Актуальные задачи (0)", report)
        self.assertIn("Завершённые задачи (0)", report)
        self.assertIn("Всего задач: 0", report)


if __name__ == '__main__':
    unittest.main()
