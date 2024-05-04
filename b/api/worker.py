import os
import celery
import subprocess

# Services
from api.services.storage_services import storage_instance

# Constants
from api.constants.server_constants import TEMP_DIR


app = celery.Celery(
    "converter",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)


@app.task
def convert_file(user_id, original_temp_file, task):
    # Ensure this directory exists
    os.makedirs(TEMP_DIR, exist_ok=True)

    out_filepath = original_temp_file.rsplit(".", 1)[0]
    converted_temp_file = out_filepath + "." + task["new_extension"]
    print(f"Converting {original_temp_file} to {converted_temp_file}")

    # Your conversion command here
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
        subprocess.run(cmd, check=True, capture_output=True)
        try:
            # Define your GCS bucket and the destination file name
            new_filename = task["filename"] + "." + task["new_extension"]
            blob_name = os.path.join(user_id, new_filename)

            # Assuming upload_to_gcs is defined to handle the upload
            storage_instance.upload_file(converted_temp_file, blob_name)

            # Clean up the temporary file if no longer needed
            os.remove(converted_temp_file)
            os.remove(original_temp_file)

            return {
                "status": "success",
                "message": f"File converted and uploaded to GCS as {blob_name}",
            }

        except Exception as e:
            # Attempt to clean up local files even in case of failure
            if os.path.exists(converted_temp_file):
                os.remove(converted_temp_file)
            if os.path.exists(original_temp_file):
                os.remove(original_temp_file)
            return {"status": "error", "message": str(e)}

    except subprocess.CalledProcessError as e:
        # Log the error or handle it as per your application's error handling policy
        return {"status": "error", "message": "subprocess error - " + str(e)}
