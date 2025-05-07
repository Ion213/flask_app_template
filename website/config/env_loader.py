import os
from dotenv import load_dotenv
load_dotenv()


GMAIL = os.getenv("MAIL_USERNAME")
PASSWORD = os.getenv("MAIL_PASSWORD")
SECRET_KEY = os.getenv("SECRET_KEY")
database_url = os.getenv("DATABASE_URL")