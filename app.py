from flask import Flask
from config.config import Config
from web.routes import web

app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(web)

if __name__ == '__main__':
    app.run()