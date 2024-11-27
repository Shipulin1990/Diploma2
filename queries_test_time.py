# queries_test_time.py

import subprocess
import time

def run_script(command):
    start_time = time.time()
    process = subprocess.Popen(command, shell=True)
    process.wait()
    end_time = time.time()
    return end_time - start_time

if __name__ == '__main__':
    print("Запуск тестов для Django ORM...")
    django_time = run_script('python django_orm/queries.py')
    print(f"Общее время выполнения для Django ORM: {django_time} секунд.\n")

    print("Запуск тестов для SQLAlchemy ORM...")
    sqlalchemy_time = run_script('python sqlalchemy_orm/queries.py')
    print(f"Общее время выполнения для SQLAlchemy ORM: {sqlalchemy_time} секунд.\n")

    print("Запуск тестов для Tortoise ORM...")
    tortoise_time = run_script('python tortoise_orm/queries.py')
    print(f"Общее время выполнения для Tortoise ORM: {tortoise_time} секунд.\n")

    print("Результаты тестирования:")
    print(f"Django ORM: {django_time} секунд")
    print(f"SQLAlchemy ORM: {sqlalchemy_time} секунд")
    print(f"Tortoise ORM: {tortoise_time} секунд")
