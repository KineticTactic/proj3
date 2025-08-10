from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object('config')

    # Import routes
    from . import routes

    return app

app = create_app()