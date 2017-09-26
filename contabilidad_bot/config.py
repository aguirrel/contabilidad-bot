import os

telegram = {
	'token': os.environ.get('TELEGRAM_TOKEN', '')
}

db = {
	'prefix': os.environ.get('DB_NAME_PREFIX', 'cbotdev_')
}

rdc = {
    'host': os.environ.get('REDIS_HOST', 'localhost'),
    'port': os.environ.get('REDIS_PORT', '6379'),
    'db':   os.environ.get('REDIS_DB', '0')
}
