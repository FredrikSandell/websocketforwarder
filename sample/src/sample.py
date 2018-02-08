import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
import pika
import os


sock = None
close_count = 0
connection = None
channel = None


def start_rabbitmq_connection():
    global connection
    global channel
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='mq'))
    channel = connection.channel()
    channel.queue_declare(queue='forwardedmsg')

def forward(msg):
    global channel
    channel.basic_publish(exchange='',
                      routing_key='forwardedmsg',
                      body=msg)
    print("forwarded message")

def start_connection():
    sock = websocket.WebSocketApp("ws://echo.websocket.org/",
                                  on_message=on_message,
                                  on_error=on_error,
                                  on_close=on_close)
    sock.on_open = on_open
    sock.run_forever()

def on_message(ws, message):
    forward(message)

def on_error(ws, error):
    print("Got error")
    print(error)
    start_connection()

def on_close(ws):
    global close_count
    print("socket closed")
    print("Close count {}".format(close_count))
    close_count += 1
    if close_count < 2:
        print("need to reopen the connection")
        start_connection()



def on_open(ws):
    # everything here is just to get a response from the echo server
    def run(*args):
        for i in range(300):
            time.sleep(1)
            ws.send("Msg %d" % i)
            time.sleep(1)
        ws.close()
    thread.start_new_thread(run, ())

if __name__ == "__main__":
    time.sleep(2)
    start_rabbitmq_connection()
    start_connection()
