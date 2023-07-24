from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room
import wave
import base64

app = Flask(__name__)
#app.secret_key = 'random secret key!'
socketio = SocketIO(app, cors_allowed_origins="*")



def read_wave_file(file_path):
    with wave.open(file_path, 'rb') as wf:
        return wf.readframes(wf.getnframes())

@socketio.on('stream_audio')
def stream_audio(message):
    room = message['room']
    #audio_data = read_wave_file('D:\\workspace\\originAI\\socket_server\\voice_file\\long.wav')
    audio_data = read_wave_file('./voice_file/long.wav')
    # Encode audio data to base64 to transmit as a string
    encoded_audio_data = base64.b64encode(audio_data).decode('utf-8')
    print("AudioEvent: {} has sent the audio:\n {}\n".format(message['username'], "audio_data"))
    emit('audio_data',encoded_audio_data, to=room)



@socketio.on('join')
def join(message):
    username = message['username']
    room = message['room']
    join_room(room)
    print('RoomEvent: {} has joined the room {}\n'.format(username, room))
    emit('ready', {username: username},to=room)


@socketio.on('data')
def transfer_data(message):
    username = message['username']
    room = message['room']
    data = message['data']
    print('DataEvent: {} has sent the data:\n {}\n'.format(username, data))
    emit('data', data,to=room)


@socketio.on_error_default
def default_error_handler(e):
    print("Error: {}".format(e))
    socketio.stop()


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5004)