import sys
from domain.services import SessionService, LoginService, UploadService, SignatureService
from config.config import Config
from flask import redirect, url_for, render_template, session, flash

class SessionController:

    def __init__(self, session_service: SessionService):
        self.session_service = session_service

    def new_session(self):
        self.session_service.session_init()

class LoginController:

    def __init__(self, login_service: LoginService):
        self.login_service = login_service

    def login(self, request):
        code = request.args.get('code')
        if code:
            resp_status = self.login_service.login(code)
            if resp_status == 200:
                return redirect(url_for('web.index'))
            else:
                return redirect(url_for('web.index'))
        return redirect(Config.RHSSO_LOGIN_URL)

    def logout(self, request):
        logout_url = self.login_service.logout()
        return redirect(logout_url)

class BusinessController:

    def business(self):
        if not 'id_token' in session or not session['id_token']:
            return redirect(url_for('web.index'))
        else:
            messages = None
            return render_template('pages/svempresa.html', messages=messages)

class ProccessController:

    def proccess(self):
        messages = None
        if not 'id_token' in session or not session['id_token']:
            return redirect(url_for('web.index'))
        elif not session['level']:
            flash('É necessária uma conta nível Prata ou Ouro para esta ação.', 'error')
            return redirect(url_for('web.business'))
        else:
            return render_template('pages/processo.html', messages=messages)

class UploadController:

    def __init__(self, upload_service: UploadService):
        self.upload_service = upload_service

    def upload(self, request):
        if not 'id_token' in session or not session['id_token']:
            return redirect(url_for('web.index'))
        else:
            if 'fileToUpload' not in request.files:
                return redirect(url_for('web.proccess'))
            self.upload_service.upload(request)
            if session['hashes']:
                return redirect(url_for('web.to_sign'))
            else:
                messages = json.dumps({"error":"Falha no upload. tente novamente."})
                flash('Falha no upload. tente novamente.', 'error')
                return redirect(url_for('web.proccess', messages=json.loads(messages)))

class SignatureController:

    def __init__(self, signature_service: SignatureService):
        self.signature_service = signature_service

    def to_sign(self, request):
        code = request.args.get('code')
        if code:
            token = self.signature_service.sign_token(code)
            if isinstance(token, str):
                cert = self.signature_service.get_cert(token)
                self.signature_service.sign_file(token)
                if session['doc_signed']:
                    flash('Operação executada com sucesso', 'success')
                    return redirect(url_for('web.business'))
                else:
                    flash('Falha na assinatura. tente novamente.', 'error')
                    return redirect(url_for('web.business'))
            elif token == 401:
                flash('Falha na assinatura. tente novamente.', 'error')
                return redirect(url_for('web.business'))
            else:
                flash('Falha no upload. tente novamente.', 'error')
                return redirect(url_for('web.business'))
        return redirect(Config.SIGNATURE_LOGIN_URL)