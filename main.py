from fastapi import FastAPI, WebSocket
from typing import Dict, Any
import asyncio

app = FastAPI(title="NewPay")

websocket_data: Dict[str, Any] = {}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_json()
        websocket_data = data

@app.post("/api/s1/operation/create/setresponse")
async def set_response(data: Dict[str, Any]):
    global websocket_data

    if not websocket_data:
        websocket_data = {}

    websocket_data.update(data)
    return {}

@app.post("/api/s1/operation/create")
async def create_operation():
    global websocket_data

    if not websocket_data:
        return {"message": "setresponse не вызывался"}

    if "http_error" in websocket_data:
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

        if http_error in error_messages:
            return {"error": error_messages[http_error]}

    if "timeout" in websocket_data:
        timeout = websocket_data["timeout"]
        await asyncio.sleep(timeout)

    return websocket_data