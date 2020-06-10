import pymysql
# config.py
db = {
    'user'     : 'ds2017',		# 1)
    'password' : 'cream2020',		# 2)
    'host'     : '3.20.87.90',	# 3)
    'port'     : 3306,			# 4)
    'database' : 'KorConversationApp'		# 5)
}
DB_URL = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
