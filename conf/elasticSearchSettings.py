# 配置es地址信息
from conf import PROJECT_NAME
from utils.fileHelper import readFile

data = readFile(PROJECT_NAME, ['conf.json'])


ELASTICSEARCH_SERVER = data['es']['ELASTICSEARCH_SERVER']
# 数据库
ELASTICSEARCH_INDEX = data['es']['ELASTICSEARCH_INDEX']