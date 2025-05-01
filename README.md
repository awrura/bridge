[![Review](https://github.com/awrura/bridge/actions/workflows/review.yml/badge.svg)](https://github.com/awrura/bridge/actions/workflows/review.yml)
[![Run Tests](https://github.com/awrura/bridge/actions/workflows/unitest.yml/badge.svg)](https://github.com/awrura/bridge/actions/workflows/unitest.yml)

![Static Badge](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=yellow)
![Static Badge](https://img.shields.io/badge/docker-25.0.4-blue?logo=docker)
![Static Badge](https://img.shields.io/badge/redis-7.2.4-blue?logo=redis&logoColor=red)
![Static Badge](https://img.shields.io/badge/FastAPI-0.109.0-blue?logo=fastapi&logoColor=%23009688)
![Static Badge](https://img.shields.io/badge/pytest-8.0.1-blue?logo=pytest&logoColor=red)
![Static Badge](https://img.shields.io/badge/poetry-1.8.5-blue?logo=poetry)

## Bridge

`HTTP` плагин для отправки команд на матрицу. 

Принимает входищие запросы по `HTTP` обрабатывает их, сериализует данные и отправляет в сервис [sender](https://github.com/awrura/sender) для дальнейшей отправки их на матрицу. 
Так же данный сервис поддерживает общение по протоколу `WS`

## Сборка

Для сборки используется [Dockerfile](https://github.com/awrura/bridge/blob/main/docker/Dockerfile), поэтому сборка возможна через `Docker`. **Важно**, перед запуском `docker` контейнера необходимо создать и заполнить `.env` файл. Пример файла можно посмотреть в **`.env.example`**

## Жизненный цикл

![image](https://github.com/user-attachments/assets/c2e7e81b-dbaa-4ae7-bb73-cebe93d53545)
