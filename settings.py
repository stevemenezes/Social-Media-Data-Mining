import os


LOG_LEVEL = "DEBUG"
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
BASE_OUTPUT_PATH = ROOT_PATH+"/../../../"
LOG_PATH = os.path.join(BASE_OUTPUT_PATH,'logs')

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

BACKEND_URL = "https://cloud.iaastha.com"
# BACKEND_URL = "http://localhost:8000"


VENV_PATH = os.path.join(ROOT_PATH+"/../../../../../",'twitterextraction')
ACTIVATE_VENV = os.path.join(VENV_PATH,os.path.join('bin','activate_this.py'))
print("Using application virtual ENV Path : {0}".format(VENV_PATH))
