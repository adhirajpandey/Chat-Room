from flask import Flask, render_template, request, session, jsonify, abort
from flask_socketio import join_room, leave_room, send, SocketIO
from flask_cors import CORS
from utils import get_current_datetime, generate_room_code, rooms

app = Flask(__name__)
CORS(app)
app.secret_key = "hellosecretkey"
socketio = SocketIO(app)

@app.route('/', methods=["GET", "POST"])
def index():
    session.clear()
    if request.method == "POST":
        json_data = request.get_json(force=True)

        username = json_data.get("username")
        request_type = json_data.get("requestType")
        roomcode = json_data.get("roomCode", None)

        if request_type == "join-room":
            if roomcode == "" or len(roomcode) < 4:
                abort(400)
            elif roomcode not in rooms:
                abort(404)
            else:
                room = roomcode
        elif request_type == "create-room":
            if username == "" or len(username) < 2 or len(username) > 10:
                abort(400)
            else:
                room = generate_room_code(4)
                rooms[room] = {"members": 0, "messages": []}

        session["room"] = room
        session["username"] = username

        return jsonify({"msg": "SUCCESS"})

    else:
        return render_template('index.html', room_count=len(rooms))
    

@app.route("/room", methods=["GET"])
def room():
    room = session.get("room")
    if room is None or room not in rooms:
        abort(404)

    return render_template("room.html", room=room, messages=rooms[room]["messages"])


@socketio.on("connect")
def connect():
    room = session.get("room")
    username = session.get("username")

    if not room or not username:
        return None
    if room not in rooms:
        leave_room(room)
        return None

    join_room(room)

    send({"name": username, "message": "entered the room", "datetime": get_current_datetime()}, to=room)

    rooms[room]["members"] += 1

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    username = session.get("username")

    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
        
    send({"name": username, "message": "left the room", "datetime": get_current_datetime()}, to=room)

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return None
    
    content = {
        "name": session.get("username"),
        "message": data["data"],
        "datetime": get_current_datetime()
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')