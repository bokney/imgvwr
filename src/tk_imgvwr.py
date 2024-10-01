
import os
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from pathlib import Path

class IMGVWR:

    def init_images(self, folder_path):
        self.folder_path = folder_path
        self.images = [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))
            ]
        self.image_index = 0

    def __init__(self, root: tk.Tk, folder_path: Path = os.getcwd()) -> None:
        self.root = root
        self.init_images(folder_path)

        self.fill_window: bool = False
        self.full_screen: bool = True

        self.load_image()

        self.root.bind("<Left>", self.prev_image)
        self.root.bind("<Right>", self.next_image)
        self.root.bind("<Up>", self.toggle_full_screen)
        self.root.bind("<Down>", self.toggle_fill_window)

    def toggle_fill_window(self, event):
        self.fill_window = not self.fill_window
        self.load_image()

    def toggle_full_screen(self, event):
        self.full_screen = not self.full_screen
        root.attributes('-fullscreen', self.full_screen)
        self.load_image()

    def load_image(self):
        image_path = os.path.join(self.folder_path, self.images[self.image_index])
        image = Image.open(image_path)

        image_width, image_height = image.size

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        if self.fill_window:
            scaling_factor = min(screen_width / image_width, screen_height / image_height)
            width = int(image_width * scaling_factor)
            height = int(image_height * scaling_factor)
            self.root.geometry(f"{width}x{height}")
            image = image.resize((width, height), Image.LANCZOS)
        else:
            width = image_width
            height = image_height
            self.root.geometry(f"{width}x{height}")

        self.tk_image = ImageTk.PhotoImage(image)

        if (hasattr(self, 'image_label')):
            self.image_label.config(image = self.tk_image)
        else:
            self.image_label = ttk.Label(self.root, image = self.tk_image)
    
        self.image_label.pack(expand = True, anchor = 'center')
        self.root.update_idletasks()

    def prev_image(self, event):
        self.image_index = (self.image_index - 1) % len(self.images)
        self.load_image()

    def next_image(self, event):
        self.image_index = (self.image_index + 1) % len(self.images)
        self.load_image()

    def open(self) -> Path:
        folder_path = filedialog.askdirectory(
            title="Select a folder"
        )

        if folder_path:
        
            folder = Path(folder_path)
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif'}
            contains_images = any(file.suffix.lower() in image_extensions for file in folder.iterdir() if file.is_file())

            if contains_images:
                print(f"selected {folder_path}")
                self.init_images(folder_path)
                self.load_image()
            else:
                print(f"Folder {folder_path} contains no images.")


root = tk.Tk()
menu_bar = tk.Menu(root)

str_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/data'
folder_path = Path(str_path)
app = IMGVWR(root, folder_path)

file_menu = tk.Menu(menu_bar, tearoff = 0)
file_menu.add_command(label = "Open", command = app.open)
file_menu.add_separator()
file_menu.add_command(label = "Exit", command = root.quit)
menu_bar.add_cascade(label = "File", menu = file_menu)
root.config(menu = menu_bar)

root.mainloop()
