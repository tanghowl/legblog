import os

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sqluser = os.getenv('SQLUSER')
possword = os.getenv('SQLPW')
database = os.getenv('DATABASE')


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECODE_QUERIES = True

    CKEDIRTOR_ENABLE_CSRF = True
    CKEDIRTOR_FILE_UPLOADER = 'admin.upload_image'

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('MyBlog Amdin', MAIL_USERNAME)

    LEGBLOG_EMAIL = os.getenv('LEGBLOG_EMAIL', 'tanghowl@163.com')
    LEGBLOG_POST_PER_PAGE = 10
    LEGBLOG_MANAGE_POST_PER_PAGE = 15
    LEGBLOG_COMMENT_PER_PAGE = 15
    LEGBLOG_THEMES = {'black_swan': 'Black Swan', 'perfect_blue': 'Perfect Blue'}
    LEGBLOG_SLOW_QUERY_THERSHOLD = 1

    LEGBLOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    LEGBLOG_ALLOWED_IMAGE_EXTENDSIONS = ['png', 'jpg', 'jpeg', 'gif']


class DevelopmentConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{sqluser}:{possword}@127.0.0.1:3306/{database}'


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{sqluser}:{possword}@127.0.0.1:3306/{database}'


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{sqluser}:{possword}@127.0.0.1:3306/{database}'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
