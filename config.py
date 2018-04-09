"""
This file is the configuration object in which we set the path to the database and other SQLAlchemy options.
Also, the secret key is set so that we can use encrypted sessions for logging into the application
"""

class Config(object):
	SECRET_KEY = 'temp_secret_key' # We should probably change this to an environment variable later