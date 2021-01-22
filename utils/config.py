import pymysql
# config.py
db = {
    'user'     : '####',		# 1)
    'password' : '####',		# 2)
    'host'     : '####',	# 3)
    'port'     : 3306,			# 4)
    'database' : 'KorConversationApp'		# 5)
}
DB_URL = f"mysql+pymysql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
