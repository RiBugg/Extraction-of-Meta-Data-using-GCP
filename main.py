import os
import base64
from flask import Flask, request
from google.cloud import pubsub_v1

app = Flask(__name__)
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("integral-hold-462207-u2", "extraction-topic")

@app.route("/", methods=["POST"])
def handle_event():
    envelope = request.get_json()
    if not envelope:
        return "No event", 400
#store meta data and push msg
    name = envelope["name"]
    size = envelope["size"]
    content_type = envelope["contentType"]    
    message = f"Name: {name}, Size: {size}, Format: {content_type}"
    publisher.publish(topic_path, message.encode("utf-8"))

    return "OK", 200 
