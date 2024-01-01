import requests
import json as js


#Sending Messages to Rasa
def send_rasa_messages(text_, sid):
    try:
        print("********************Rasa Sender Message Called")
        data = js.dumps({"sender": sid, "message": text_})
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post('http://127.0.0.1:5005/webhooks/rest/webhook', data=data, headers=headers)
        print("Res: ",res.text)
        dict_res = js.loads(res.text) 
        dict_res = preprocess_message(dict_res)
        return str(dict_res)
    except Exception as e:
        return e


#Presprocessing the messages
def preprocess_message(msg):
    str_msg = ''
    for i in msg:
        try:
            str_msg += ' \n'+(i['text'])
        except:
            str_msg += ' \n'+(i['image'])
    return str_msg

#Getting message from user and passing it to send_rasa_messages method
def process_message(text_, sid):
    formatted_message = text_.lower()
    response = send_rasa_messages(formatted_message, sid)
    return response

#Function for redirecting to middleware
def send_values(user, bot):
    user = str(user).strip()
    bot = str(bot).strip()
    return bot