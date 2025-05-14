# Лабораторная работа 2: Потоки, процессы и асинхронность

## Цель

Целью данной лабораторной работы является понимание различий между потоками и процессами, а также понимание асинхронности в Python.

## Реализация

### Подход с использованием потоков

Подход с использованием потоков использует модуль Python `threading` для создания нескольких потоков для парсинга веб-страниц.

```python
import threading
import requests
from bs4 import BeautifulSoup
import time
from database import save_title_to_db

def parse_and_save(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "Заголовок не найден"
        save_title_to_db(url, title)
        print(f"Поток: {threading.current_thread().name}, URL: {url}, Заголовок: {title}")
    except Exception as e:
        print(f"Ошибка при парсинге {url}: {e}")

def main():
    urls = [
        "https://www.python.org",
        "https://www.github.com",
        "https://www.stackoverflow.com",
        "https://www.wikipedia.org",
        "https://www.reddit.com"
    ]
    
    threads = []
    start_time = time.time()
    
    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"Подход с использованием потоков занял {end_time - start_time:.2f} секунд")

if __name__ == "__main__":
    main()
```

### Подход с использованием многопроцессорности

Подход с использованием многопроцессорности использует модуль Python `multiprocessing` для создания нескольких процессов для парсинга веб-страниц.

```python
import multiprocessing
import requests
from bs4 import BeautifulSoup
import time
from database import save_title_to_db

def parse_and_save(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "Заголовок не найден"
        save_title_to_db(url, title)
        print(f"Процесс: {multiprocessing.current_process().name}, URL: {url}, Заголовок: {title}")
    except Exception as e:
        print(f"Ошибка при парсинге {url}: {e}")

def main():
    urls = [
        "https://www.python.org",
        "https://www.github.com",
        "https://www.stackoverflow.com",
        "https://www.wikipedia.org",
        "https://www.reddit.com"
    ]
    
    processes = []
    start_time = time.time()
    
    for url in urls:
        process = multiprocessing.Process(target=parse_and_save, args=(url,))
        processes.append(process)
        process.start()
    
    for process in processes:
        process.join()
    
    end_time = time.time()
    print(f"Подход с использованием многопроцессорности занял {end_time - start_time:.2f} секунд")

if __name__ == "__main__":
    main()
```

### Асинхронный подход

Асинхронный подход использует модули Python `asyncio` и `aiohttp` для создания асинхронных задач для парсинга веб-страниц.

```python
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import time
from database import save_title_to_db

async def parse_and_save(url, session):
    try:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            title = soup.title.string if soup.title else "Заголовок не найден"
            save_title_to_db(url, title)
            print(f"Задача: {asyncio.current_task().get_name()}, URL: {url}, Заголовок: {title}")
    except Exception as e:
        print(f"Ошибка при парсинге {url}: {e}")

async def main():
    urls = [
        "https://www.python.org",
        "https://www.github.com",
        "https://www.stackoverflow.com",
        "https://www.wikipedia.org",
        "https://www.reddit.com"
    ]
    
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(parse_and_save(url, session))
            tasks.append(task)
        
        await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"Асинхронный подход занял {end_time - start_time:.2f} секунд")

if __name__ == "__main__":
    asyncio.run(main())
```

## Сравнение производительности

| Подход | Время (секунды) |
|----------|----------------|
| Потоки | 1.25 |
| Многопроцессорность | 1.78 |
| Асинхронность | 0.89 |

## Анализ

### Потоки

Подход с использованием потоков подходит для задач, связанных с вводом-выводом, таких как веб-скрапинг, поскольку потоки могут эффективно ожидать ответов сети, не блокируя CPU. Однако из-за глобальной блокировки интерпретатора Python (GIL) потоки не могут выполнять код Python параллельно, что ограничивает их производительность для задач, связанных с CPU.

### Многопроцессорность

Подход с использованием многопроцессорности создает отдельные процессы, каждый со своим интерпретатором Python и пространством памяти. Это позволяет действительно параллельно выполнять код Python, что полезно для задач, связанных с CPU. Однако он имеет более высокие накладные расходы из-за создания процессов и межпроцессного взаимодействия, что может сделать его медленнее для задач, связанных с вводом-выводом.

### Асинхронность

Асинхронный подход использует один поток, но позволяет нескольким задачам выполняться одновременно, уступая управление при ожидании операций ввода-вывода. Это очень эффективно для задач, связанных с вводом-выводом, таких как веб-скрапинг, поскольку минимизирует время простоя без накладных расходов на создание нескольких потоков или процессов.

## Заключение

Для веб-скрапинга и других задач, связанных с вводом-выводом, асинхронный подход обеспечивает наилучшую производительность благодаря низким накладным расходам и эффективной обработке одновременных операций ввода-вывода. Подход с использованием потоков является хорошей альтернативой, если код не может быть легко адаптирован для использования async/await. Подход с использованием многопроцессорности больше подходит для задач, связанных с CPU, где требуется параллельное выполнение.
