import os
from pathlib import Path
import json

class Config:
    SITE_ROOT = Path(__file__).resolve(strict=True).parent.parent
    BASE_DIR = os.path.join(Path(__file__).resolve(strict=True).parent.parent, 'manager')
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'public\\static')
    
    SECRET_KEY = 'im20*%v8+2kh$1997)wlf9owg)&w%r3wroj1o*o%(s0_cr%oa$'
    SQLALCHEMY_BINDS = json.load(open(f'{BASE_DIR}\\uri.json','r'))
    
    # Flask-Mail.
    MAIL_DEFAULT_SENDER = 'contact@local.host'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'ajay.patil.ap01@gmail.com'
    MAIL_PASSWORD = 'Apku1290'

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True


class DevConfig(Config):
    DB_PATH = os.path.join(Path(__file__).resolve(strict=True).parent.parent, 'manager\\dbs')
    ENVIRONMENT = 'development'
    DEBUG = True
    SERVER_NAME = 'localhost:8000'
    ALLOWED_HOSTS = ['*']
    LOG_LEVEL = 'DEBUG'  # CRITICAL / ERROR / WARNING / INFO / DEBUG
    
    db_uri = f'sqlite:///{DB_PATH}\\site.db'
    # db_uri = 'postgresql://postgres:apku1290@localhost:5432/agust_db'
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    STRIPE_SECRET_KEY = None
    STRIPE_PUBLISHABLE_KEY = None
    STRIPE_API_VERSION = '2016-03-07'
    STRIPE_PLANS = {
        '0': {
            'id': 'bronze',
            'name': 'Bronze',
            'amount': 100,
            'currency': 'usd',
            'interval': 'month',
            'interval_count': 1,
            'trial_period_days': 14,
            'statement_descriptor': 'SNAKEEYES BRONZE',
            'metadata': {
                'coins': 110
            }
        },
        '1': {
            'id': 'gold',
            'name': 'Gold',
            'amount': 500,
            'currency': 'usd',
            'interval': 'month',
            'interval_count': 1,
            'trial_period_days': 14,
            'statement_descriptor': 'SNAKEEYES GOLD',
            'metadata': {
                'coins': 600,
                'recommended': True
            }
        },
        '2': {
            'id': 'platinum',
            'name': 'Platinum',
            'amount': 1000,
            'currency': 'usd',
            'interval': 'month',
            'interval_count': 1,
            'trial_period_days': 14,
            'statement_descriptor': 'SNAKEEYES PLATINUM',
            'metadata': {
                'coins': 1500
            }
        }
    }

    
class ProdConfig(Config):
    ENVIRONMENT = 'production'
    DEBUG = False
    SERVER_NAME = '192.168.99.100'
    ALLOWED_HOSTS = ['192.168.99.100']
    LOG_LEVEL = 'INFO'  # CRITICAL / ERROR / WARNING / INFO / DEBUG

    db_uri = 'postgresql://postgres:apku1290@localhost:5432/agust_db'
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False