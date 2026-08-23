import threading
import time
from collections import defaultdict
from utils import logger

class RoomManager:
    def __init__(self, client_timeout, room_timeout, max_players):
        self.rooms = defaultdict(dict)  # {room_code: {sid: {'last_seen': timestamp, 'username': ...}}}
        self.client_timeout = client_timeout
        self.room_timeout = room_timeout
        self.max_players = max_players
        self.shutdown_flag = threading.Event()
        self.lock = threading.Lock()
        self.cleaner_thread = threading.Thread(target=self._clean_inactive_clients, daemon=True)
        self.cleaner_thread.start()

    def add_client(self, room_code, sid, username):
        with self.lock:
            if len(self.rooms[room_code]) >= self.max_players:
            	logger.warning(f"Tentative de rejoindre room {room_code} pleine")
            	return False
            self.rooms[room_code][sid] = {'last_seen': time.time(), 'username': username}
            logger.info(f"Client {sid} rejoint la room {room_code} ({username})")
            return True

    def remove_client(self, room_code, sid):
        with self.lock:
            if sid in self.rooms[room_code]:
                del self.rooms[room_code][sid]
                logger.info(f"Client {sid} quitte la room {room_code}")
            if not self.rooms[room_code]:
                del self.rooms[room_code]
                logger.info(f"Room {room_code} supprimée (vide)")

    def update_activity(self, room_code, sid):
        with self.lock:
            if sid in self.rooms[room_code]:
                self.rooms[room_code][sid]['last_seen'] = time.time()

    def get_clients(self, room_code):
        with self.lock:
            return list(self.rooms[room_code].keys())

    def _clean_inactive_clients(self):
        while not self.shutdown_flag.is_set():
            now = time.time()
            with self.lock:
                for room_code in list(self.rooms.keys()):
                    for sid in list(self.rooms[room_code].keys()):
                        if now - self.rooms[room_code][sid]['last_seen'] > self.client_timeout:
                            logger.info(f"Suppression client inactif {sid} de la room {room_code}")
                            del self.rooms[room_code][sid]
                    if not self.rooms[room_code]:
                        logger.info(f"Suppression room inactive {room_code}")
                        del self.rooms[room_code]
            self.shutdown_flag.wait(timeout=10)


    def shutdown(self):
        self.shutdown_flag.set()
        self.cleaner_thread.join()