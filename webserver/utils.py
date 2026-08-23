import logging
from logging.handlers import RotatingFileHandler
from functools import wraps
from flask import request, jsonify
from jsonschema import validate, ValidationError

def setup_logger(log_file, max_bytes, backup_count):
    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger('server')
    if not any(isinstance(h, RotatingFileHandler) for h in logger.handlers):
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
    return logger


logger = logging.getLogger('server')

def init_app(app):
    global logger
    logger = setup_logger(
        log_file=app.config.get('LOG_FILE', 'server.log'),
        max_bytes=app.config.get('LOG_MAX_BYTES', 10 * 1024 * 1024),
        backup_count=app.config.get('LOG_BACKUP_COUNT', 5)
    )


def validate_json(required_fields):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                logger.warning("Requête sans JSON")
                return jsonify({'error': 'Format JSON requis.'}), 400
            data = request.get_json()
            missing = [field for field in required_fields if field not in data]
            if missing:
                logger.warning(f"Champs manquants : {missing}")
                return jsonify({'error': f"Champs manquants : {', '.join(missing)}"}), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator

def validate_json_schema(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                validate(instance=request.get_json(), schema=schema)
            except ValidationError as e:
                logger.warning(f"Validation JSON échouée : {e.message}")
                return jsonify({'error': f"Validation JSON échouée : {e.message}"}), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator