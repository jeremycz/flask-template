import json
from logging.config import dictConfig
import os
from typing import Union

from flask import Flask

from app.settings import DefaultConfig


def load_config_from_json(path: str) -> dict():
    """"""
    config = dict()
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config


def create_app(app_config: Union[str, dict, None] = None) -> Flask:
    """"""
    # Setup logging
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    # Create app
    app = Flask(__name__)

    # Load default configuration
    app.config.from_object("app.settings.DefaultConfig")
    app.logger.info(app.config)

    # User configuration
    if isinstance(app_config, dict):
        app.config.update(app_config)
    elif isinstance(app_config, str):
        if os.path.isabs(app_config) and os.path.exists(app_config):
            _, file_ext = os.path.splitext(app_config)
            if file_ext == "json":
                app.config.update(load_config_from_json(app_config))
            elif file_ext in ("cfg", "py"):
                app.config.from_pyfile(app_config)
            else:
                app.logger.warn("Unrecognized extension for configuration file %s", app_config)
        elif os.path.exists(os.path.join(os.getcwd(), app_config)):
            config_path = os.path.join(os.getcwd(), app_config)
            _, file_ext = os.path.splitext(config_path)
            if file_ext == "json":
                app.config.update(load_config_from_json(config_path))
            elif file_ext in ("cfg", "py"):
                app.config.from_pyfile(config_path)
            else:
                app.logger.warn("Unrecognized extension for configuration file %s", config_path)
        elif os.getenv(app_config) is not None:
            app.config.from_envvar(app_config)
        else:
            app.config.from_object(app_config)
    elif isinstance(app_config, DefaultConfig):
        app.config.from_object(DefaultConfig)

    # Load blueprints

    # Allows access to application context during import
    with app.app_context():
        from app import model

    app.register_blueprint(model.bp)

    return app
