from conf import PROJECT_NAME
from utils.fileHelper import readFile

data = readFile(PROJECT_NAME, ['conf.json'])

REDIS_HOST = data['redis']['REDIS_HOST']
REDIS_PORT = data['redis']['REDIS_PORT']
REDIS_PASSWORD = data['redis']['REDIS_PASSWORD']