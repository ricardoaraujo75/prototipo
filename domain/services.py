import hashlib, requests, json, base64
from flask import session
from config.config import Config

class SessionService:

    def session_init(self):
        if not 'id_token' in session or not session['id_token']:
            session['id_token'] = False
        return session

class LoginService:

    def id_token_decoder(self, id_token):
        header  = json.loads(base64.b64decode(id_token.split('.')[0] + '=='))
        payload = json.loads(base64.b64decode(id_token.split('.')[1] + '=='))
        session['username'] = payload['name']
        session['uid'] = payload['preferred_username']

    def get_level(self, access_token):
        if 'id_token' in session or session['id_token']:
            headersList = {
                "Content-Type": "application/x-www-form-urlencoded"
            }
            payload = "&client_id=" \
            + Config.SSO_CLIENTID \
            + "&client_secret=" \
            + Config.SSO_CLIENTSECRET \
            + "&grant_type=client_credentials" \
            + "&scope=openid"
            client_response = requests.request("POST", Config.RHSSO_TOKEN_URL, \
            data=payload,  headers=headersList)
            if client_response.status_code == 200:
                client_token = json.loads(client_response.text)
                levelHeadersList = {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": "Bearer " + client_token['access_token']
                }
                levelPayload = "token=" + access_token
                level_response = requests.request("GET", Config.RHSSO_LEVEL_URL, \
                data=levelPayload,  headers=levelHeadersList)
                if level_response.status_code == 200:
                    level = json.loads(level_response.text)
                    session['level'] = level
                    for x in session['level']:
                        if int(x['id']) > 1:
                            session['level'] = True
                        else:
                            session['level'] = False
                else:
                    session['level'] = False
            else:
                session['client_token'] = False
            return session['level']

    def login(self, code):
        headersList = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = "code=" + code + "&client_id=" \
        + Config.SSO_CLIENTID \
        + "&client_secret=" \
        + Config.SSO_CLIENTSECRET \
        + "&redirect_uri=" \
        + Config.SSO_REDIRECTURI \
        + "&grant_type=authorization_code" \
        + "&scope=openid"
        response = requests.request("POST", Config.RHSSO_TOKEN_URL, \
        data=payload,  headers=headersList)

        if response.status_code == 200:
            token = json.loads(response.text)
            session['id_token'] = token['id_token']
            self.id_token_decoder(session['id_token'])
            level_response = self.get_level(token['access_token'])
            return response.status_code
        else:
            return response.status_code

    def logout(self):
        if 'id_token' in session or session['id_token']:
            RHSSO_LOGOUT_URL = "https://" \
            + Config.SSO_BASE_URL \
            + "/auth/realms/rj/protocol/openid-connect/logout" \
            + "?post_logout_redirect_uri=" \
            + Config.SIG_BASE_URL \
            + "&id_token_hint=" \
            + session['id_token']
            session.pop('doc_signed', None)
            session.pop('id_token', None)
            session.pop('username', None)
            session.pop('uid', None)
            session.pop('level', None)
            return RHSSO_LOGOUT_URL

class UploadService:

    def calculate_sha256(self, file_to_hash):

        sha256_hash = hashlib.sha256()
        for byte_block in iter(lambda: file_to_hash.read(4096), b""):
            sha256_hash.update(byte_block)
        return sha256_hash.digest()

    def upload(self, request):
        file = request.files['fileToUpload']
        file_name = request.files['fileToUpload'].filename
        session['hashes'] = {
            file_name: self.calculate_sha256(file)
        }
        return session

class SignatureService:

    def sign_token(self, code):
        headers_token = {
        "Content-Type": "application/x-www-form-urlencoded"
        }
        payload_token = "code=" + code + "&client_id=" \
        + Config.SIG_CLIENTID \
        + "&client_secret=" \
        + Config.SIG_CLIENTSECRET \
        + "&redirect_uri=" \
        + Config.SIG_REDIRECTURI \
        + "&grant_type=authorization_code"
        response_token = requests.request("POST", Config.SIGNATURE_TOKEN_URL, \
        data=payload_token, headers=headers_token)
        if response_token.status_code == 200:
            token = json.loads(response_token.text)
            access_token = token['access_token']
            return access_token
        elif response_token.status_code == 401:
            access_token = response_token.status_code
            return access_token
        else:
            access_token = None
            return access_token

    def get_cert(self, access_token):
        headers_cert = {
            "Authorization": f"Bearer {access_token}"
        }
        cert_base64 = requests.request("GET", Config.SIGNATURE_CERTIFICATE_URL, \
        headers=headers_cert)
        if cert_base64.status_code == 200:
            # cert = json.loads(cert_base64.text)
            return cert_base64
        else:
            cert_base64 = None
            return cert_base64

    def sign_file(self, access_token):
        headers_signing = {
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/json",
        }
        signatures = {}
        for file_name, file_hash in session['hashes'].items():
            base64_encoded = base64.b64encode(file_hash).decode('utf-8')
            signature_package = json.dumps({'hashBase64': base64_encoded})
            signature_base64 = requests.request("POST", Config.SIGNATURE_SIGNING_URL, \
            data=signature_package, headers=headers_signing)
            if signature_base64.status_code == 200:
                signatures[file_name] = signature_base64.text
            elif signature_base64.status_code == 403:
                session['doc_signed'] = False
                return session
        if len(signatures) != 0:
            session['doc_signed'] = True
            return session
        else:
            session['doc_signed'] = False
            return session