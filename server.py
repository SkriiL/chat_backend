from aiohttp import web
import socketio
import messages
import users

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('message')
async def print_message(sid, message):
    sio.enter_room(sid, 'standard')
    await send_message(message, 'standard', sid)
    print("Socket ID: ", sid)
    print(message)


@sio.on('connect')
def connect(sid, environ):
    print(sid + " connected")
    sio.enter_room(sid, room='standard')


@sio.on('getUserById')
async def get_user_by_id(sid, id_str):
    user = users.get_single_by_id(id_str)
    await send_user(sid, user)


@sio.on('getUserByName')
async def get_user_by_username(sid, username):
    user = users.get_single_by_username(username)
    await send_user(sid, user)


@sio.on('addUser')
async def add_user(sid, user_str):
    users.add(user_str)


@sio.on('getAllUsers')
async def get_all_users(sid, arg):
    all_users = users.get_all()
    await send_all_users(sid, all_users)


@sio.on('editUser')
async def edit_user(sid, user_str):
    users.edit(user_str)


@sio.on('deleteUser')
async def delete_user(sid, id_str):
    users.delete_by_id(id_str)


async def send_all_users(sid, users):
    await sio.emit('allUsers', users, room=sid)


async def send_user(sid, user):
    await sio.emit('user', user, room=sid)


async def send_message(message, room, sid):
    message = messages.message_to_list(message)
    await sio.emit('message', message, room=room, skip_sid=sid)


app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, port='56789')