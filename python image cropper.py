# # # # import tkinter as tk
# # # # from tkinter import filedialog
# # # # from PIL import Image, ImageTk

# # # # class ImageCropperApp:
# # # #     def __init__(self, root):
# # # #         self.root = root
# # # #         self.root.title("Square Image Cropper")
# # # #         self.canvas = tk.Canvas(root, cursor="cross")
# # # #         self.canvas.pack(fill="both", expand=True)

# # # #         self.image = None
# # # #         self.tk_img = None
# # # #         self.start_x = self.start_y = self.rect = None

# # # #         self.setup_menu()
# # # #         self.canvas.bind("<ButtonPress-1>", self.on_click)
# # # #         self.canvas.bind("<B1-Motion>", self.on_drag)
# # # #         self.canvas.bind("<ButtonRelease-1>", self.on_release)

# # # #     def setup_menu(self):
# # # #         menubar = tk.Menu(self.root)
# # # #         file_menu = tk.Menu(menubar, tearoff=0)
# # # #         file_menu.add_command(label="Open Image", command=self.open_image)
# # # #         file_menu.add_command(label="Save Crop", command=self.save_crop)
# # # #         menubar.add_cascade(label="File", menu=file_menu)
# # # #         self.root.config(menu=menubar)

# # # #     def open_image(self):
# # # #         file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg")])
# # # #         if not file_path:
# # # #             return
# # # #         self.image = Image.open(file_path).convert("RGB")
# # # #         self.display_image()

# # # #     def display_image(self):
# # # #         self.tk_img = ImageTk.PhotoImage(self.image)
# # # #         self.canvas.delete("all")
# # # #         self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
# # # #         self.canvas.config(width=self.tk_img.width(), height=self.tk_img.height())
# # # #         self.rect = None

# # # #     def on_click(self, event):
# # # #         self.start_x = event.x
# # # #         self.start_y = event.y
# # # #         self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

# # # #     def on_drag(self, event):
# # # #         if self.rect:
# # # #             end_x = event.x
# # # #             end_y = event.y
# # # #             size = min(abs(end_x - self.start_x), abs(end_y - self.start_y))
# # # #             end_x = self.start_x + size if end_x >= self.start_x else self.start_x - size
# # # #             end_y = self.start_y + size if end_y >= self.start_y else self.start_y - size
# # # #             self.canvas.coords(self.rect, self.start_x, self.start_y, end_x, end_y)

# # # #     def on_release(self, event):
# # # #         pass  # We don't need to do anything here for now

# # # #     def save_crop(self):
# # # #         if not self.rect or not self.image:
# # # #             return

# # # #         x1, y1, x2, y2 = [int(c) for c in self.canvas.coords(self.rect)]
# # # #         x1, x2 = sorted((x1, x2))
# # # #         y1, y2 = sorted((y1, y2))

# # # #         cropped = self.image.crop((x1, y1, x2, y2)).resize((700, 700), Image.LANCZOS)
# # # #         save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg")])
# # # #         if save_path:
# # # #             cropped.save(save_path)
# # # #             print(f"Saved cropped image to: {save_path}")

# # # # if __name__ == "__main__":
# # # #     root = tk.Tk()
# # # #     app = ImageCropperApp(root)
# # # #     root.mainloop()

# # # import tkinter as tk
# # # from tkinter import filedialog
# # # from PIL import Image, ImageTk

# # # class ImageCropperApp:
# # #     def __init__(self, root):
# # #         self.root = root
# # #         self.root.title("Square Image Cropper")
# # #         self.canvas = tk.Canvas(root, cursor="cross")
# # #         self.canvas.pack(fill="both", expand=True)

# # #         self.image = None
# # #         self.tk_img = None
# # #         self.start_x = self.start_y = self.rect = None

# # #         self.setup_menu()
# # #         self.canvas.bind("<ButtonPress-1>", self.on_click)
# # #         self.canvas.bind("<B1-Motion>", self.on_drag)
# # #         self.canvas.bind("<ButtonRelease-1>", self.on_release)

# # #     def setup_menu(self):
# # #         menubar = tk.Menu(self.root)
# # #         file_menu = tk.Menu(menubar, tearoff=0)
# # #         file_menu.add_command(label="Open Image", command=self.open_image)
# # #         file_menu.add_command(label="Save Crop", command=self.save_crop)
# # #         menubar.add_cascade(label="File", menu=file_menu)
# # #         self.root.config(menu=menubar)

# # #     def open_image(self):
# # #         file_path = filedialog.askopenfilename(filetypes=[
# # #             ("PNG files", "*.png"),
# # #             ("JPG files", "*.jpg"),
# # #             ("JPEG files", "*.jpeg"),
# # #             ("All files", "*.*")
# # #         ])
# # #         if not file_path:
# # #             return
# # #         self.image = Image.open(file_path).convert("RGB")
# # #         self.display_image()

# # #     def display_image(self):
# # #         self.tk_img = ImageTk.PhotoImage(self.image)
# # #         self.canvas.delete("all")
# # #         self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
# # #         self.canvas.config(width=self.tk_img.width(), height=self.tk_img.height())
# # #         self.rect = None

# # #     def on_click(self, event):
# # #         self.start_x = event.x
# # #         self.start_y = event.y
# # #         self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

# # #     def on_drag(self, event):
# # #         if self.rect:
# # #             end_x = event.x
# # #             end_y = event.y
# # #             size = min(abs(end_x - self.start_x), abs(end_y - self.start_y))
# # #             end_x = self.start_x + size if end_x >= self.start_x else self.start_x - size
# # #             end_y = self.start_y + size if end_y >= self.start_y else self.start_y - size
# # #             self.canvas.coords(self.rect, self.start_x, self.start_y, end_x, end_y)

# # #     def on_release(self, event):
# # #         pass

# # #     def save_crop(self):
# # #         if not self.rect or not self.image:
# # #             return

# # #         x1, y1, x2, y2 = [int(c) for c in self.canvas.coords(self.rect)]
# # #         x1, x2 = sorted((x1, x2))
# # #         y1, y2 = sorted((y1, y2))

# # #         cropped = self.image.crop((x1, y1, x2, y2)).resize((700, 700), Image.LANCZOS)
# # #         save_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("All Files", "*.*")])
# # #         if save_path:
# # #             cropped.save(save_path)
# # #             print(f"Saved cropped image to: {save_path}")

# # # if __name__ == "__main__":
# # #     root = tk.Tk()
# # #     app = ImageCropperApp(root)
# # #     root.mainloop()


# # import tkinter as tk
# # from tkinter import filedialog
# # from PIL import Image, ImageTk
# # import os

# # class ImageCropperApp:
# #     def __init__(self, root):
# #         self.root = root
# #         self.root.title("Square Image Cropper")

# #         self.canvas_size = 900
# #         self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="gray", cursor="cross")
# #         self.canvas.pack()

# #         self.image = None
# #         self.tk_img = None
# #         self.displayed_img = None
# #         self.scale_ratio = 1

# #         self.start_x = self.start_y = self.rect = None

# #         self.setup_menu()
# #         self.bind_events()

# #         # Output directory
# #         self.output_dir = "cropped_output"
# #         os.makedirs(self.output_dir, exist_ok=True)

# #     def setup_menu(self):
# #         menubar = tk.Menu(self.root)
# #         file_menu = tk.Menu(menubar, tearoff=0)
# #         file_menu.add_command(label="Open Image", command=self.open_image)
# #         menubar.add_cascade(label="File", menu=file_menu)
# #         self.root.config(menu=menubar)

# #     def bind_events(self):
# #         self.canvas.bind("<ButtonPress-1>", self.on_click)
# #         self.canvas.bind("<B1-Motion>", self.on_drag)
# #         self.root.bind("<Return>", self.save_crop)

# #     def open_image(self):
# #         file_path = filedialog.askopenfilename(filetypes=[
# #             ("Image files", "*.png *.jpg *.jpeg"),
# #             ("All files", "*.*")
# #         ])
# #         if not file_path:
# #             return

# #         self.image = Image.open(file_path).convert("RGB")
# #         self.original_image_path = file_path
# #         self.prepare_display_image()

# #     def prepare_display_image(self):
# #         img = self.image.copy()
# #         img.thumbnail((self.canvas_size, self.canvas_size), Image.LANCZOS)
# #         self.displayed_img = img
# #         self.scale_ratio = self.image.width / img.width

# #         self.tk_img = ImageTk.PhotoImage(img)
# #         self.canvas.delete("all")
# #         self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
# #         self.rect = None

# #     def on_click(self, event):
# #         self.start_x = event.x
# #         self.start_y = event.y
# #         self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

# #     def on_drag(self, event):
# #         if self.rect:
# #             size = min(abs(event.x - self.start_x), abs(event.y - self.start_y))
# #             end_x = self.start_x + size if event.x >= self.start_x else self.start_x - size
# #             end_y = self.start_y + size if event.y >= self.start_y else self.start_y - size
# #             self.canvas.coords(self.rect, self.start_x, self.start_y, end_x, end_y)

# #     def save_crop(self, event=None):
# #         if not self.rect or not self.image:
# #             print("No crop area selected.")
# #             return

# #         x1, y1, x2, y2 = [int(c) for c in self.canvas.coords(self.rect)]
# #         x1, x2 = sorted((x1, x2))
# #         y1, y2 = sorted((y1, y2))

# #         # Convert to original image coordinates
# #         x1_orig = int(x1 * self.scale_ratio)
# #         y1_orig = int(y1 * self.scale_ratio)
# #         x2_orig = int(x2 * self.scale_ratio)
# #         y2_orig = int(y2 * self.scale_ratio)

# #         cropped = self.image.crop((x1_orig, y1_orig, x2_orig, y2_orig)).resize((700, 700), Image.LANCZOS)

# #         # Save using original file name
# #         filename = os.path.basename(self.original_image_path)
# #         name, _ = os.path.splitext(filename)
# #         output_path = os.path.join(self.output_dir, f"{name}_cropped.jpg")
# #         cropped.save(output_path)
# #         print(f"Saved cropped image to: {output_path}")

# # if __name__ == "__main__":
# #     root = tk.Tk()
# #     app = ImageCropperApp(root)
# #     root.mainloop()

# import tkinter as tk
# from tkinter import filedialog
# from PIL import Image, ImageTk
# import cv2
# import os

# class SmartCropper:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Smart Face Cropper")

#         self.canvas_size = 900
#         self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="gray", cursor="cross")
#         self.canvas.pack()

#         self.image_files = []
#         self.current_index = 0
#         self.image = None
#         self.tk_img = None
#         self.displayed_img = None
#         self.original_image_path = ""
#         self.rect = None
#         self.scale_ratio = 1

#         self.start_x = self.start_y = None
#         self.rect_override = False

#         self.output_dir = "cropped_output"
#         os.makedirs(self.output_dir, exist_ok=True)

#         self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#         self.setup_menu()
#         self.bind_events()

#     def setup_menu(self):
#         menubar = tk.Menu(self.root)
#         file_menu = tk.Menu(menubar, tearoff=0)
#         file_menu.add_command(label="Open Folder", command=self.open_folder)
#         menubar.add_cascade(label="File", menu=file_menu)
#         self.root.config(menu=menubar)

#     def bind_events(self):
#         self.canvas.bind("<ButtonPress-1>", self.on_click)
#         self.canvas.bind("<B1-Motion>", self.on_drag)
#         self.root.bind("<Return>", self.save_and_next)

#     def open_folder(self):
#         folder_path = filedialog.askdirectory()
#         if not folder_path:
#             return
#         self.image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
#                             if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
#         self.image_files.sort()
#         self.current_index = 0
#         self.load_image()

#     def load_image(self):
#         if self.current_index >= len(self.image_files):
#             print("All images processed.")
#             self.canvas.delete("all")
#             return

#         file_path = self.image_files[self.current_index]
#         self.image = Image.open(file_path).convert("RGB")
#         self.original_image_path = file_path
#         self.prepare_display_image()

#     def prepare_display_image(self):
#         img = self.image.copy()
#         img.thumbnail((self.canvas_size, self.canvas_size), Image.LANCZOS)
#         self.displayed_img = img
#         self.scale_ratio = self.image.width / img.width

#         self.tk_img = ImageTk.PhotoImage(img)
#         self.canvas.delete("all")
#         self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
#         self.rect = None
#         self.rect_override = False
#         self.auto_crop_face()

#     def auto_crop_face(self):
#         # Convert to OpenCV format
#         img_cv = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
#         faces = self.face_cascade.detectMultiScale(img_cv, scaleFactor=1.1, minNeighbors=5)

#         if len(faces) == 0:
#             print("No face detected.")
#             return

#         (x, y, w, h) = faces[0]
#         size = max(w, h) * 2
#         center_x = x + w // 2
#         center_y = y + h // 2
#         half = size // 2

#         left = max(center_x - half, 0)
#         top = max(center_y - half, 0)
#         right = min(center_x + half, self.image.width)
#         bottom = min(center_y + half, self.image.height)

#         # scale to canvas
#         x1 = int(left / self.scale_ratio)
#         y1 = int(top / self.scale_ratio)
#         x2 = int(right / self.scale_ratio)
#         y2 = int(bottom / self.scale_ratio)

#         size = min(x2 - x1, y2 - y1)
#         x2 = x1 + size
#         y2 = y1 + size

#         self.rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)

#     def on_click(self, event):
#         self.start_x = event.x
#         self.start_y = event.y
#         if self.rect:
#             self.canvas.delete(self.rect)
#         self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="blue", width=2)
#         self.rect_override = True

#     def on_drag(self, event):
#         if self.rect:
#             size = min(abs(event.x - self.start_x), abs(event.y - self.start_y))
#             end_x = self.start_x + size if event.x >= self.start_x else self.start_x - size
#             end_y = self.start_y + size if event.y >= self.start_y else self.start_y - size
#             self.canvas.coords(self.rect, self.start_x, self.start_y, end_x, end_y)

#     def save_and_next(self, event=None):
#         if not self.rect or not self.image:
#             return

#         x1, y1, x2, y2 = [int(c) for c in self.canvas.coords(self.rect)]
#         x1, x2 = sorted((x1, x2))
#         y1, y2 = sorted((y1, y2))

#         # Convert to original scale
#         x1_orig = int(x1 * self.scale_ratio)
#         y1_orig = int(y1 * self.scale_ratio)
#         x2_orig = int(x2 * self.scale_ratio)
#         y2_orig = int(y2 * self.scale_ratio)

#         cropped = self.image.crop((x1_orig, y1_orig, x2_orig, y2_orig)).resize((700, 700), Image.LANCZOS)

#         # Save
#         filename = os.path.basename(self.original_image_path)
#         name, _ = os.path.splitext(filename)
#         output_path = os.path.join(self.output_dir, f"{name}_cropped.jpg")
#         cropped.save(output_path)
#         print(f"Saved: {output_path}")

#         # Load next
#         self.current_index += 1
#         self.load_image()


# # Required import for OpenCV face detection
# import numpy as np

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = SmartCropper(root)
#     root.mainloop()


import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import os
import numpy as np

class SmartCropper:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Face Cropper")

        self.canvas_size = 900
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="gray", cursor="cross")
        self.canvas.pack()

        self.image_files = []
        self.current_index = 0
        self.image = None
        self.tk_img = None
        self.displayed_img = None
        self.original_image_path = ""
        self.rect = None
        self.scale_ratio = 1

        self.start_x = self.start_y = None
        self.rect_override = False
        self.output_dir = "cropped_output"
        os.makedirs(self.output_dir, exist_ok=True)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.setup_menu()
        self.setup_buttons()
        self.bind_events()

    def setup_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Folder", command=self.open_folder)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

    def setup_buttons(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=5)
        self.back_button = tk.Button(btn_frame, text="Back", command=self.go_back)
        self.back_button.pack(side="left")

    def bind_events(self):
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<Return>", self.save_and_next)
        self.root.bind("<Left>", lambda e: self.move_rect(-5, 0))
        self.root.bind("<Right>", lambda e: self.move_rect(5, 0))
        self.root.bind("<Up>", lambda e: self.move_rect(0, -5))
        self.root.bind("<Down>", lambda e: self.move_rect(0, 5))

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return

        all_files = sorted(f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png')))
        self.image_files = []
        for f in all_files:
            name, _ = os.path.splitext(f)
            if not os.path.exists(os.path.join(self.output_dir, f"{name}_cropped.jpg")):
                self.image_files.append(os.path.join(folder_path, f))

        self.current_index = 0
        self.load_image()

    def load_image(self):
        if self.current_index >= len(self.image_files):
            print("All images processed.")
            self.canvas.delete("all")
            return

        file_path = self.image_files[self.current_index]
        self.image = Image.open(file_path).convert("RGB")
        self.original_image_path = file_path
        self.prepare_display_image()

    def prepare_display_image(self):
        img = self.image.copy()
        img.thumbnail((self.canvas_size, self.canvas_size), Image.LANCZOS)
        self.displayed_img = img
        self.scale_ratio = self.image.width / img.width

        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)
        self.rect = None
        self.rect_override = False
        self.auto_crop_face()

    def auto_crop_face(self):
        img_cv = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
        faces = self.face_cascade.detectMultiScale(img_cv, scaleFactor=1.1, minNeighbors=5)

        if len(faces) == 0:
            print("No face detected.")
            return

        (x, y, w, h) = faces[0]
        size = max(w, h) * 2
        center_x = x + w // 2
        center_y = y + h // 2
        half = size // 2

        left = max(center_x - half, 0)
        top = max(center_y - half, 0)
        right = min(center_x + half, self.image.width)
        bottom = min(center_y + half, self.image.height)

        x1 = int(left / self.scale_ratio)
        y1 = int(top / self.scale_ratio)
        x2 = int(right / self.scale_ratio)
        y2 = int(bottom / self.scale_ratio)

        size = min(x2 - x1, y2 - y1)
        x2 = x1 + size
        y2 = y1 + size

        self.rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2)

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="blue", width=2)
        self.rect_override = True

    def on_drag(self, event):
        if self.rect:
            size = min(abs(event.x - self.start_x), abs(event.y - self.start_y))
            end_x = self.start_x + size if event.x >= self.start_x else self.start_x - size
            end_y = self.start_y + size if event.y >= self.start_y else self.start_y - size
            self.canvas.coords(self.rect, self.start_x, self.start_y, end_x, end_y)

    def move_rect(self, dx, dy):
        if self.rect:
            coords = self.canvas.coords(self.rect)
            new_coords = [coords[0]+dx, coords[1]+dy, coords[2]+dx, coords[3]+dy]
            self.canvas.coords(self.rect, *new_coords)

    def save_and_next(self, event=None):
        if not self.rect or not self.image:
            return

        x1, y1, x2, y2 = [int(c) for c in self.canvas.coords(self.rect)]
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))

        x1_orig = int(x1 * self.scale_ratio)
        y1_orig = int(y1 * self.scale_ratio)
        x2_orig = int(x2 * self.scale_ratio)
        y2_orig = int(y2 * self.scale_ratio)

        cropped = self.image.crop((x1_orig, y1_orig, x2_orig, y2_orig)).resize((700, 700), Image.LANCZOS)
        filename = os.path.basename(self.original_image_path)
        name, _ = os.path.splitext(filename)
        output_path = os.path.join(self.output_dir, f"{name}_cropped.jpg")
        cropped.save(output_path)
        print(f"Saved: {output_path}")

        self.current_index += 1
        self.load_image()

    def go_back(self):
        if self.current_index > 0:
            self.current_index -= 1
            filename = os.path.basename(self.image_files[self.current_index])
            name, _ = os.path.splitext(filename)
            output_path = os.path.join(self.output_dir, f"{name}_cropped.jpg")
            if os.path.exists(output_path):
                os.remove(output_path)
                print(f"Removed: {output_path}")
            self.load_image()

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCropper(root)
    root.mainloop()
