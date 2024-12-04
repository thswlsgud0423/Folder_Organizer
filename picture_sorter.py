import os
import shutil
from tkinter import Tk, filedialog
from datetime import datetime


def sort_photos_by_date(folder_path):
    """
    Sorts files in the given folder into subfolders based on the date

    Parameters:
        folder_path: path to the folder with photos
    """

    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isdir(file_path):
            continue

        creation_date = os.path.getctime(file_path)
        date_folder_name = datetime.fromtimestamp(creation_date).strftime('%Y-%m-%d')
        date_folder_path = os.path.join(folder_path, date_folder_name)

        if not os.path.exists(date_folder_path):
            os.makedirs(date_folder_path)

        new_file_path = os.path.join(date_folder_path, file_name)
        shutil.move(file_path, new_file_path)
        print(f"Moved: {file_name} --> {date_folder_name}/")
    
    print(f"Complete :> : {folder_path}")


def change_file_name(folder_path):
    
    if not os.path.exists(folder_path):
        print(f"The folder '{folder_path}' does not exist.")
        return
    
    for i, file_name in enumerate(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isdir(file_path):
            continue

        creation_date = os.path.getctime(file_path)
        date_file_name = datetime.fromtimestamp(creation_date).strftime('%Y-%m-%d')

        file_extension = os.path.splitext(file_name)[1]
        
        # Create the new filename
        new_name = f"{date_file_name}_{i}{file_extension}"
        new_file_path = os.path.join(folder_path, new_name)
        
        os.rename(file_path, new_file_path)
        print(f"Name Changed: {file_name} --> {new_name}")

def tagging_image(self):
    pass

def main():
    Tk().withdraw()
    folder_path = filedialog.askdirectory(title="Select your folder")
    
    if folder_path:
        print(f"Selected folder: {folder_path}")
        #sort_photos_by_date(folder_path)
        change_file_name(folder_path)
    else:
        print("No folder selected. Exiting.")

if __name__ == "__main__":
    main()