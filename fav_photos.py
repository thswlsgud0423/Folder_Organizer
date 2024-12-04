import os
import shutil
from tkinter import Tk, Canvas, filedialog, Button, simpledialog
from PIL import Image, ImageTk


class PhotoViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Viewer")

        # Get the screen dimensions and set the window size as a fraction of it
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.root.geometry(f"{window_width}x{window_height}")

        self.photos = []
        self.current_index = 0
        self.rotation_angle = 0  # Track the current rotation angle of the image
        self.zoom_scale = 0.7
        self.selected_photos = []  # To store the user's favorited photos

        # Create a canvas for displaying the image
        self.canvas = Canvas(self.root, bg="black")
        self.canvas.pack(fill="both", expand=True)

        # Load photos initially
        self.load_photos()

        self.root.bind("<MouseWheel>", self.zoom)
        # Create transparent rotation and favorite/save buttons
        self.create_overlay_buttons()

    def load_photos(self):
        folder_path = filedialog.askdirectory(title="Select a folder with photos")
        if folder_path:
            # Collect all image files in the selected folder
            self.photos = [
                os.path.join(folder_path, f) for f in os.listdir(folder_path)
                if f.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif'))
            ]

            if self.photos:
                self.current_index = 0
                self.show_photo()
            else:
                print("No photos found in the selected folder.")
        else:
            print("No folder selected.")

    def show_photo(self):
        if not self.photos:
            return

        photo_path = self.photos[self.current_index]
        image = Image.open(photo_path)

        # Apply the current rotation angle
        self.current_image = image.rotate(self.rotation_angle, expand=True)

        # Scale the image to fit the canvas while maintaining aspect ratio
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        img_width, img_height = self.current_image.size
        scale_factor = min(canvas_width / img_width, canvas_height / img_height)
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)

        resized_image = self.current_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Display the image
        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width // 2, canvas_height // 2, image=self.tk_image, anchor="center")

        self.create_overlay_buttons()


    def create_overlay_buttons(self):
        # Transparent "Rotate Left" button
        self.rotate_left_button = Button(
            self.root,
            text="⟲",  # Unicode for a counterclockwise arrow
            font=("Arial", 24, "bold"),
            fg="white",
            bg="black",
            activebackground="gray",
            activeforeground="white",
            borderwidth=0,
            command=self.rotate_left
        )
        self.rotate_left_button.place(relx=0.1, rely=0.05, anchor="center")  # Adjust position (10% width, 5% height)

        # Transparent "Rotate Right" button
        self.rotate_right_button = Button(
            self.root,
            text="⟳",  # Unicode for a clockwise arrow
            font=("Arial", 24, "bold"),
            fg="white",
            bg="black",
            activebackground="gray",
            activeforeground="white",
            borderwidth=0,
            command=self.rotate_right
        )
        self.rotate_right_button.place(relx=0.9, rely=0.05, anchor="center")  # Adjust position (90% width, 5% height)

        # Transparent "Favorite Photo" button
        self.favorite_button = Button(
            self.root,
            text="❤",  # Unicode heart symbol
            font=("Arial", 18, "bold"),
            fg="red",
            bg="black",
            activebackground="gray",
            activeforeground="red",
            borderwidth=0,
            command=self.favorite_photo
        )
        self.favorite_button.place(relx=0.5, rely=0.05, anchor="center")  # Center at top (50% width, 5% height)

        # Transparent "Save Selected" button
        self.save_button = Button(
            self.root,
            text="Save Selected",
            font=("Arial", 12),
            fg="white",
            bg="black",
            activebackground="gray",
            activeforeground="white",
            borderwidth=0,
            command=self.save_selected_photos
        )
        self.save_button.place(relx=0.5, rely=0.95, anchor="center")  # Center at bottom (50% width, 95% height)
        
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        # Add semi-transparent left arrow
        left_arrow_x = 50
        self.canvas.create_polygon(
            [left_arrow_x, canvas_height // 2,
             left_arrow_x + 40, canvas_height // 2 - 30,
             left_arrow_x + 40, canvas_height // 2 + 30],
            fill="white", outline="", tags="navigation", stipple="gray50"
        )
        self.canvas.tag_bind("navigation", "<Button-1>", lambda event: self.show_previous())

        # Add semi-transparent right arrow
        right_arrow_x = canvas_width - 50
        self.canvas.create_polygon(
            [right_arrow_x, canvas_height // 2,
             right_arrow_x - 40, canvas_height // 2 - 30,
             right_arrow_x - 40, canvas_height // 2 + 30],
            fill="white", outline="", tags="navigation", stipple="gray50"
        )
        self.canvas.tag_bind("navigation", "<Button-1>", lambda event: self.show_next())


    def favorite_photo(self):
        if not self.photos:
            return
        selected_photo = self.photos[self.current_index]
        if selected_photo not in self.selected_photos:
            self.selected_photos.append(selected_photo)
            print(f"Favorited: {os.path.basename(selected_photo)}")
        else:
            print(f"Photo already favorited: {os.path.basename(selected_photo)}")

    def save_selected_photos(self):
        if not self.selected_photos:
            print("No photos selected")
            return

        # Ask user for the folder name to save the selected photos using simpledialog
        folder_name = simpledialog.askstring("Folder Name", "Enter a name for the folder:")
        if not folder_name:
            return

        # Create the new folder
        save_folder = os.path.join(os.path.dirname(self.photos[0]), folder_name)
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        # Copy selected photos to the new folder
        for photo in self.selected_photos:
            shutil.copy(photo, save_folder)

        print(f"Saved {len(self.selected_photos)} photos to {save_folder}")
        self.selected_photos.clear()  # Clear the selected photos after saving

    def rotate_left(self):
        self.rotation_angle = (self.rotation_angle + 90) % 360
        self.show_photo()

    def rotate_right(self):
        self.rotation_angle = (self.rotation_angle - 90) % 360
        self.show_photo()

    def show_next(self):
        if self.photos:
            self.current_index = (self.current_index + 1) % len(self.photos)
            self.show_photo()

    def show_previous(self):
        if self.photos:
            self.current_index = (self.current_index - 1) % len(self.photos)
            self.show_photo()

    def zoom(self, event):
        if event.delta > 0 or event.num == 4:  # Zoom in
            self.zoom_scale *= 1.1
        elif event.delta < 0 or event.num == 5:  # Zoom out
            self.zoom_scale /= 1.1

        # Limit the zoom scale to avoid extreme zoom levels
        self.zoom_scale = max(0.1, min(self.zoom_scale, 10))

        # Update the image display with the new zoom scale
        self.show_photo()

if __name__ == "__main__":
    root = Tk()
    app = PhotoViewer(root)
    root.mainloop()
