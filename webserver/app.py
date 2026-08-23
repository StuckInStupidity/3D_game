import os
import signal
from flask import Flask, jsonify, request, flash, redirect, url_for, render_template
from flask_cors import CORS
from markupsafe import escape
from werkzeug.exceptions import HTTPException
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity, create_access_token
from config import Config
from database import db, User
from auth import auth_bp, bcrypt, login_manager
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf, CSRFError
from room import RoomManager
import utils

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
utils.init_app(app)
logger = utils.logger
CORS(app, origins=Config.CORS_ORIGINS, supports_credentials=True)
jwt = JWTManager(app)
csrf = CSRFProtect(app)

@app.context_processor
def csrf_context():
    return dict(csrf_token=generate_csrf)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    flash("Security check failed. Please refresh the page and try again.", "error")
    return redirect(url_for("auth.sign"))

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

with app.app_context():
	db.create_all()

socketio = SocketIO(
    app,
    cors_allowed_origins=Config.CORS_ORIGINS,
    message_queue=Config.SOCKETIO_MESSAGE_QUEUE,
    async_mode='eventlet'  # ou 'gevent'
)

room_manager = RoomManager(
    client_timeout=Config.CLIENT_TIMEOUT,
    room_timeout=Config.ROOM_TIMEOUT,
    max_players=Config.MAX_PLAYERS_PER_ROOM
)

app.register_blueprint(auth_bp, url_prefix='/auth')

MESSAGE_SCHEMA = {
    "type": "object",
    "properties": {
        "room_code": {"type": "string"},
        "sender": {"type": "string"},
        "payload": {"type": "object"}
    },
    "required": ["room_code", "sender", "payload"]
}

@app.route('/')
def hihan():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/devlog')
def devlog():
    return render_template("devlog.html")

@app.route('/credits')
def credits():
    return render_template("credits.html")

@app.route('/download')
def download():
    return render_template("cartoon.html")

""" Verif base de donnees server
@app.route('/health', methods=['GET'])
def health():
    try:
        db.session.execute('SELECT 1')
        return jsonify({'status': 'ok'}), 200
    except Exception as e:
        logger.error(f"Healthcheck DB failed: {e}")
        return jsonify({'status': 'error', 'details': str(e)}), 500
"""

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    text = "Server error."
    if isinstance(e, HTTPException):
        code = e.code
        messages = {
            400: "Invalid request.",
            401: "Unauthorized request.",
            403: "Forbidden.",
            404: "Page not found.",
            405: "Method not allowed.",
            408: "Request timeout.",
            415: "Invalid JSON payload.",
            429: "Too many requests.",
            500: "Internal server error.",
            502: "Bad gateway.",
            503: "Service unavailable.",
            504: "Gateway timeout."
        }
        text = messages.get(code, e.description)
    if code >= 500:
        logger.error(f"Erreur serveur : {e}")
    safe_text, safe_code = escape(text), escape(str(code))
    return render_template("error.html", text=safe_text, nb=safe_code), code

@socketio.on('join')
def handle_join(data):
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except Exception:
        emit('error', {'error': 'Authentification requise.'})
        return
    room_code = data.get('room_code')
    username = data.get('username')
    sid = request.sid
    if not room_code or not username:
        emit('error', {'error': 'room_code et username requis.'})
        return
    if room_code not in room_manager.rooms:
        emit('error', {'error': f"La room {room_code} n'existe pas."})
        return
    for existing_room, clients in room_manager.rooms.items():
        if sid in clients:
            emit('error', {'error': f"Vous êtes déjà dans la room {existing_room}."})
            return
    success = room_manager.add_client(room_code, sid, username)
    if not success:
        emit('error', {'error': f"La room {room_code} est pleine."})
        return
    join_room(room_code)
    emit('system', {'message': f"{username} a rejoint la room."}, room=room_code)
    logger.info(f"Client {sid} ({username}) rejoint room {room_code}")

@socketio.on('leave')
def handle_leave(data):
    room_code = data.get('room_code')
    sid = request.sid
    leave_room(room_code)
    room_manager.remove_client(room_code, sid)
    emit('system', {'message': 'Un utilisateur a quitté la room.'}, room=room_code)
    logger.info(f"Client {sid} quitte room {room_code}")

@socketio.on('message')
@utils.validate_json_schema(MESSAGE_SCHEMA)
def handle_message(data):
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except Exception:
        emit('error', {'error': 'Authentification requise.'})
        return
    room_code = data['room_code']
    sender = data['sender']
    payload = data['payload']
    sid = request.sid
    room_manager.update_activity(room_code, sid)
    emit('message', {'sender': sender, 'payload': payload}, room=room_code)
    logger.info(f"Message relayé dans room {room_code} par {sender}")

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    for room_code, clients in list(room_manager.rooms.keys()):
        if sid in clients:
    	    leave_room(room_code)
    	    room_manager.remove_client(room_code, sid)
    	    emit('system', {'message': 'Un utilisateur a été déconnecté.'}, room=room_code)
    logger.info(f"Client {sid} déconnecté.")

def graceful_shutdown(*args):
    logger.info("Arrêt du serveur demandé, nettoyage en cours...")
    room_manager.shutdown()
    socketio.stop()

signal.signal(signal.SIGTERM, graceful_shutdown)
signal.signal(signal.SIGINT, graceful_shutdown)

if __name__ == '__main__':
	try:
		socketio.run(app, host='0.0.0.0', port=5000, debug=Config.DEBUG)
	except KeyboardInterrupt:
		graceful_shutdown()
