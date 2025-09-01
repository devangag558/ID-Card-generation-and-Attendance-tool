import os
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import pandas as pd
import platform
import json

class IDCardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SG ID Card Generator")

        if platform.system() == "Windows":
            self.root.state('zoomed')
        else:
            self.root.attributes('-zoomed', True)

        self.root.bind("<Key>", self.on_key_press)

        self.canvas_width = 1122
        self.canvas_height = 1417

        self.template_path = None
        self.csv_path = None
        self.image_folder = None
        self.qr_folder = None
        self.output_folder = None

        self.positions = {
            'photo': [100, 100],
            'qr': [900, 100],
            'name': [300, 1300]
        }
        self.sizes = {
            'photo': 200,
            'qr': 200
        }
        self.font_size = 40
        self.font_color = "#000000"
        self.selected_object = None

        self.current_roll = None
        self.current_name = None

        self.build_ui()

    def build_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=5)

        tk.Button(top_frame, text="Select CSV", command=self.select_csv).grid(row=0, column=0)
        tk.Button(top_frame, text="Photos Folder", command=self.select_image_folder).grid(row=0, column=1)
        tk.Button(top_frame, text="QR Folder", command=self.select_qr_folder).grid(row=0, column=2)
        tk.Button(top_frame, text="Template Image", command=self.select_template).grid(row=0, column=3)
        tk.Button(top_frame, text="Output Folder", command=self.select_output_folder).grid(row=0, column=4)
        tk.Button(top_frame, text="Preview One", command=self.preview_card).grid(row=0, column=5)
        tk.Button(top_frame, text="Generate All", command=self.generate_all).grid(row=0, column=6)
        tk.Button(top_frame, text="Save Config", command=self.save_config).grid(row=0, column=7)
        tk.Button(top_frame, text="Load Config", command=self.load_config).grid(row=0, column=8)

        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg="gray", scrollregion=(0, 0, self.canvas_width, self.canvas_height))
        hbar = tk.Scrollbar(canvas_frame, orient="horizontal", command=self.canvas.xview)
        vbar = tk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        vbar.grid(row=0, column=1, sticky="ns")
        hbar.grid(row=1, column=0, sticky="ew")

        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        tool_frame = tk.Frame(self.root)
        tool_frame.pack(pady=5)

        tk.Label(tool_frame, text="Photo Size").grid(row=0, column=0)
        self.photo_size_var = tk.IntVar(value=self.sizes['photo'])
        tk.Scale(tool_frame, from_=50, to=500, variable=self.photo_size_var,
                 orient="horizontal", command=self.update_sliders).grid(row=0, column=1)

        tk.Label(tool_frame, text="QR Size").grid(row=0, column=2)
        self.qr_size_var = tk.IntVar(value=self.sizes['qr'])
        tk.Scale(tool_frame, from_=50, to=500, variable=self.qr_size_var,
                 orient="horizontal", command=self.update_sliders).grid(row=0, column=3)

        tk.Label(tool_frame, text="Font Size").grid(row=0, column=4)
        self.font_size_var = tk.IntVar(value=self.font_size)
        tk.Scale(tool_frame, from_=10, to=100, variable=self.font_size_var,
                 orient="horizontal", command=self.update_sliders).grid(row=0, column=5)

        tk.Button(tool_frame, text="Font Color", command=self.pick_color).grid(row=0, column=6)

        select_frame = tk.Frame(self.root)
        select_frame.pack(pady=5)

        tk.Label(select_frame, text="Select Object:").grid(row=0, column=0)
        tk.Button(select_frame, text="Photo", command=lambda: self.select_object("photo")).grid(row=0, column=1)
        tk.Button(select_frame, text="QR", command=lambda: self.select_object("qr")).grid(row=0, column=2)
        tk.Button(select_frame, text="Name", command=lambda: self.select_object("name")).grid(row=0, column=3)

        tk.Label(select_frame, text="Move:").grid(row=0, column=4, padx=(20, 5))
        tk.Button(select_frame, text="↑", command=lambda: self.move_selected(0, -5)).grid(row=0, column=5)
        tk.Button(select_frame, text="↓", command=lambda: self.move_selected(0, 5)).grid(row=0, column=6)
        tk.Button(select_frame, text="←", command=lambda: self.move_selected(-5, 0)).grid(row=0, column=7)
        tk.Button(select_frame, text="→", command=lambda: self.move_selected(5, 0)).grid(row=0, column=8)

    def select_csv(self):
        self.csv_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

    def select_image_folder(self):
        self.image_folder = filedialog.askdirectory()

    def select_qr_folder(self):
        self.qr_folder = filedialog.askdirectory()

    def select_template(self):
        self.template_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png")])

    def select_output_folder(self):
        self.output_folder = filedialog.askdirectory()

    def pick_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.font_color = color
            self.refresh_preview()

    def get_font_path(self):
        if platform.system() == "Windows":
            return "arial.ttf"
        return "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    def select_object(self, obj):
        self.selected_object = obj

    def move_selected(self, dx, dy):
        if self.selected_object:
            self.positions[self.selected_object][0] += dx
            self.positions[self.selected_object][1] += dy
            self.refresh_preview()

    def on_key_press(self, event):
        key = event.keysym
        if self.selected_object:
            if key == 'Left':
                self.move_selected(-5, 0)
            elif key == 'Right':
                self.move_selected(5, 0)
            elif key == 'Up':
                self.move_selected(0, -5)
            elif key == 'Down':
                self.move_selected(0, 5)

    def update_sliders(self, _=None):
        self.sizes['photo'] = self.photo_size_var.get()
        self.sizes['qr'] = self.qr_size_var.get()
        self.font_size = self.font_size_var.get()
        self.refresh_preview()

    def refresh_preview(self):
        if self.current_roll and self.current_name:
            self.preview_from_data(self.current_roll, self.current_name)

    def preview_card(self):
        if not all([self.csv_path, self.template_path, self.image_folder, self.qr_folder]):
            messagebox.showerror("Missing", "Select all required files/folders.")
            return
        df = pd.read_csv(self.csv_path)
        row = df.iloc[0]
        self.current_roll = str(row["Roll Number"])
        self.current_name = str(row["Name"])
        self.preview_from_data(self.current_roll, self.current_name)

    # def preview_from_data(self, roll, name):
    #     name=name.upper()
    #     template = Image.open(self.template_path).convert("RGB")
    #     draw = ImageDraw.Draw(template)

    #     photo_path = os.path.join(self.image_folder, f"{roll}_cropped.png")
    #     qr_path = os.path.join(self.qr_folder, f"qr_{roll}.png")

    #     if os.path.exists(photo_path):
    #         photo = Image.open(photo_path).resize((self.sizes['photo'], self.sizes['photo']))
    #         template.paste(photo, tuple(map(int, self.positions['photo'])), mask=photo)

    #     if os.path.exists(qr_path):
    #         qr = Image.open(qr_path).resize((self.sizes['qr'], self.sizes['qr']))
    #         template.paste(qr, tuple(map(int, self.positions['qr'])), qr.convert('RGBA'))

    #     font = ImageFont.truetype(self.get_font_path(), self.font_size)
    #     bbox = draw.textbbox((0, 0), name, font=font)
    #     text_width = bbox[2] - bbox[0]
    #     text_x = int(self.positions['name'][0]) - text_width // 2
    #     text_y = int(self.positions['name'][1])
    #     draw.text((text_x, text_y), name, font=font, fill=self.font_color)

    #     self.preview_img = ImageTk.PhotoImage(template)
    #     self.canvas.delete("all")
    #     self.canvas.create_image(0, 0, anchor="nw", image=self.preview_img)

    def preview_from_data(self, roll, name):
        name = name.upper()
        template = Image.open(self.template_path).convert("RGB")
        draw = ImageDraw.Draw(template)

        photo_path = os.path.join(self.image_folder, f"{roll}_cropped.png")
        qr_path = os.path.join(self.qr_folder, f"qr_{roll}.png")

        if os.path.exists(photo_path):
            photo = Image.open(photo_path).resize((self.sizes['photo'], self.sizes['photo']))
            template.paste(photo, tuple(map(int, self.positions['photo'])), mask=photo)

        if os.path.exists(qr_path):
            qr = Image.open(qr_path).resize((self.sizes['qr'], self.sizes['qr']))
            template.paste(qr, tuple(map(int, self.positions['qr'])), qr.convert('RGBA'))

        font = ImageFont.truetype(self.get_font_path(), self.font_size)
        bbox = draw.textbbox((0, 0), name, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_x = int(self.positions['name'][0]) - text_width // 2
        text_y = int(self.positions['name'][1])

        # Draw text
        draw.text((text_x, text_y), name, font=font, fill=self.font_color)

        # Draw alignment box (bounding box around text)
        rect_start = (text_x, text_y)
        rect_end = (text_x + text_width, text_y + text_height)
        draw.rectangle([rect_start, rect_end], outline="red", width=2)

        self.preview_img = ImageTk.PhotoImage(template)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.preview_img)


    def generate_all(self):
        if not all([self.csv_path, self.template_path, self.image_folder, self.qr_folder, self.output_folder]):
            messagebox.showerror("Missing", "Please select all folders and files.")
            return

        df = pd.read_csv(self.csv_path)
        skipped = []
        generated_images = []

        for _, row in df.iterrows():
            roll = str(row["Roll Number"])
            name = str(row["Name"]).upper()
            photo_path = os.path.join(self.image_folder, f"{roll}_cropped.png")
            qr_path = os.path.join(self.qr_folder, f"qr_{roll}.png")

            if not os.path.exists(photo_path) or not os.path.exists(qr_path):
                skipped.append({'Roll Number': roll, 'Name': name})
                continue

            template = Image.open(self.template_path).convert("RGB")
            draw = ImageDraw.Draw(template)

            photo = Image.open(photo_path).resize((self.sizes['photo'], self.sizes['photo']))
            template.paste(photo, tuple(map(int, self.positions['photo'])), mask=photo)

            qr = Image.open(qr_path).resize((self.sizes['qr'], self.sizes['qr']))
            template.paste(qr, tuple(map(int, self.positions['qr'])), qr.convert('RGBA'))

            font = ImageFont.truetype(self.get_font_path(), self.font_size)
            bbox = draw.textbbox((0, 0), name, font=font)
            text_width = bbox[2] - bbox[0]
            text_x = int(self.positions['name'][0]) - text_width // 2
            text_y = int(self.positions['name'][1])
            draw.text((text_x, text_y), name, font=font, fill=self.font_color)

            out_path = os.path.join(self.output_folder, f"{roll}_id_card.png")
            template.save(out_path)
            generated_images.append(template)

        if skipped:
            pd.DataFrame(skipped).to_csv(os.path.join(self.output_folder, "skipped_records.csv"), index=False)

        # Save to one PDF
        if generated_images:
            pdf_path = os.path.join(self.output_folder, "all_id_cards.pdf")
            generated_images[0].save(
                pdf_path,
                save_all=True,
                append_images=generated_images[1:],
                resolution=100.0
            )

        messagebox.showinfo("Done", f"Generated {len(generated_images)} ID cards.\nSkipped {len(skipped)} records.")


    # def generate_all(self):
    #     if not all([self.csv_path, self.template_path, self.image_folder, self.qr_folder, self.output_folder]):
    #         messagebox.showerror("Missing", "Please select all folders and files.")
    #         return

    #     df = pd.read_csv(self.csv_path)
    #     skipped = []

    #     for _, row in df.iterrows():
    #         roll = str(row["Roll Number"])
    #         name = str(row["Name"]).upper()
    #         photo_path = os.path.join(self.image_folder, f"{roll}_cropped.png")
    #         qr_path = os.path.join(self.qr_folder, f"qr_{roll}.png")

    #         if not os.path.exists(photo_path) or not os.path.exists(qr_path):
    #             skipped.append({'Roll Number': roll, 'Name': name})
    #             continue

    #         template = Image.open(self.template_path).convert("RGB")
    #         draw = ImageDraw.Draw(template)

    #         photo = Image.open(photo_path).resize((self.sizes['photo'], self.sizes['photo']))
    #         template.paste(photo, tuple(map(int, self.positions['photo'])), mask=photo)

    #         qr = Image.open(qr_path).resize((self.sizes['qr'], self.sizes['qr']))
    #         template.paste(qr, tuple(map(int, self.positions['qr'])), qr.convert('RGBA'))

    #         font = ImageFont.truetype(self.get_font_path(), self.font_size)
    #         bbox = draw.textbbox((0, 0), name, font=font)
    #         text_width = bbox[2] - bbox[0]
    #         text_x = int(self.positions['name'][0]) - text_width // 2
    #         text_y = int(self.positions['name'][1])

    #         draw.text((text_x, text_y), name, font=font, fill=self.font_color)

    #         out_path = os.path.join(self.output_folder, f"{roll}_id_card.jpg")
    #         template.save(out_path)

    #     if skipped:
    #         pd.DataFrame(skipped).to_csv(os.path.join(self.output_folder, "skipped_records.csv"), index=False)

    #     messagebox.showinfo("Done", f"Generated ID cards.\nSkipped {len(skipped)} records.")

    def save_config(self):
        config = {
            "positions": self.positions,
            "sizes": self.sizes,
            "font_size": self.font_size,
            "font_color": self.font_color,
            "csv_path": self.csv_path,
            "image_folder": self.image_folder,
            "qr_folder": self.qr_folder,
            "template_path": self.template_path,
            "output_folder": self.output_folder
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as f:
                json.dump(config, f)
            messagebox.showinfo("Saved", "Configuration saved.")

    def load_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as f:
                config = json.load(f)
            self.positions = config.get("positions", self.positions)
            self.sizes = config.get("sizes", self.sizes)
            self.font_size = config.get("font_size", self.font_size)
            self.font_color = config.get("font_color", self.font_color)
            self.csv_path = config.get("csv_path", self.csv_path)
            self.image_folder = config.get("image_folder", self.image_folder)
            self.qr_folder = config.get("qr_folder", self.qr_folder)
            self.template_path = config.get("template_path", self.template_path)
            self.output_folder = config.get("output_folder", self.output_folder)

            self.photo_size_var.set(self.sizes['photo'])
            self.qr_size_var.set(self.sizes['qr'])
            self.font_size_var.set(self.font_size)
            self.refresh_preview()

# Run app
if __name__ == "__main__":
    root = tk.Tk()
    app = IDCardApp(root)
    root.mainloop()
