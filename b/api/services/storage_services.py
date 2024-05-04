import os
from google.cloud import storage

dir_path = os.path.dirname(os.path.realpath(__file__))
credentials_path = os.path.join(dir_path, "..", "..", "proyecto-desarrollo-cloud.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath(credentials_path)

BUCKET_NAME = "archivos_desarrollo_cloud"


class StorageService:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(bucket_name)

    def upload_file(self, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        try:
            blob = self.bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_name)
        except Exception as e:
            raise Exception("storage error - " + str(e))
        
    def download_file(self, source_blob_name, destination_file_name):
        """Downloads a blob from the bucket."""
        try:
            blob = self.bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_name)
        except Exception as e:
            raise Exception("storage error - " + str(e))

    def list_files(self):
        """Lists all the blobs in the bucket."""
        try:
            blobs = self.client.list_blobs(self.bucket_name)
            return [blob.name for blob in blobs]
        except Exception as e:
            raise Exception("storage error - " + str(e))

    def delete_file(self, file_name):
        """Deletes a blob from the bucket."""
        try:
            blob = self.bucket.blob(file_name)
            blob.delete()
        except Exception as e:
            raise Exception("storage error - " + str(e))

    def get_file(self, file_name):
        """Gets a blob from the bucket."""
        try:
            blob = self.bucket.blob(file_name)
            return blob
        except Exception as e:
            raise Exception("storage error - " + str(e))
        
    def file_exists(self, file_name):
        """Checks if a blob exists in the bucket."""
        try:
            blob = self.bucket.blob(file_name)
            return blob.exists()
        except Exception as e:
            raise Exception("storage error - " + str(e))

storage_instance = StorageService(BUCKET_NAME)