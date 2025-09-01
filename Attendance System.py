import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.camera import Camera
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView
import cv2
import numpy as np
import os
import csv
import time
import sys

storage_path = "/storage/emulated/0/Download/attendance"
if not os.path.exists(storage_path):
    os.makedirs(storage_path)

FONT_SIZE = 32
BUTTON_HEIGHT = 130

COLOR_PRIMARY = [0.15, 0.5, 0.75, 1]
COLOR_SECONDARY = [0.9, 0.4, 0.3, 1]
COLOR_GREEN = [0.2, 0.7, 0.3, 1]
COLOR_GRAY = [0.7, 0.7, 0.7, 1]

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        label = Label(text="QR Attendance System", font_size=55, size_hint=(1, 0.3), bold=True, color=[1,1,1,1])
        layout.add_widget(label)

        layout.add_widget(self.create_button("Add Event", self.add_event, COLOR_GREEN))
        layout.add_widget(self.create_button("View Events", self.view_events, COLOR_PRIMARY))
        layout.add_widget(self.create_button("Start Attendance", self.select_event, COLOR_PRIMARY))
        layout.add_widget(self.create_button("Exit", self.exit_app, COLOR_SECONDARY))

        self.add_widget(layout)
        self.event_list_popup = None  # <<< tracker for the events list popup

    def create_button(self, text, callback, color):
        btn = Button(text=text, size_hint=(1, None), height=BUTTON_HEIGHT,
                     font_size=FONT_SIZE, background_color=color, background_normal='', border=(0,0,0,0))
        btn.bind(on_press=callback)
        return btn

    def load_events(self):
        events_file = os.path.join(storage_path, "events.csv")
        if not os.path.exists(events_file):
            return []
        with open(events_file, "r") as f:
            return [line.strip() for line in f if line.strip()]

    def save_events(self, events):
        events_file = os.path.join(storage_path, "events.csv")
        with open(events_file, "w") as f:
            for event in events:
                f.write(event + "\n")

    def add_event(self, instance):
        # -- unchanged --
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        input_box = TextInput(hint_text="Enter Event Name", font_size=FONT_SIZE, multiline=False)
        content.add_widget(input_box)

        btn_layout = BoxLayout(size_hint=(1, 0.3), spacing=10)
        btn_save = Button(text="Save", font_size=FONT_SIZE, background_color=COLOR_GREEN, background_normal='')
        btn_cancel = Button(text="Cancel", font_size=FONT_SIZE, background_color=COLOR_GRAY, background_normal='')

        def save_instance(inst):
            event_name = input_box.text.strip()
            if event_name:
                events = self.load_events()
                if event_name in events:
                    Popup(title="Duplicate Event",
                          content=Label(text="Event already exists!", font_size=FONT_SIZE),
                          size_hint=(0.7,0.4)).open()
                    return
                events.append(event_name)
                self.save_events(events)
                popup.dismiss()

        btn_save.bind(on_press=save_instance)
        btn_cancel.bind(on_press=lambda inst: popup.dismiss())
        btn_layout.add_widget(btn_save)
        btn_layout.add_widget(btn_cancel)
        content.add_widget(btn_layout)

        popup = Popup(title="Add Event", content=content, size_hint=(0.8,0.5))
        popup.open()

    def view_events(self, instance):
        # Dismiss any existing events-list popup
        if self.event_list_popup:
            self.event_list_popup.dismiss()
            self.event_list_popup = None

        events = self.load_events()
        if not events:
            Popup(title="No Events",
                  content=Label(text="No events available.", font_size=FONT_SIZE),
                  size_hint=(0.8,0.5)).open()
            return

        content = BoxLayout(orientation='vertical')
        scroll = ScrollView(size_hint=(1,1))
        box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=10)
        box.bind(minimum_height=box.setter('height'))

        for event in events:
            event_box = BoxLayout(size_hint_y=None, height=BUTTON_HEIGHT, spacing=10)

            lbl = Label(text=event, font_size=FONT_SIZE, size_hint=(0.4,1))
            event_box.add_widget(lbl)

            btn_view = Button(text="View", size_hint=(0.3,1), font_size=FONT_SIZE,
                              background_color=COLOR_PRIMARY, background_normal='')
            btn_view.bind(on_press=lambda inst, e=event: self.show_attendance_popup(e))
            event_box.add_widget(btn_view)

            btn_delete = Button(text="Delete", size_hint=(0.3,1), font_size=FONT_SIZE,
                                background_color=COLOR_SECONDARY, background_normal='')
            btn_delete.bind(on_press=lambda inst, e=event: self.delete_event(e))
            event_box.add_widget(btn_delete)

            box.add_widget(event_box)

        scroll.add_widget(box)
        content.add_widget(scroll)

        # Store and open the popup
        self.event_list_popup = Popup(title="View Events", content=content, size_hint=(0.9,0.9))
        self.event_list_popup.open()

    def delete_event(self, event):
        def confirm_delete(instance):
            events = self.load_events()
            if event in events:
                events.remove(event)
                self.save_events(events)
                attendance_file = os.path.join(storage_path, f"{event}.csv")
                if os.path.exists(attendance_file):
                    os.remove(attendance_file)
            # dismiss confirm dialog
            confirm_popup.dismiss()
            # now refresh or close the events list
            if self.event_list_popup:
                self.event_list_popup.dismiss()
                self.event_list_popup = None

            if events:
                # re-open list with remaining events
                Clock.schedule_once(lambda dt: self.view_events(None), 0)
            else:
                # no events left → show feedback
                Popup(title="No Events",
                      content=Label(text="No events available.", font_size=FONT_SIZE),
                      size_hint=(0.8,0.5)).open()

        # confirmation dialog
        confirm_box = BoxLayout(orientation='vertical', padding=20, spacing=10)
        confirm_box.add_widget(Label(text=f"Delete event '{event}'?", font_size=FONT_SIZE))

        btns = BoxLayout(size_hint=(1,0.3), spacing=10)
        btn_yes = Button(text="Yes", font_size=FONT_SIZE, background_color=COLOR_GREEN, background_normal='')
        btn_no = Button(text="No", font_size=FONT_SIZE, background_color=COLOR_GRAY, background_normal='')
        btn_yes.bind(on_press=confirm_delete)
        btn_no.bind(on_press=lambda inst: confirm_popup.dismiss())
        btns.add_widget(btn_yes)
        btns.add_widget(btn_no)
        confirm_box.add_widget(btns)

        confirm_popup = Popup(title="Confirm Delete", content=confirm_box, size_hint=(0.7,0.4))
        confirm_popup.open()

    # --- all methods below are unchanged: show_attendance_popup, delete_individual, select_event, start_attendance, exit_app ---

    def show_attendance_popup(self, event):
        file_path = os.path.join(storage_path, f"{event}.csv")
        data = []
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                reader = csv.reader(f)
                next(reader, None)
                data = [row for row in reader if row]
        if not data:
            Popup(title="No Attendance",
                  content=Label(text="No attendance found.", font_size=FONT_SIZE),
                  size_hint=(0.7,0.4)).open()
            return

        content = BoxLayout(orientation='vertical')
        scroll = ScrollView(size_hint=(1,1))
        box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        box.bind(minimum_height=box.setter('height'))

        for row in data:
            record_box = BoxLayout(size_hint_y=None, height=BUTTON_HEIGHT, spacing=10)
            text = f"{row[0]} {row[1]}"
            lbl = Label(text=text, font_size=FONT_SIZE, size_hint=(0.6,1))
            record_box.add_widget(lbl)

            btn_delete = Button(text="Delete", font_size=FONT_SIZE, size_hint=(0.4,1),
                                background_color=COLOR_SECONDARY, background_normal='')
            btn_delete.bind(on_press=lambda inst, r=row: self.delete_individual(event, r))
            record_box.add_widget(btn_delete)

            box.add_widget(record_box)

        scroll.add_widget(box)
        content.add_widget(scroll)

        btn_back = Button(text="Back", size_hint=(1,0.1), font_size=FONT_SIZE,
                          background_color=COLOR_PRIMARY, background_normal='')
        btn_back.bind(on_press=lambda inst: self.attendance_popup.dismiss())
        content.add_widget(btn_back)

        self.attendance_popup = Popup(title=f"Attendance: {event}", content=content, size_hint=(0.9,0.9))
        self.attendance_popup.open()

    def delete_individual(self, event, row_to_delete):
        file_path = os.path.join(storage_path, f"{event}.csv")
        rows = []
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if row != row_to_delete:
                    rows.append(row)
        with open(file_path, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)

        self.attendance_popup.dismiss()
        Clock.schedule_once(lambda dt: self.show_attendance_popup(event), 0.1)

    def select_event(self, instance):
        events = self.load_events()
        if not events:
            Popup(title="No Events",
                  content=Label(text="No events available.", font_size=FONT_SIZE),
                  size_hint=(0.8,0.5)).open()
            return

        content = BoxLayout(orientation='vertical')
        scroll = ScrollView(size_hint=(1,1))
        box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=15, padding=10)
        box.bind(minimum_height=box.setter('height'))

        for event in events:
            btn = Button(text=event, size_hint_y=None, height=BUTTON_HEIGHT, font_size=FONT_SIZE,
                         background_color=COLOR_PRIMARY, background_normal='')
            btn.bind(on_press=lambda btn_inst: self.start_attendance(btn_inst.text))
            box.add_widget(btn)

        scroll.add_widget(box)
        content.add_widget(scroll)

        popup = Popup(title="Select Event", content=content, size_hint=(0.9,0.9))
        popup.open()
        self.event_popup = popup

    def start_attendance(self, event_name):
        self.event_popup.dismiss()
        self.manager.current = 'camera'
        self.manager.get_screen('camera').set_event(event_name)

    def exit_app(self, instance):
        App.get_running_app().stop()
        sys.exit(0)


class CameraScreen(Screen):
    # -- unchanged --
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.event_name = None

        layout = BoxLayout(orientation='vertical')
        self.camera = Camera(play=False)
        self.camera.resolution = (640,480)
        layout.add_widget(self.camera)

        self.count_label = Label(text="", size_hint=(1,0.1), font_size=FONT_SIZE)
        layout.add_widget(self.count_label)

        btn_layout = BoxLayout(size_hint=(1,0.2), spacing=10, padding=10)
        btn_scan = Button(text="Scan QR Code", font_size=FONT_SIZE, background_color=COLOR_PRIMARY, background_normal='')
        btn_scan.bind(on_press=self.scan_qr)
        btn_stop = Button(text="Stop Attendance", font_size=FONT_SIZE, background_color=COLOR_SECONDARY, background_normal='')
        btn_stop.bind(on_press=self.stop_attendance)
        btn_layout.add_widget(btn_scan)
        btn_layout.add_widget(btn_stop)

        layout.add_widget(btn_layout)
        self.add_widget(layout)

    def set_event(self, event_name):
        self.event_name = event_name
        self.attendance_file = os.path.join(storage_path, f"{self.event_name}.csv")
        if not os.path.exists(self.attendance_file):
            with open(self.attendance_file, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["RollNumber","Name","Degree","Dept","Timestamp"])
        self.camera.play = True
        self.update_count_label()

    def stop_attendance(self, instance):
        self.camera.play = False
        self.manager.current = 'main'

    def scan_qr(self, instance):
        texture = self.camera.texture
        if not texture:
            return
        size = texture.size
        pixels = texture.pixels
        img = np.frombuffer(pixels, np.uint8).reshape(size[1], size[0], 4)
        img_bgr = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
        img_bgr = cv2.rotate(img_bgr, cv2.ROTATE_90_COUNTERCLOCKWISE)

        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img_bgr)

        if data:
            self.process_qr_data(data)
        self.update_count_label()

    # def process_qr_data(self, data):
    #     lines = data.strip().split('\n')
    #     fields = {}
    #     for line in lines:
    #         if ':' in line:
    #             key, value = line.split(':',1)
    #             fields[key.strip()] = value.strip()

    #     roll = fields.get('Roll','')
    #     name = fields.get('Name','')
    #     degree = fields.get('Degree','')
    #     dept = fields.get('Dept','')

    #     already_marked = False
    #     with open(self.attendance_file, "r") as f:
    #         reader = csv.reader(f)
    #         next(reader)
    #         for row in reader:
    #             if row[0] == roll:
    #                 already_marked = True
    #                 break

    #     if not already_marked and roll:
    #         with open(self.attendance_file, "a", newline='') as f:
    #             writer = csv.writer(f)
    #             writer.writerow([roll,name,degree,dept,time.strftime("%Y-%m-%d %H:%M:%S")])
    #         self.show_scan_popup(fields)
    #     elif already_marked:
    #         self.show_scan_popup(fields, already=True)

    def process_qr_data(self, data):
        # Parse the CSV-style QR code data
        parts = data.strip().split(',')
        if len(parts) != 4:
            print("Invalid QR code data format")
            return

        roll, name, degree, dept = [p.strip() for p in parts]

        already_marked = False
        with open(self.attendance_file, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row[0] == roll:
                    already_marked = True
                    break

        if not already_marked and roll:
            with open(self.attendance_file, "a", newline='') as f:
                writer = csv.writer(f)
                writer.writerow([roll, name, degree, dept, time.strftime("%Y-%m-%d %H:%M:%S")])
            self.show_scan_popup({
                "Roll": roll,
                "Name": name,
                "Degree": degree,
                "Dept": dept
            })
        elif already_marked:
            self.show_scan_popup({
                "Roll": roll,
                "Name": name,
                "Degree": degree,
                "Dept": dept
            }, already=True)

    def update_count_label(self):
        count = 0
        if os.path.exists(self.attendance_file):
            with open(self.attendance_file, "r") as f:
                reader = csv.reader(f)
                next(reader)
                count = sum(1 for _ in reader)
        self.count_label.text = f"Total Marked: {count}"

    def show_scan_popup(self, fields, already=False):
        if already:
            message = "Already Marked\n"
        else:
            message = "Marked Successfully\n"
        message += (f"Roll: {fields.get('Roll','')}\n"
                    f"Name: {fields.get('Name','')}\n"
                    f"Degree: {fields.get('Degree','')}\n"
                    f"Dept: {fields.get('Dept','')}")
        popup = Popup(title="Scan Result",
                      content=Label(text=message, font_size=FONT_SIZE),
                      size_hint=(0.8,0.5))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

class AttendanceApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(CameraScreen(name='camera'))
        return sm

if __name__ == '__main__':
    AttendanceApp().run()
