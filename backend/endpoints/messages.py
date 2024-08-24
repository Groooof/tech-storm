import json
import random
import sys
from math import ceil
from time import sleep

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from ai.db_filler.utilities import getconfig
from ai.llm.llm_answer.search import ModelOllama
from ai.llm.query_transformer.rephrase import make_rephares, rephrase_query
from logic.messages import create_message
from schemas.messages import CreateMessageSchema
from shared.dependencies import _get_session

router = APIRouter(tags=['messages'])


@router.websocket("/ws")
async def ws_message(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            # {user_id: 0, text: ''}
            raw_data = await websocket.receive_text()
            json_data = json.loads(raw_data)
            data = CreateMessageSchema(user_id=json_data['user_id'], type_='question', text=json_data['text'])

            async with _get_session() as session:
                message_id = await create_message(session, data)

            response = {'type': 'message_id', 'data': message_id}
            await websocket.send_text(json.dumps(response, ensure_ascii=False))

            model = ModelOllama(getconfig)
            reph_funcs = [make_rephares]
            additional_question = rephrase_query(data.text, model, random.choice(reph_funcs))

            stream, sources = model.make_search(data.text, additional_query=additional_question)
            answer = ''

            for chunk in stream:
                if answer_part := chunk["response"]:
                    answer += answer_part
                    response = {'type': 'answer', 'data': {'id': -1, 'text': answer_part}}
                    await websocket.send_text(json.dumps(response, ensure_ascii=False))

            print(sources)
            sources = '\n'.join(sources.split(','))
            print(sources)
            response = {'type': 'answer', 'data': {'id': -1, 'text': sources}}
            await websocket.send_text(json.dumps(response, ensure_ascii=False))

            data = CreateMessageSchema(user_id=json_data['user_id'], type_='answer', text=answer)
            async with _get_session() as session:
                message_id = await create_message(session, data)

            response = {'type': 'message_id', 'data': message_id}
            await websocket.send_text(json.dumps(response, ensure_ascii=False))

    except WebSocketDisconnect:
        return
