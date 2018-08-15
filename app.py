from flask import Flask
from redis import Redis, RedisError
import os
import socket

# Connect to Redis
redis = Redis(host="redis", db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled</i>"

    img_url = 'https://tr4.cbsistatic.com/hub/i/r/2017/10/13/1455bd12-7a96-48ee-8ad2-7af33d31017c/thumbnail/768x432/843ec3e4805e49358b2c9dc52100b373/20171010dockerjack.jpg'
    img2_url = 'https://blogs.gartner.com/richard-watson/files/2015/05/Worked-Fine-In-Dev-Ops-Problem-Now.jpg'

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}" \
           "<p><img src='{img_url}' alt='I <3 Docker'/></p>" \
           "<p><img src='{img2_url}' alt='Let it all burn'/></p>"

    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname(), visits=visits, img_url=img_url, img2_url=img2_url)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
