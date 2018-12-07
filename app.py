from flask import Flask, render_template
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
    def index():
        return render_template("index.html")

    @app.route('/login.html')
    def login_page():
        return render_template("login.html")

    @app.route('/postContent.html')
    def postContent():
        return render_template("postContent.html")

    @app.route('/tagCenter.html')
    def tc():
        return render_template("tagCenter.html")

    @app.route('/contentPage.html')
    def cp():
        return render_template("contentPage.html")

    @app.route('/postTag.html')
    def pt():
        return render_template("postTag.html")

    @app.route('/postRate.html')
    def pr():
        return render_template("postRate.html")

    return app


if __name__ == '__main__':
    app = create_app("development")
    app.run()
