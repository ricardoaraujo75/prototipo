from flask import Blueprint, render_template, request
from .controllers import LoginController, SessionController, ProccessController, \
BusinessController, UploadController, SignatureController
from domain.services import LoginService, SessionService, UploadService, \
SignatureService

web = Blueprint('web', __name__)

login_service = LoginService()
login_controller = LoginController(login_service)
session_service = SessionService()
session_controller = SessionController(session_service)
proccess_controller = ProccessController()
business_controller = BusinessController()
upload_service = UploadService()
upload_controller = UploadController(upload_service)
signature_service = SignatureService()
signature_controller = SignatureController(signature_service)

@web.route('/')
def index():
    session_controller.new_session()
    return render_template('pages/home.html')

@web.route('/login', methods=['GET', 'POST'])
def login():
    return login_controller.login(request)

@web.route('/logout', methods=['POST'])
def logout():
    return login_controller.logout(request)

@web.route('/svempresa')
def business():
    # session_controller.new_session()
    return business_controller.business()

@web.route('/processo')
def proccess():
    return proccess_controller.proccess()

@web.route('/upload', methods=['POST'])
def upload():
    return upload_controller.upload(request)

@web.route('/assinar', methods=['GET', 'POST'])
def to_sign():
    return signature_controller.to_sign(request)