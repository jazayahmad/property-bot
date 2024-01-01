from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import http
import json

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

import xmltodict
from .rasa_functions import process_message, send_values
from config import whatsapp


origins = ['*']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    try:
        return {"message": "Welcome to PropertyBot"}
    except Exception as e:
        return {'Error': str(e)}

client = Client(whatsapp.account_sid, whatsapp.auth_token)

@app.post('/twilio')
async def webhook_wa(request: Request):
    print("*--------------------- WhatsApp (Twilio) Message -------------------------------*")
    text_ = await request.form()
    sid = text_.getlist('From')[0].split(':')[1]
    text_ = text_['Body']
    response = process_message(text_, sid)
    sv = send_values(text_, response)
    resp = MessagingResponse()
    res = resp.message(sv)
    dict_parsed = xmltodict.parse(str(res))
    dict_parsed = (dict_parsed['Message'])
    message = client.messages.create(
        body=dict_parsed,
        from_='whatsapp:+14155238886',
        to='whatsapp:'+ sid,
    )
    print(message)
    return JSONResponse({'Response': "Successful"})