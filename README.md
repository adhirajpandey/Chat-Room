# Chat-Room

## Overview

This web application enables users to engage in live conversations within chat rooms. Any user has the ability to create a new chat room and share its unique code with multiple participants, who can then join the conversation using that code. 

Realtime two-way communication is achieved through the utilization of web sockets. HTML, JS and Tailwind used for frontend and Flask for backend.

Test it out at: https://chatroom.adhirajpandey.me/


## Features

- **Create Chat Rooms:** Effortlessly establish new chat rooms and share the unique room code with multiple users for quick and convenient communication.

- **Realtime Communication:** Enable seamless and instant two-way communication within the chat rooms using web sockets for a responsive and dynamic user experience.

- **User-Friendly Interface:** Intuitive and straightforward user interface, ensuring ease of use for all participants.

- **Containerized:** Availabilty of Dockerfile for easy deployments in self-hosting environment ensuring privacy over your data.

## Installation and Usage

1. Clone the project to your local system using: `git clone https://github.com/adhirajpandey/Chat-Room`.
2. Build docker image by running this command: `docker build -t chatroom .` in project directory.
3. Run the container using `docker run -d -p 5000:5000 chatroom`.


## To-Do

- [x] Maintain Message History
- [x] UI Improvements
- [x] Live Room Count
- [ ] Integrate DB for persistent storage
- [ ] Message Encryption

## Demonstration

- Youtube Demo Link: https://www.youtube.com/watch?v=aZolRUkhIb4
- Index Page Screenshot:
  
    ![chatroom_index1](https://github.com/adhirajpandey/Chat-Room/assets/87516052/90ba178c-27ea-4d48-a0ac-36de898092c3)

    
