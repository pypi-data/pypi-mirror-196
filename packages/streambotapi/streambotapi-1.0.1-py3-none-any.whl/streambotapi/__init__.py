import os
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from streambot import StreamBot

class StreamBotAPI:
    def __init__(self, streambot, host='0.0.0.0', port=80, origins=['*']):
        self.host = host
        self.port = port
        self.streambot = streambot
        self.origins = origins

        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*", websocket=True)
        self.init_cors()
        self.init_routes()

        self.messages = {}

    def init_cors(self):
        CORS(self.app, resources={r"/api/*": {"origins": self.origins}})

    def init_routes(self):
        self.app.route('/api/getmessages/<user_id>', methods=['GET', 'POST'])(self.get_messages)
        self.app.route('/api/messages', methods=['GET', 'POST'])(self.handle_messages)
        self.app.route('/api/newchat', methods=['POST'])(self.reset_chat)

    def chat_stream(self, messages):
        for event in self.streambot.chat_stream(messages):
            yield event

    def get_messages(self, user_id):
        connection_id = user_id
        if connection_id in self.messages:
            return jsonify(self.messages[connection_id])
        else:
            self.messages[connection_id] = self.streambot.messages
            return jsonify(self.messages[connection_id])

    def handle_messages(self):
        connection_id = request.json.get('connection_id')

        if connection_id in self.messages:
            self.messages[connection_id].append({"role": "user", "content": request.json.get('message')})
        else:
            self.messages[connection_id] = [{"role": "user", "content": request.json.get('message')}]
        response = ""
        for event in self.chat_stream(self.messages[connection_id]):
            response += event
            self.socketio.emit('message', {'message': event, 'connection_id': connection_id}, room=connection_id, broadcast=True)
        self.messages[connection_id].append({"role": "assistant", "content": response})
        return jsonify(self.messages[connection_id])

    def reset_chat(self):
        connection_id = request.json.get('connection_id')
        if connection_id in self.messages:
            self.messages[connection_id] = []
        return jsonify(True)

    def start(self):
        self.app.run(host=self.host, port=self.port)
