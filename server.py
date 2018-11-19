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
    #await send_single_user(sid, user)
    return user


async def send_single_user(sid, user):
    await sio.emit('user', user, room=sid)


async def send_message(message, room, sid):
    message = messages.message_to_list(message)
    await sio.emit('message', message, room=room, skip_sid=sid)


app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app, port='56789')