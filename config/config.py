import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')

    SSO_BASE_URL = os.environ.get('FLASKAPP_RHSSO_SIS_BASE_URL')
    SSO_CLIENTID = os.environ.get('FLASKAPP_RHSSO_SIS_CLIENTID')
    SSO_CLIENTSECRET = os.environ.get('FLASKAPP_RHSSO_SIS_SECRET')
    SSO_REDIRECTURI = os.environ.get('FLASKAPP_RHSSO_SIS_REDIRECT_URI')

    SIG_BASE_URL = os.environ.get('ASSELETRONICA_BASE_URI')
    SIG_LOGINURI = os.environ.get('ASSELETRONICA_SERVIDOROAUTH')
    SIG_REDIRECTURI = os.environ.get('ASSELETRONICA_REDIRECT_URI')
    SIG_CLIENTID = os.environ.get('ASSELETRONICA_CLIENTID')
    SIG_CLIENTSECRET = os.environ.get('ASSELETRONICA_SECRET')
    SIG_CLOUDSERVER = os.environ.get('ASSELETRONICA_SERVIDORNUVEMQUALIFICADA')

    RHSSO_LOGIN_URL = "https://" \
    + SSO_BASE_URL \
    + "/auth/realms/rj/protocol/openid-connect/auth?response_type=code&client_id=" \
    + SSO_CLIENTID \
    + "&redirect_uri=" \
    + SSO_REDIRECTURI \
    + "&scope=openid"

    RHSSO_TOKEN_URL = "https://" \
    + SSO_BASE_URL \
    + "/auth/realms/rj/protocol/openid-connect/token"

    RHSSO_LEVEL_URL = "https://" \
    + SSO_BASE_URL \
    + "/auth/realms/rj/spi-selos-api/level"

    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

    SIGNATURE_LOGIN_URL = "https://" \
    + SIG_LOGINURI \
    + "/authorize?response_type=code" \
    + "&redirect_uri=" \
    + SIG_REDIRECTURI \
    + "&scope=sign" \
    + "&client_id=" \
    + SIG_CLIENTID

    SIGNATURE_TOKEN_URL = "https://" \
    + SIG_LOGINURI \
    + "/token"

    SIGNATURE_CERTIFICATE_URL = "https://" \
    + SIG_CLOUDSERVER \
    + "/certificadoPublico"

    SIGNATURE_SIGNING_URL = "https://" \
    + SIG_CLOUDSERVER \
    + "/assinarPKCS7"