from flask import Flask, render_template, request, session, redirect, url_for
from string import ascii_uppercase
import random
from flask_socketio import join_room, leave_room, send, SocketIO
from datetime import datetime

app = Flask(__name__)
app.secret_key = "hellosecretkey"
socketio = SocketIO(app)

rooms = {}


def get_current_datetime():
    datetime_string = datetime_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return datetime_string

def generate_room_code(length):
    code = ""
    for i in range(length):
        code = code + random.choice(ascii_uppercase)

    if code in rooms:
        generate_room_code(length)
    else:
        return code

@app.route('/', methods=["GET", "POST"])
def index():
    print(rooms)
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        roomcode = request.form.get("roomcode")
        join_room = request.form.get("join-room", False)
        create_room = request.form.get("create-room", False)

        # data = [username, roomcode, join_room, create_room]
    
        if join_room != False:
            if roomcode == "":
                return render_template('index.html', message="Please Input Valid Room Code")
            elif roomcode not in rooms:
                return render_template('index.html', message="Room does not Exist")
            else:
                room = roomcode
        elif create_room != False:
            room = generate_room_code(4)
            rooms[room] = {"members": 0, "messages": []}

        session["room"] = room
        session["username"] = username

        return redirect(url_for('room'))

    else:
        return render_template('index.html')
    

@app.route("/room", methods=["GET"])
def room():
    room = session.get("room")
    if room is None:
        return redirect(url_for("index"))
    
    return render_template("room.html", roomcode=room)


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

    send({"name": username, "message": "has entered the room", "datetime": get_current_datetime()}, to=room)

    rooms[room]["members"] += 1
    print(f"{username} entered room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    username = session.get("username")

    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
        
    send({"name": username, "message": "has left the room", "datetime": get_current_datetime()}, to=room)
    print(f"{username} left room {room}")

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

    print(f"{session.get('name')} sent: {data['data']}")


if __name__ == '__main__':
    app.run(debug=True)