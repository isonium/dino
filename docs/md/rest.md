## RESTful API

### Message received

When user A receives a private message, or a message from a room that user A is in, the event `gn_message` will be sent
to user A with the following content:

    {
        "id": "<server-generated UUID>",
        "published": "<server-generated timestamp, RFC3339 format>",
        "actor": {
            "id": "<UUID of the sender>",
            "summary": "<name of the sender>"
        },
        "verb": "send",
        "target": {
            "id": "<UUID of the room, or this user's UUID if private msg>",
            "displayName": "<name of the room, or empty if private msg>",
            "objectType": "<room/private>"
        },
        "object": {
            "content": "<the message body>",
            "url": "<UUID of the channel for this room, or empty if private msg>"
        }
    }

### Invitation received

When user B invites user A to join room X, the event `gn_invitation` will be sent to user A with the following content:

    {
        "id": "<server-generated UUID>",
        "published": "<server-generated timestamp, RFC3339 format>",
        "actor": {
            "id": "<UUID of user B>",
            "summary": "<name of user B>"
        },
        "verb": "invite",
        "object": {
            "url": "<UUID of the channel for room X>",
            "summary": "<name of the channel for room X>"
        },
        "target": {
            "id": "<UUID of the room>",
            "displayName": "<name of the room>"
        }
    }

### Another user joins the room 

If user A is in room X, and another user B joins room X, the server will send an event called `gn_user_joined` to user A
with the following content:

    {
        "id": "<server-generated UUID>",
        "published": "<server-generated timestamp, RFC3339 format>",
        "actor": {
            "id": "<user B's UUID>",
            "summary": "<name of user B>",
            "image": {
                "url": "<user B's image url>"
            }
        },
        "target": {
            "id": "<uuid of the room>",
            "displayName": "<name of the room>"
        },
        "verb": "join"
    }

### Another user leaves room

When user A is in room X, and another user B leaves room X, the sever will send an event called `gn_user_left` to user A
with the following content:

    {
        "id": "<server-generated UUID>",
        "published": "<server-generated timestamp, RFC3339 format>",
        "actor": {
            "id": "<user B's UUID>",
            "summary": "<name of user B>",
        },
        "target": {
            "id": "<uuid of the room>",
            "displayName": "<name of the room>"
        },
        "verb": "leave"
    }

### Another user disconnects

If user A is in any room that user B is in, and user B disconnects from the chat server, an event called
`gn_user_disconnected` will be sent to user A with the following content:

    {
        "id": "<server-generated UUID>",
        "published": "<server-generated timestamp, RFC3339 format>",
        "actor": {
            "id": "<user B's UUID>",
            "summary": "<name of user B>",
        },
        "verb": 'disconnect'
    }

### A new room is created

When a new room is created in a channel that user A is in, an event called `gn_room_created` will be sent to user A with
the following content:

    {
        "id": "<server-generated UUID>",
        "published": "<server-generated timestamp, RFC3339 format>",
        "actor": {
            "id": "<UUID of user who created the room>",
            "summary": "<name of the user who created the room>",
        },
        "object": {
            "url": "<UUID of the channel for this room>"
        },
        "target": {
            "id": "<UUID of the new room>",
            "displayName": "<name of the new room>"
        },
        "verb": "create"
    }

### A user is kicked from a room

When a user is kicked from a room, an event will be sent to all users in that room (except the kicked user), called 
`gn_user_kicked`, with the following content:

    {
        "id": "<server-generated UUID>",
        "published": "<server-generated timestamp, RFC3339 format>",
        "actor": {
            "id": "<UUID of the kicker>",
            "summary": "<name of the kicker>"
        },
        "object": {
            "id": "<UUID of the kicked user>",
            "summary": "<name of the kicked user>"
        },
        "target": {
            "id": "<UUID of the room the user was kicked from>",
            "displayName": "<name of the room the user was kicked from>"
        },
        "verb": "kick"
    }

### A user is banned

TODO: currently the user will be banned, but the "kicked" event will be broadcasted to relevant users. There's currently
no "banned" event for this.