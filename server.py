from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


async def index(request):
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('message')
def print_message(sid, message):
    sio.enter_room(sid, 'room')
    sio.emit('message', message, room='room')
    print("Socket ID: " , sid)
    print(message)


app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)