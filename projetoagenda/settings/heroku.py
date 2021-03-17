import environ

from projetoagenda.settings.base import *

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# False if not in os.environ
DEBUG = env('DEBUG')

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    # read os.environ['DATABASE_URL'] and raises ImproperlyConfigured exception if not found
    'default': env.db(),
}

# EMAIL_HOST_USER = env('EMAIL_USER')
# EMAIL_HOST_PASSWORD = env('EMAIL_PASS')

AWS_S3_FILE_OVERWRITE = env('AWS_FILE_OVERWRITE')  # False
AWS_DEFAULT_ACL = env('AWS_DEFAULT_ACL')  # None
DEFAULT_FILE_STORAGE = env('AWS_DFT_FILE_STORAGE')  # 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
