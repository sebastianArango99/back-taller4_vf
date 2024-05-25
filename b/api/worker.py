import os
import subprocess
from google.cloud import pubsub_v1
import json
import sys

sys.path.append('/code')
# Services
from api.services.storage_services import storage_instance

# Constants
from api.constants.server_constants import TEMP_DIR

# Initialize Pub/Sub client
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

# Define Pub/Sub topic and subscription names
TOPIC_NAME = "pubsub"
PROJECT_ID = "proyecto-desarrollo-cloud"
SUBSCRIPTION_NAME = "ejemplo123-sub"
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_NAME)


def publish_task(task_data):
    """Publish a task to Pub/Sub"""
    data = json.dumps(task_data).encode("utf-8")
    future = publisher.publish(topic_path, data=data)
    print(f"Published message ID: {future.result()}")


def process_message(message):
    """Callback function to process incoming Pub/Sub messages"""
    try:
        task_data = json.loads(message.data.decode("utf-8"))
        convert_file(task_data["user_id"], task_data["temp_file"], task_data["task"])
        message.ack()
    except Exception as e:
        print(f"Failed to process message: {e}")
        message.nack()


def convert_file(user_id, original_temp_file, task):
    """Converts a file to the specified extension and uploads it to GCS"""
    # Ensure the temp directory exists
    os.makedirs(TEMP_DIR, exist_ok=True)

    out_filepath = original_temp_file.rsplit(".", 1)[0]
    converted_temp_file = out_filepath + "." + task["new_extension"]
    print(f"Converting {original_temp_file} to {converted_temp_file}")

    # Conversion command
    cmd = [
        "libreoffice",
        "--headless",
        "--convert-to",
        task["new_extension"],
        "--outdir",
        TEMP_DIR,
        original_temp_file,
    ]

    try:
        # Run conversion
        subprocess.run(cmd, check=True, capture_output=True)
        try:
            # Define the destination file name in GCS
            new_filename = task["filename"] + "." + task["new_extension"]
            blob_name = os.path.join(user_id, new_filename)

            # Upload the converted file to GCS
            storage_instance.upload_file(converted_temp_file, blob_name)

            # Clean up local temporary files
            os.remove(converted_temp_file)
            os.remove(original_temp_file)

            print(f"File converted and uploaded to GCS as {blob_name}")

            # Update Pub/Sub message with the new status
            task["status"] = "processed"
            task["converted_file"] = blob_name
            publish_task({"user_id": user_id, "task": task})
        except Exception as e:
            if os.path.exists(converted_temp_file):
                os.remove(converted_temp_file)
            if os.path.exists(original_temp_file):
                os.remove(original_temp_file)
            print(f"Error uploading file: {e}")
    except subprocess.CalledProcessError as e:
        print(f"Subprocess error: {e}")


def worker():
    """Initialize Pub/Sub worker for message processing"""
    flow_control = pubsub_v1.types.FlowControl(max_messages=1)
    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=process_message, flow_control=flow_control
    )
    print(f"Listening for messages on {subscription_path}")

    with subscriber:
        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()
            streaming_pull_future.result()


if __name__ == "__main__":
    worker()
