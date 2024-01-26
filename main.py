from flask import Flask, render_template, request, session, redirect, url_for
from string import ascii_uppercase
import random

app = Flask(__name__)
app.secret_key = "hellosecretkey"

rooms = {}

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
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        roomcode = request.form.get("roomcode")
        join_room = request.form.get("join-room", False)
        create_room = request.form.get("create-room", False)

        data = [username, roomcode, join_room, create_room]
        print(rooms)

        if join_room != False:
            if roomcode == "":
                return render_template('index.html', message="Please Input Valid Room Code")
            elif roomcode not in rooms:
                return render_template('index.html', message="Room does not Exist")
            else:
                room = roomcode
        else:
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
    
    return render_template("room.html")



if __name__ == '__main__':
    app.run(debug=True)