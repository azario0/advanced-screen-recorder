import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
import threading
import time
from PIL import Image, ImageTk
import pyautogui
import os
from datetime import datetime

class ScreenRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Screen Recorder")
        self.root.geometry("400x500")
        self.root.resizable(True, True)
        
        # Recording variables
        self.is_recording = False
        self.is_previewing = False
        self.video_writer = None
        self.preview_thread = None
        self.record_thread = None
        self.preview_window = None
        
        # Recording settings
        self.fps = tk.IntVar(value=30)
        self.quality = tk.StringVar(value="High")
        self.output_format = tk.StringVar(value=".mp4")
        self.output_path = tk.StringVar(value=os.path.expanduser("~/Desktop"))
        
        # Screen capture area
        self.start_x = 100
        self.start_y = 100
        self.width = 800
        self.height = 600
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Screen Recorder", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Recording Area Settings
        area_frame = ttk.LabelFrame(main_frame, text="Recording Area", padding="10")
        area_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(area_frame, text="Select Area & Preview", 
                  command=self.open_preview_window, width=25).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Area info display
        self.area_info = ttk.Label(area_frame, text=f"Area: {self.width}x{self.height} at ({self.start_x}, {self.start_y})")
        self.area_info.grid(row=1, column=0, columnspan=2)
        
        # Recording Settings
        settings_frame = ttk.LabelFrame(main_frame, text="Recording Settings", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Frame Rate
        ttk.Label(settings_frame, text="Frame Rate (FPS):").grid(row=0, column=0, sticky=tk.W)
        fps_frame = ttk.Frame(settings_frame)
        fps_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        fps_scale = ttk.Scale(fps_frame, from_=10, to=60, variable=self.fps, orient=tk.HORIZONTAL)
        fps_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        fps_label = ttk.Label(fps_frame, textvariable=self.fps)
        fps_label.grid(row=0, column=1, padx=(5, 0))
        
        # Quality
        ttk.Label(settings_frame, text="Quality:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        quality_combo = ttk.Combobox(settings_frame, textvariable=self.quality, 
                                   values=["Low", "Medium", "High", "Ultra"], state="readonly", width=15)
        quality_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # Output Format
        ttk.Label(settings_frame, text="Format:").grid(row=2, column=0, sticky=tk.W, pady=(10, 0))
        format_combo = ttk.Combobox(settings_frame, textvariable=self.output_format,
                                  values=[".mp4", ".avi", ".mov"], state="readonly", width=15)
        format_combo.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # Output Path
        path_frame = ttk.Frame(settings_frame)
        path_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        ttk.Label(path_frame, text="Output Folder:").grid(row=0, column=0, sticky=tk.W)
        
        path_display_frame = ttk.Frame(path_frame)
        path_display_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        self.path_label = ttk.Label(path_display_frame, text=self.output_path.get(), 
                                   foreground="blue", cursor="hand2")
        self.path_label.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Button(path_display_frame, text="Browse", 
                  command=self.browse_output_path, width=8).grid(row=0, column=1, padx=(10, 0))
        
        # Control Buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, columnspan=2, pady=(20, 0))
        
        self.record_button = ttk.Button(control_frame, text="Start Recording", 
                                       command=self.toggle_recording, width=15)
        self.record_button.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(control_frame, text="Stop Recording", 
                  command=self.stop_recording, width=15).grid(row=0, column=1)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="Ready to record", foreground="green")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        # Recording time
        self.time_label = ttk.Label(main_frame, text="00:00:00", font=("Arial", 12, "bold"))
        self.time_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        fps_frame.columnconfigure(0, weight=1)
        path_display_frame.columnconfigure(0, weight=1)
        
    def open_preview_window(self):
        if self.preview_window and self.preview_window.winfo_exists():
            self.preview_window.destroy()
            
        self.preview_window = tk.Toplevel(self.root)
        self.preview_window.title("Recording Area Preview - Resize and Position")
        self.preview_window.geometry(f"{self.width}x{self.height+50}+{self.start_x}+{self.start_y}")
        self.preview_window.attributes('-alpha', 0.7)
        self.preview_window.configure(bg='red')
        
        # Preview frame
        preview_frame = ttk.Frame(self.preview_window)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Canvas for preview
        self.preview_canvas = tk.Canvas(preview_frame, bg='black', highlightthickness=2, 
                                       highlightbackground='red')
        self.preview_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Control buttons frame
        button_frame = ttk.Frame(self.preview_window, style='Red.TFrame')
        button_frame.pack(fill=tk.X, pady=2)
        
        ttk.Button(button_frame, text="Start Preview", 
                  command=self.start_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Stop Preview", 
                  command=self.stop_preview).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Confirm Area", 
                  command=self.confirm_area).pack(side=tk.RIGHT, padx=5)
        
        # Info label
        info_label = ttk.Label(button_frame, text="Resize window to set recording area", 
                              font=("Arial", 8))
        info_label.pack(side=tk.RIGHT, padx=10)
        
        # Bind window events
        self.preview_window.bind('<Configure>', self.on_preview_resize)
        self.preview_window.protocol("WM_DELETE_WINDOW", self.close_preview_window)
        
    def on_preview_resize(self, event):
        if event.widget == self.preview_window:
            # Update dimensions and position
            self.width = max(100, self.preview_window.winfo_width() - 4)
            self.height = max(100, self.preview_window.winfo_height() - 54)  # Account for button frame
            self.start_x = self.preview_window.winfo_x()
            self.start_y = self.preview_window.winfo_y()
            
            # Update info display
            self.area_info.config(text=f"Area: {self.width}x{self.height} at ({self.start_x}, {self.start_y})")
            
    def start_preview(self):
        if not self.is_previewing:
            self.is_previewing = True
            self.preview_thread = threading.Thread(target=self.preview_loop, daemon=True)
            self.preview_thread.start()
            
    def stop_preview(self):
        self.is_previewing = False
        if self.preview_canvas.winfo_exists():
            self.preview_canvas.delete("all")
            
    def preview_loop(self):
        while self.is_previewing and self.preview_window and self.preview_window.winfo_exists():
            try:
                # Capture screen area
                screenshot = pyautogui.screenshot(region=(self.start_x, self.start_y, self.width, self.height))
                
                # Convert to display format
                canvas_width = self.preview_canvas.winfo_width()
                canvas_height = self.preview_canvas.winfo_height()
                
                if canvas_width > 1 and canvas_height > 1:
                    # Resize image to fit canvas
                    screenshot = screenshot.resize((canvas_width, canvas_height), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(screenshot)
                    
                    # Update canvas
                    self.preview_canvas.delete("all")
                    self.preview_canvas.create_image(canvas_width//2, canvas_height//2, 
                                                   image=photo, anchor=tk.CENTER)
                    self.preview_canvas.image = photo  # Keep a reference
                    
                time.sleep(1/30)  # 30 FPS preview
                
            except Exception as e:
                print(f"Preview error: {e}")
                break
                
    def confirm_area(self):
        self.stop_preview()
        if self.preview_window:
            self.preview_window.destroy()
        self.status_label.config(text=f"Area set: {self.width}x{self.height}", foreground="blue")
        
    def close_preview_window(self):
        self.stop_preview()
        if self.preview_window:
            self.preview_window.destroy()
            
    def browse_output_path(self):
        folder = filedialog.askdirectory(initialdir=self.output_path.get())
        if folder:
            self.output_path.set(folder)
            self.path_label.config(text=folder)
            
    def get_codec_and_quality(self):
        quality_settings = {
            "Low": (15, cv2.VideoWriter_fourcc(*'mp4v')),
            "Medium": (20, cv2.VideoWriter_fourcc(*'mp4v')),
            "High": (25, cv2.VideoWriter_fourcc(*'mp4v')),
            "Ultra": (30, cv2.VideoWriter_fourcc(*'XVID'))
        }
        
        if self.output_format.get() == ".avi":
            return quality_settings[self.quality.get()][0], cv2.VideoWriter_fourcc(*'XVID')
        elif self.output_format.get() == ".mov":
            return quality_settings[self.quality.get()][0], cv2.VideoWriter_fourcc(*'mp4v')
        else:  # mp4
            return quality_settings[self.quality.get()][0], cv2.VideoWriter_fourcc(*'mp4v')
            
    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self):
        try:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screen_recording_{timestamp}{self.output_format.get()}"
            self.output_file = os.path.join(self.output_path.get(), filename)
            
            # Get codec and quality
            quality_factor, fourcc = self.get_codec_and_quality()
            
            # Initialize video writer
            self.video_writer = cv2.VideoWriter(
                self.output_file,
                fourcc,
                self.fps.get(),
                (self.width, self.height)
            )
            
            if not self.video_writer.isOpened():
                raise Exception("Failed to initialize video writer")
                
            # Start recording
            self.is_recording = True
            self.record_start_time = time.time()
            self.record_thread = threading.Thread(target=self.record_loop, daemon=True)
            self.record_thread.start()
            
            # Update UI
            self.record_button.config(text="Recording...", state="disabled")
            self.status_label.config(text="Recording in progress...", foreground="red")
            
            # Start timer update
            self.update_timer()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {str(e)}")
            
    def record_loop(self):
        frame_duration = 1.0 / self.fps.get()
        
        while self.is_recording:
            frame_start = time.time()
            
            try:
                # Capture screen
                screenshot = pyautogui.screenshot(region=(self.start_x, self.start_y, self.width, self.height))
                
                # Convert PIL to OpenCV format
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                
                # Write frame
                if self.video_writer:
                    self.video_writer.write(frame)
                    
                # Control frame rate
                elapsed = time.time() - frame_start
                sleep_time = max(0, frame_duration - elapsed)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
            except Exception as e:
                print(f"Recording error: {e}")
                break
                
    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            
            # Wait for recording thread to finish
            if self.record_thread and self.record_thread.is_alive():
                self.record_thread.join(timeout=2)
                
            # Close video writer
            if self.video_writer:
                self.video_writer.release()
                self.video_writer = None
                
            # Update UI
            self.record_button.config(text="Start Recording", state="normal")
            self.status_label.config(text=f"Recording saved: {os.path.basename(self.output_file)}", 
                                   foreground="green")
            self.time_label.config(text="00:00:00")
            
            # Show completion message
            messagebox.showinfo("Recording Complete", 
                              f"Recording saved successfully!\n\nFile: {self.output_file}")
                              
    def update_timer(self):
        if self.is_recording:
            elapsed = time.time() - self.record_start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.time_label.config(text=time_str)
            
            # Schedule next update
            self.root.after(1000, self.update_timer)
            
    def on_closing(self):
        # Stop all operations
        self.stop_recording()
        self.stop_preview()
        
        if self.preview_window:
            self.preview_window.destroy()
            
        self.root.destroy()
        
    def run(self):
        # Set up close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start the GUI
        self.root.mainloop()

class PreviewWindow:
    def __init__(self, parent_recorder):
        self.recorder = parent_recorder
        self.create_overlay()
        
    def create_overlay(self):
        # Create a semi-transparent overlay window
        self.overlay = tk.Toplevel()
        self.overlay.title("Recording Area Selector")
        self.overlay.attributes('-alpha', 0.3)
        self.overlay.configure(bg='red')
        self.overlay.geometry(f"{self.recorder.width}x{self.recorder.height}+{self.recorder.start_x}+{self.recorder.start_y}")
        
        # Make it stay on top
        self.overlay.attributes('-topmost', True)
        
        # Add border
        self.overlay.configure(highlightbackground='red', highlightthickness=3)
        
        # Instructions label
        instructions = tk.Label(self.overlay, 
                               text="Resize and move this window to select recording area\nThen click 'Confirm Area'",
                               bg='red', fg='white', font=('Arial', 12, 'bold'))
        instructions.place(relx=0.5, rely=0.5, anchor='center')

if __name__ == "__main__":
    # Check if required modules are available
    try:
        import pyautogui
        import cv2
        from PIL import Image, ImageTk
    except ImportError as e:
        print(f"Missing required module: {e}")
        print("Please install required packages:")
        print("pip install opencv-python pillow pyautogui")
        exit(1)
        
    # Disable pyautogui failsafe for smoother operation
    pyautogui.FAILSAFE = False
    
    # Create and run the application
    app = ScreenRecorder()
    app.run()