import os

import dotenv
import tkinter as tk
from tkinter import messagebox

from hand_tracking import hand_tracking
from camera_calibration import camera_calibration
from test_cameras import test_cameras
from utils.validate_input import validate_input

# Load .env file
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

class GUI():
  def __init__(self):
    self.root = tk.Tk()
    self.root.title(string="Hand Tracking")
    self.root.resizable(width=0, height=0)

    self.main_menu_view()

    self.root.protocol(name="WM_DELETE_WINDOW", func=self.on_close)
    self.root.mainloop()

  def main_menu_view(self):
    # Destroy all widgets
    for i in self.root.winfo_children():
      i.destroy()

    self.view_title = tk.Label(master=self.root, text="Hand Tracking in 3D Space", font=("TkDefaultFont", 16))
    self.view_title.pack(padx=(42, 42), pady=(42, 0))

    self.pixel_hand_tracking = tk.PhotoImage(width=1, height=1)
    self.button_hand_tracking = tk.Button(master=self.root, text="Hand Tracking", font=("TkDefaultFont", 12), image=self.pixel_hand_tracking, width=160, height=40, compound="c", command=hand_tracking)
    self.button_hand_tracking.pack(pady=(42, 0))

    self.pixel_camera_calibration = tk.PhotoImage(width=1, height=1)
    self.button_camera_calibration = tk.Button(master=self.root, text="Camera Calibration", font=("TkDefaultFont", 12), image=self.pixel_camera_calibration, width=160, height=40, compound="c", command=camera_calibration)
    self.button_camera_calibration.pack(pady=(32, 0))

    self.pixel_test_cameras = tk.PhotoImage(width=1, height=1)
    self.button_test_cameras = tk.Button(master=self.root, text="Test Cameras", font=("TkDefaultFont", 12), image=self.pixel_test_cameras, width=160, height=40, compound="c", command=test_cameras)
    self.button_test_cameras.pack(pady=(32, 0))

    self.pixel_settings = tk.PhotoImage(width=1, height=1)
    self.button_settings = tk.Button(master=self.root, text="Settings", font=("TkDefaultFont", 12), image=self.pixel_settings, width=160, height=40, compound="c", command=self.settings_view)
    self.button_settings.pack(pady=(32, 0))

    self.pixel_quit = tk.PhotoImage(width=1, height=1)
    self.button_quit = tk.Button(master=self.root, text="Quit", font=("TkDefaultFont", 12), image=self.pixel_quit, width=160, height=40, compound="c", command=self.on_close)
    self.button_quit.pack(pady=(32, 42))

  def settings_view(self):
    # Destroy all widgets
    for i in self.root.winfo_children():
      i.destroy()

    self.view_title = tk.Label(master=self.root, text="Settings", font=("TkDefaultFont", 16))
    self.view_title.pack(pady=(42, 0))

    self.grid_frame = tk.Frame(master=self.root)
    self.grid_frame.pack(padx=(42, 42), pady=(42, 0))

    self.left_column_frame = tk.Frame(master=self.grid_frame)
    self.left_column_frame.pack(side="left")

    self.camera_0_label = tk.Label(master=self.left_column_frame, text="Camera 0 ID", font=("TkDefaultFont", 12))
    self.camera_0_label.pack(pady=(0, 4))

    self.camera_0_entry = tk.Entry(master=self.left_column_frame, font=("TkDefaultFont", 12), width=12)
    self.camera_0_entry.pack()

    self.width_label = tk.Label(master=self.left_column_frame, text="Frame Width", font=("TkDefaultFont", 12))
    self.width_label.pack(pady=(16, 4))

    self.width_entry = tk.Entry(master=self.left_column_frame, font=("TkDefaultFont", 12), width=12)
    self.width_entry.pack()

    self.chessboard_rows_label = tk.Label(master=self.left_column_frame, text="Chessboard Rows", font=("TkDefaultFont", 12))
    self.chessboard_rows_label.pack(pady=(16, 4))

    self.chessboard_rows_entry = tk.Entry(master=self.left_column_frame, font=("TkDefaultFont", 12), width=12)
    self.chessboard_rows_entry.pack()

    self.chessboard_columns_label = tk.Label(master=self.left_column_frame, text="Chessboard Columns", font=("TkDefaultFont", 12))
    self.chessboard_columns_label.pack(pady=(16, 4))

    self.chessboard_columns_entry = tk.Entry(master=self.left_column_frame, font=("TkDefaultFont", 12), width=12)
    self.chessboard_columns_entry.pack()

    self.chessboard_square_size_label = tk.Label(master=self.left_column_frame, text="Chessboard Square Size", font=("TkDefaultFont", 12))
    self.chessboard_square_size_label.pack(pady=(16, 4))

    self.chessboard_square_size_entry = tk.Entry(master=self.left_column_frame, font=("TkDefaultFont", 12), width=12)
    self.chessboard_square_size_entry.pack()

    self.right_column_frame = tk.Frame(master=self.grid_frame)
    self.right_column_frame.pack(side="right")

    self.camera_1_label = tk.Label(master=self.right_column_frame, text="Camera 1 ID", font=("TkDefaultFont", 12))
    self.camera_1_label.pack(pady=(0, 4))

    self.camera_1_entry = tk.Entry(master=self.right_column_frame, font=("TkDefaultFont", 12), width=12)
    self.camera_1_entry.pack()

    self.height_label = tk.Label(master=self.right_column_frame, text="Frame Height", font=("TkDefaultFont", 12))
    self.height_label.pack(pady=(16, 4))

    self.height_entry = tk.Entry(master=self.right_column_frame, font=("TkDefaultFont", 12), width=12)
    self.height_entry.pack()

    self.min_hand_detection_confidence_label = tk.Label(master=self.right_column_frame, text="Min Hand Detection Confidence", font=("TkDefaultFont", 12))
    self.min_hand_detection_confidence_label.pack(pady=(16, 4))

    self.min_hand_detection_confidence_entry = tk.Entry(master=self.right_column_frame, font=("TkDefaultFont", 12), width=12)
    self.min_hand_detection_confidence_entry.pack()

    self.min_hand_presence_confidence_label = tk.Label(master=self.right_column_frame, text="Min Hand Presence Confidence", font=("TkDefaultFont", 12))
    self.min_hand_presence_confidence_label.pack(pady=(16, 4))

    self.min_hand_presence_confidence_entry = tk.Entry(master=self.right_column_frame, font=("TkDefaultFont", 12), width=12)
    self.min_hand_presence_confidence_entry.pack()

    self.min_tracking_confidence_label = tk.Label(master=self.right_column_frame, text="Min Tracking Confidence", font=("TkDefaultFont", 12))
    self.min_tracking_confidence_label.pack(pady=(16, 4))

    self.min_tracking_confidence_entry = tk.Entry(master=self.right_column_frame, font=("TkDefaultFont", 12), width=12)
    self.min_tracking_confidence_entry.pack()

    self.pixel_save = tk.PhotoImage(width=1, height=1)
    self.button_save = tk.Button(master=self.root, text="Save", font=("TkDefaultFont", 12), image=self.pixel_save, width=160, height=40, compound="c", command=self.save_settings)
    self.button_save.pack(pady=(42, 0))

    self.pixel_back = tk.PhotoImage(width=1, height=1)
    self.button_back = tk.Button(master=self.root, text="Back", font=("TkDefaultFont", 12), image=self.pixel_back, width=160, height=40, compound="c", command=self.main_menu_view)
    self.button_back.pack(pady=(32, 42))

    self.load_settings()

  def on_close(self):
    if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
      self.root.destroy()

  def load_settings(self):
    self.camera_0_entry.insert(0, os.environ["CAMERA_0_ID"])
    self.camera_1_entry.insert(0, os.environ["CAMERA_1_ID"])
    
    self.width_entry.insert(0, os.environ["FRAME_WIDTH"])
    self.height_entry.insert(0, os.environ["FRAME_HEIGHT"])
    
    self.chessboard_rows_entry.insert(0, os.environ["CHESSBOARD_ROWS"])
    self.chessboard_columns_entry.insert(0, os.environ["CHESSBOARD_COLUMNS"])
    self.chessboard_square_size_entry.insert(0, os.environ["CHESSBOARD_SQUARE_SIZE"])

    self.min_hand_detection_confidence_entry.insert(0, os.environ["MIN_HAND_DETECTION_CONFIDENCE"])
    self.min_hand_presence_confidence_entry.insert(0, os.environ["MIN_HAND_PRESENCE_CONFIDENCE"])
    self.min_tracking_confidence_entry.insert(0, os.environ["MIN_TRACKING_CONFIDENCE"])

  def save_settings(self):
    settings_state = {
      "CAMERA_0_ID": self.camera_0_entry.get(),
      "CAMERA_1_ID": self.camera_1_entry.get(),
      "FRAME_WIDTH": self.width_entry.get(),
      "FRAME_HEIGHT": self.height_entry.get(),
      "CHESSBOARD_ROWS": self.chessboard_rows_entry.get(),
      "CHESSBOARD_COLUMNS": self.chessboard_columns_entry.get(),
      "CHESSBOARD_SQUARE_SIZE": self.chessboard_square_size_entry.get(),
      "MIN_HAND_DETECTION_CONFIDENCE": self.min_hand_detection_confidence_entry.get(),
      "MIN_HAND_PRESENCE_CONFIDENCE": self.min_hand_presence_confidence_entry.get(),
      "MIN_TRACKING_CONFIDENCE": self.min_tracking_confidence_entry.get()   
    }

    error_state = {
      "CAMERA_0_ID": False,
      "CAMERA_1_ID": False,
      "FRAME_WIDTH": False,
      "FRAME_HEIGHT": False,
      "CHESSBOARD_ROWS": False,
      "CHESSBOARD_COLUMNS": False,
      "CHESSBOARD_SQUARE_SIZE": False,
      "MIN_HAND_DETECTION_CONFIDENCE": False,
      "MIN_HAND_PRESENCE_CONFIDENCE": False,
      "MIN_TRACKING_CONFIDENCE": False
    }

    has_error = False;

    for key, value in settings_state.items():
      type = "float"
      in_range = False
      if key in ["CAMERA_0_ID", "CAMERA_1_ID", "FRAME_WIDTH", "FRAME_HEIGHT", "CHESSBOARD_ROWS", "CHESSBOARD_COLUMNS", "CHESSBOARD_SQUARE_SIZE"]:
        type = "int"
      if key in ["MIN_HAND_DETECTION_CONFIDENCE", "MIN_HAND_PRESENCE_CONFIDENCE", "MIN_TRACKING_CONFIDENCE"]:
        in_range = True

      if validate_input(input=value, type=type, range=in_range):
        os.environ[key] = value
        dotenv.set_key(dotenv_path=dotenv_file, key_to_set=key, value_to_set=os.environ[key])
      else:
        has_error = True
        error_state[key] = True

    if has_error:
      error_message = ""
      for key, value in error_state.items():
        if value == True:
          error_message += f"Error in {key} input\n"

      messagebox.showerror(title="Error", message=error_message)
    else:
      messagebox.showinfo(title="Success", message="Settings saved successfully")

GUI()