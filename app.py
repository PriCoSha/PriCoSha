from flask import Flask
from config import config


def create_app(config_name):
    # Initialize app from flask
    app = Flask(__name__)
    print("Running in %s config" % config_name)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # register api blueprint
    from api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # static pages
    @app.route('/')
    def hello_world():
        return 'Hello World!'

    return app


if __name__ == '__main__':
    myapp = create_app('development')
    myapp.run()
