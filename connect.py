from configparser import ConfigParser
from mongoengine import connect
from redis import StrictRedis
from redis_lru import RedisLRU


config = ConfigParser()
config.read('../config.ini')
user_name = config.get('DB', 'user')
password = config.get('DB', 'pass')
db_name = config.get('DB', 'db_name')
db_domain = config.get('DB', 'db_domain')

connect(host=f"""mongodb+srv://{user_name}:{password}@{db_domain}/{db_name}?retryWrites=true&w=majority""", ssl=True)

redis_connect = StrictRedis(host='localhost', port=6379, password=None)
cache = RedisLRU(redis_connect)
