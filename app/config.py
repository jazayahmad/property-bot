from pydantic import BaseSettings
import os

path = os.path.join(os.curdir,".env")

# WhatsApp Config Class
class WhatsApp(BaseSettings):
    account_sid: str
    auth_token: str

    class Config:
        env_file = path

whatsapp = WhatsApp()