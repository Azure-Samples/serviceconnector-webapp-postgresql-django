from .settings import *
import requests

# Configure default domain name
ALLOWED_HOSTS = [os.environ['WEBSITE_SITE_NAME'] + '.azurewebsites.net', '127.0.0.1'] if 'WEBSITE_SITE_NAME' in os.environ else []

DEBUG = False

# WhiteNoise configuration
MIDDLEWARE = [                                                                   
    'django.middleware.security.SecurityMiddleware',
# Add whitenoise middleware after the security middleware                             
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',                      
    'django.middleware.common.CommonMiddleware',                                 
    'django.middleware.csrf.CsrfViewMiddleware',                                 
    'django.contrib.auth.middleware.AuthenticationMiddleware',                   
    'django.contrib.messages.middleware.MessageMiddleware',                      
    'django.middleware.clickjacking.XFrameOptionsMiddleware',                    
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


db_name = os.environ['AZURE_POSTGRESQL_NAME']
db_host = os.environ['AZURE_POSTGRESQL_HOST']
db_user = os.environ['AZURE_POSTGRESQL_USER']
db_password = os.environ['AZURE_POSTGRESQL_PASSWORD']

# Configure Postgres database, for connection string
DATABASES = {                                                                    
    'default': {                                                                 
        'ENGINE': 'django.db.backends.postgresql',                               
        'NAME': db_name,                                        
        'HOST': db_host,                                            
        'USER': db_user,                                            
        'PASSWORD': db_password                                         
    }                                                                            
}































# Configure Postgres database, for system-assigned msi
# resource_uri = 'https://ossrdbms-aad.database.windows.net'
# identity_endpoint = os.environ["IDENTITY_ENDPOINT"]
# identity_header = os.environ["IDENTITY_HEADER"]
# token_auth_uri = f"{identity_endpoint}?resource={resource_uri}&api-version=2019-08-01"
# head_msi = {'X-IDENTITY-HEADER':identity_header}

# resp = requests.get(token_auth_uri, headers=head_msi)
# access_token = resp.json()['access_token']

# DATABASES = {                                                                    
#     'default': {                                                                 
#         'ENGINE': 'django.db.backends.postgresql',                               
#         'NAME': os.environ['ResourceConnector_DBforPostgreSQL_SubResourceName'],                                            
#         'HOST': os.environ['ResourceConnector_DBforPostgreSQL_TargetServiceEndpoint'],                                            
#         'USER': os.environ['ResourceConnector_DBforPostgreSQL_Identity'],                                            
#         'PASSWORD': access_token,
#         'OPTIONS': {
#             'sslmode': 'require'
#         }                                         
#     }                                                                            
# }

# Configure Postgres database, for user-assigned msi
# resource_uri = 'https://ossrdbms-aad.database.windows.net'
# identity_endpoint = os.environ["IDENTITY_ENDPOINT"]
# identity_header = os.environ["IDENTITY_HEADER"]
# client_id = os.environ["Cupertino_DBforPostgreSQL_Identity"]
# token_auth_uri = f"{identity_endpoint}?resource={resource_uri}&api-version=2019-08-01&client_id={client_id}"
# head_msi = {'X-IDENTITY-HEADER':identity_header}

# resp = requests.get(token_auth_uri, headers=head_msi)
# access_token = resp.json()['access_token']

# DATABASES = {                                                                    
#     'default': {                                                                 
#         'ENGINE': 'django.db.backends.postgresql',                               
#         'NAME': os.environ['Cupertino_DBforPostgreSQL_SubResourceName'],                                            
#         'HOST': os.environ['Cupertino_DBforPostgreSQL_TargetServiceEndpoint'],                                            
#         'USER': os.environ['Cupertino_DBforPostgreSQL_Name'],                                            
#         'PASSWORD': access_token,
#         'OPTIONS': {
#             'sslmode': 'require'
#         }                                         
#     }                                                                            
# }
