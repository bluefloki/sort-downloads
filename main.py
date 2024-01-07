import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
import sys

destination_directories = [
    {
        "name": "Images",
        "filetypes": [
            "jpg",
            "png",
            "gif",
            "bmp",
            "tiff",
            "jpeg",
            "raw",
            "nef",
            "cr2",
            "dng",
        ],
    },
    {
        "name": "Documents",
        "filetypes": [
            "docx",
            "pdf",
            "txt",
            "pptx",
            "xlsx",
            "csv",
            "xls",
            "xlsx",
            "ods",
        ],
    },
    {"name": "Videos", "filetypes": ["mp4", "avi", "mkv", "mov", "wmv"]},
    {"name": "Audio", "filetypes": ["mp3", "wav", "flac", "aac", "ogg"]},
    {"name": "Archives", "filetypes": ["zip", "tar", "gz", "7z", "rar"]},
]


# make sure the script doesn't run in ~ directory
def set_working_directory():
    if getattr(sys, "frozen", False):
        script_dir = os.path.dirname(sys.executable)
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))

    os.chdir(script_dir)


# Call the function to set the working directory
set_working_directory()


class Watcher:
    source_path = os.getcwd()

    def __init__(self):
        self.observer = Observer()

    def run(self):
        print("folder-sorter is working...")

        # create directories
        for d in destination_directories:
            if not os.path.exists(d["name"]):
                os.mkdir(d["name"])
                print(f"Directory {d['name']} created.")

        # move existing files
        files_in_directory = [
            f
            for f in os.listdir(self.source_path)
            if os.path.isfile(os.path.join(self.source_path, f))
        ]
        if files_in_directory:
            for file_name in files_in_directory:
                file_path = os.path.join(self.source_path, file_name)
                move_file(file_path)

        # move incoming files
        event_handler = Handler()
        self.observer.schedule(event_handler, self.source_path, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        elif event.event_type == "created":
            move_file(event.src_path)


def get_file_ext(f):
    return f.split(".")[-1]


def move_file(source_path):
    filename = os.path.basename(source_path)
    file_ext = get_file_ext(filename)
    misc_file = False
    destination_directory = ""

    # figure out the appropriate directory to move the file
    if not misc_file:
        for d in destination_directories:
            if file_ext in d["filetypes"]:
                destination_directory = d["name"]
                break
            else:
                misc_file = True
                return
        destination_path = os.path.join(destination_directory, filename)

        # if a file with the same name already exists
        if os.path.exists(destination_path):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(
                os.path.join(destination_directory, f"{base} ({counter}){ext}")
            ):
                counter += 1

            # Create the unique filename
            filename = f"{base} ({counter}){ext}"
            destination_path = os.path.join(destination_directory, filename)

        # move the file
        shutil.move(source_path, destination_path)
        print(f"Moved {filename} to {destination_path.split('/')[0]} Directory.")


if __name__ == "__main__":
    w = Watcher()
    w.run()
