import os
from flask import Flask, request
from google.cloud import pubsub_v1

app = Flask(__name__)
publisher = pubsub_v1.PublisherClient()
PROJECT_ID = "integral-hold-462207-u2"
TOPIC_NAME = "extraction-topic"
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)

@app.route("/", methods=["POST"])
def handle_event():
    event_data = request.get_json()

    if not event_data or not event_data.get("data"):
        return "Invalid event", 400

    attributes = event_data["data"]
    name = attributes.get("name", "unknown")
    size = attributes.get("size", "unknown")
    content_type = attributes.get("contentType", "unknown")

    message = f"Name: {name}, Size: {size}, Format: {content_type}"
    print("Publishing message:", message)
    publisher.publish(topic_path, message.encode("utf-8"))

    return "OK", 200
