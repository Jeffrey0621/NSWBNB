import os
from dotenv import load_dotenv

load_dotenv()

class TestConfig(object):
    # DB config
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
