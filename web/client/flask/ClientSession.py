from flask import Flask, request
from flask_socketio import SocketIO, emit

from client.connections.ServerConnectionHandler import WebServerConnectionHandler
from common.ConnectionUtils import ConnectionUtils

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory registry for active client states
CLIENT_REGISTRY = {}

class ClientState:
    def __init__(self, session_id):
        self.session_id = session_id
        self.handler: WebServerConnectionHandler = WebServerConnectionHandler(send_callback=self._send_to_client)

    def _send_to_client(self, event_name, payload):
        emit(event_name, payload, to=self.session_id)

@socketio.on('connect')
def handle_connect():
    sid = request.sid
    CLIENT_REGISTRY[sid] = ClientState(session_id=sid)
    print(f"Client connected: {sid}")

@socketio.on('*')
def handle_key_exchange(event, data):
    sid = request.sid
    client_state: ClientState = CLIENT_REGISTRY.get(sid)
    
    if client_state:
        client_state.handler.handle_msg_map(data)

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    CLIENT_REGISTRY.pop(sid, None)
    print(f"Client disconnected: {sid}")

if __name__ == '__main__':
    socketio.run(app, host=ConnectionUtils.HOST, port=ConnectionUtils.PORT, debug=False)