import zipfile
import os
from pathlib import Path

def unzip_all_in_directory(zip_directory):
    """
    Unzips all .zip files found in a specified directory,
    extracting each into a new folder with the same name as the zip file.
    """
    zip_directory_path = Path(zip_directory)

    if not zip_directory_path.is_dir():
        print(f"Error: Directory '{zip_directory}' does not exist.")
        return

    for zip_file_path in zip_directory_path.glob("*.zip"):
        try:
            # Create a new directory for extraction based on the zip file's name
            extraction_path = zip_directory_path / zip_file_path.stem
            os.makedirs(extraction_path, exist_ok=True)

            with zipfile.ZipFile(zip_file_path, 'r') as archive:
                archive.extractall(extraction_path)
            print(f"Extracted '{zip_file_path.name}' to '{extraction_path}'.")

        except zipfile.BadZipFile:
            print(f"Error: '{zip_file_path.name}' is not a valid zip file.")
        except Exception as e:
            print(f"An error occurred while processing '{zip_file_path.name}': {e}")

# Example usage:
# Replace 'C:\\Path\\To\\Your\\ZipFiles' with the actual path to your directory of zip files
target_directory = r'C:\\Users\\craven\\OneDrive\\Documents\\itch.io assets'
unzip_all_in_directory(target_directory)