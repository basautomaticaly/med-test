## Тестовое задание для Мед-Рокет

#### Stack:
- [Python](https://www.python.org/downloads/)
- [Requests](https://pypi.org/project/requests/)

## Локальный запуск

Все действия следует выполнять из исходного каталога проекта и только после установки всех требований.

1. Сначала создайте и активируйте новую виртуальную среду:
   ```bash
   python3.9 -m venv ../venv
   source ../venv/bin/activate
   ```
   
2. Установите необходимые зависимости:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   
3. Запустите main.py и дождитесь его закрытия:
В каталоге, где находится скрипт, появится папка с названием "Tasks",
в которой будут сформированные отчеты, если запускать все последующие разы, то старые отчеты будут переименованы в формате:
   ```bash
   имя файла: old_Username_2020-09-23T15:25.txt
   ```
После переименования скрипт создаст новый отчет для этого пользователя.

4. В случае ошибок, обратитесь к файлу MyApp.log, который будет создан автоматически.
В нем будут находится сообщения о неисправностях.
