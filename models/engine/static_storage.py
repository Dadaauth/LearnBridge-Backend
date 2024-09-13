import os
import subprocess
from uuid import uuid4


UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
DASH_OUTPUT_FOLDER = os.getenv("DASH_OUTPUT_FOLDER")

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DASH_OUTPUT_FOLDER, exist_ok=True)


class StaticStorage():
    """
    """

    def __init__(self, file, filename=None):
        self.file = file
        ext = file.filename.split(".", -1)[-1]
        self.filename = f"{str(uuid4())}.{ext}" if not filename else filename

    def retrieve(self):
        pass

    def save(self):
        """
            Save the file to the static
            storage engine and return
            the necessary metadata

            :return
                The necessary metadata
        """
        """Save the file to a local storage
        before uploading to a remote location"""
        self.file.save(os.path.join(UPLOAD_FOLDER, self.filename))
        return self.filename


class VideoStorage(StaticStorage):
    """
    """

    def __init__(self, file, filename=None):
        super().__init__(file, filename)

    def save(self):
        super().save()
        # Set up a job to convert to dash
        # Job should be independent of the request

        # Try using asyncio as a placeholder
        # for jobs scheduling
        self.convert_to_dash()
        return self.filename

    def convert_to_dash(self):
        output_folder = DASH_OUTPUT_FOLDER + self.filename.rsplit('.', 1)[0]
        os.makedirs(output_folder, exist_ok=True)

        output_mpd = output_folder + f"/{self.filename.rsplit('.', 1)[0]}.mpd"

        command = [
            'ffmpeg', '-i', os.path.join(UPLOAD_FOLDER, self.filename),
            '-map', '0:v', '-map', '0:a',
            '-b:v', '1000k', '-b:a', '128k',
            '-f', 'dash', output_mpd,
        ]

        subprocess.run(command, check=True)
