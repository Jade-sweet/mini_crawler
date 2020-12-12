from conf import PROJECT_NAME
from utils.fileHelper import readFile

data = readFile(PROJECT_NAME, ['conf.json'])

FEED_EXPORT_ENCODING = data['mysql']['FEED_EXPORT_ENCODING']
MYSQL_HOST = data['mysql']['MYSQL_HOST']
MYSQL_PORT = data['mysql']['MYSQL_PORT']
MYSQL_USERNAME = data['mysql']['MYSQL_USERNAME']
MYSQL_PASSWORD = data['mysql']['MYSQL_PASSWORD']
MYSQL_DATABASE = data['mysql']['MYSQL_DATABASE']