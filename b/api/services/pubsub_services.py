import json
from google.cloud import pubsub_v1

PROJECT_ID = "e2-dsc"
TOPIC_ID = "pubsub"
SUBSCRIPTION_ID = "pubsub-sub"

publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)


def publish_message(user_id: str, temp_file: str, task: dict) -> str:
    """Publish a message to Pub/Sub"""
    message_data = {
        "user_id": user_id,
        "temp_file": temp_file,
        "task": task
    }
    data = json.dumps(message_data).encode("utf-8")
    future = publisher.publish(topic_path, data)
    message_id = future.result()
    return message_id


def get_task_status_from_pubsub(message_id: str) -> str:
    """Retrieve task status based on Pub/Sub message (mockup example)"""
    try:
        response = subscriber.get_snapshot(name=subscription_path)
        messages = response.snapshot.topic_stats.messages
        for msg in messages:
            if msg.message_id == message_id:
                message_data = json.loads(msg.data)
                return message_data.get("task", {}).get("status", "unknown")
    except Exception:
        return "unknown"

    return "unknown"
