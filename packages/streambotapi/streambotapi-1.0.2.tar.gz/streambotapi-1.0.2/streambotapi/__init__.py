import os
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from streambot import StreamBot

class StreamBotAPI:
    def __init__(self, streambots, host='0.0.0.0', port=80, origins=['*']):
        self.host = host
        self.port = port
        self.streambots = streambots
        self.origins = origins

        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app, cors_allowed_origins="*", websocket=True)
        self.init_cors()
        self.init_routes()

        self.messages = {}

    def init_cors(self):
        CORS(self.app, resources={r"/api/*": {"origins": self.origins}})

    def init_routes(self):
        self.app.route('/api/getmessages/<context_id>/<user_id>', methods=['GET', 'POST'])(self.get_messages)
        self.app.route('/api/messages', methods=['POST'])(self.handle_messages)
        self.app.route('/api/newchat', methods=['POST'])(self.reset_chat)

    def chat_stream(self, messages, context_id):
        print(f'Context ID: {context_id}')
        print(self.streambots[int(context_id)].messages)
        for event in self.streambots[int(context_id)].chat_stream(messages):
            yield event

    def get_messages(self, context_id, user_id):
        connection_id = f"{context_id}_{user_id}"
        if connection_id in self.messages:
            return jsonify(self.messages[connection_id])
        else:
            self.messages[connection_id] = self.streambots[int(context_id)].messages
            return jsonify(self.messages[connection_id])

    def handle_messages(self):
        context_id = request.json.get('context_id')
        user_id = request.json.get('user_id')
        connection_id = f"{context_id}_{user_id}"

        if connection_id in self.messages:
            self.messages[connection_id].append({"role": "user", "content": request.json.get('message')})
        else:
            self.messages[connection_id] = [{"role": "user", "content": request.json.get('message')}]

        response = ""

        for event in self.chat_stream(self.messages[connection_id], context_id=context_id):
            response += event
            self.socketio.emit('message', {'message': event, 'connection_id': connection_id}, room=user_id, broadcast=True)

        self.messages[connection_id].append({"role": "assistant", "content": response})
        return jsonify(self.messages[connection_id])
    

    def reset_chat(self):
        context_id = request.json.get('context_id')
        user_id = request.json.get('user_id')
        connection_id = f"{context_id}_{user_id}"
        if connection_id in self.messages:
            print('resetting conversation')
            self.messages[connection_id] = self.streambots[int(context_id)].messages
        return jsonify(True)

    def start(self):
        self.app.run(host=self.host, port=self.port)
