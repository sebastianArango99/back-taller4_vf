import os
from fastapi import UploadFile

# Constants
from api.constants.server_constants import TEMP_DIR


async def create_temporal_file(user_id: str, file: UploadFile):
    # Create directory if it doesn't exist
    os.makedirs(TEMP_DIR, exist_ok=True)

    # Define the path of the temporary file
    temp_file = os.path.join(TEMP_DIR, user_id + "-" + file.filename)

    # Save the file in the temporary directory
    with open(temp_file, "wb+") as f:
        f.write(await file.read())

    # Return the path of the temporary file
    return temp_file