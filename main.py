from fastapi import FastAPI, WebSocket
from typing import Dict, Any
import asyncio

app = FastAPI(title="NewPay")  # Создание экземпляра FastAPI с заголовком "NewPay"

websocket_data: Dict[str, Any] = {}  # Словарь для хранения данных из WebSocket


@app.websocket("/ws")  # WebSocket конечная точка по адресу "/ws"
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Принятие соединения WebSocket

    while True:
        data = await websocket.receive_json()  # Ожидание получения JSON-данных из WebSocket
        websocket_data = data  # Обновление словаря websocket_data полученными данными


@app.post("/api/s1/operation/create/setresponse")  # POST-маршрут по адресу "/api/s1/operation/create/setresponse"
async def set_response(data: Dict[str, Any]):
    global websocket_data

    if not websocket_data:  # Если словарь websocket_data пустой, инициализируем его
        websocket_data = {}

    websocket_data.update(data)  # Обновление словаря websocket_data полученными данными
    return {}  # Возвращаем пустой словарь в качестве ответа


@app.post("/api/s1/operation/create")  # POST-маршрут по адресу "/api/s1/operation/create"
async def create_operation():
    global websocket_data

    if not websocket_data:  # Если словарь websocket_data пустой, возвращаем сообщение об ошибке
        return {"message": "setresponse не вызывался"}

    if "http_error" in websocket_data:  # Если в словаре websocket_data есть ключ "http_error"
        http_error = websocket_data["http_error"]
        error_messages = {
            400: "Ошибка 400: Неправильный запрос",
            401: "Ошибка 401: Несанкционированный",
            403: "Ошибка 403: Запрещено",
            404: "Ошибка 404: Не найдено",
            405: "Ошибка 405: Метод не разрешен",
            406: "Ошибка 406: Недопустимо",
            408: "Ошибка 408: Время ожидания запроса",
            409: "Ошибка 409: Конфликт",
            412: "Ошибка 412: Сбой предварительных условий",
            429: "Ошибка 429: Слишком много запросов",
            500: "Ошибка 500: Внутренняя ошибка сервера",
            501: "Ошибка 501: Не реализовано",
            502: "Ошибка 502: Недопустимый шлюз",
            503: "Ошибка 503: Служба недоступна",
            504: "Ошибка 504: Время ожидания шлюза"
        }

        if http_error in error_messages:  # Если код ошибки присутствует в словаре error_messages
            return {"error": error_messages[http_error]}  # Возвращаем сообщение об ошибке

    if "timeout" in websocket_data:  # Если в словаре websocket_data есть ключ "timeout"
        timeout = websocket_data["timeout"]
        await asyncio.sleep(timeout)  # Ожидание указанной продолжительности

    return websocket_data  # Возвращаем словарь websocket_data в качестве ответа
