import tkinter as tk
from PIL import Image, ImageTk
import subprocess

def button1_click():
    print("Button 1 clicked")
    subprocess.Popen(["python", "attendance_report_attendance.py"])

def button2_click():
    print("Button 2 clicked")
    subprocess.Popen(["python", "attendance_report_stud_details.py"])

# Create the main window
root = tk.Tk()
root.title("Student Report")

# Set window size
window_width = 1000
window_height = 700
root.geometry(f"{window_width}x{window_height}")

# Calculate the position to center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"+{x_position}+{y_position}")

# Set minimum and maximum size for the main window
root.minsize(600, 400)
root.maxsize(1600, 1200)

# Load and resize background image
bg_img = Image.open("img\\bg.png")  # Replace "background_image.jpg" with your image path
bg_img = bg_img.resize((window_width, window_height))
bg_image = ImageTk.PhotoImage(bg_img)

# Create a canvas
canvas = tk.Canvas(root, width=window_width, height=window_height)
canvas.pack()

# Display background image
canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)

# Add a heading
heading_text = "STUDENT REPORT"
heading_font = ("Helvetica", 20, "bold")
heading_color = "white"
canvas.create_text(window_width/2, window_height*0.1, text=heading_text, font=heading_font, fill=heading_color, anchor=tk.CENTER)

# Create button images with larger size
button1_img = Image.open("img\\attendance.png")  # Replace "path_to_button1_image.png" with your image path
button1_img = button1_img.resize((200, 150))  # Increase the size
button1_image = ImageTk.PhotoImage(button1_img)

button2_img = Image.open("img\\student_details.png")  # Replace "path_to_button2_image.png" with your image path
button2_img = button2_img.resize((200, 150))  # Increase the size
button2_image = ImageTk.PhotoImage(button2_img)

# Create buttons with text
button1 = tk.Label(root, text="View Attendance Details", image=button1_image, compound=tk.TOP, bg="white", borderwidth=0, highlightthickness=0)
button1.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
button1.bind("<Button-1>", lambda event: button1_click())

button2 = tk.Label(root, text="View Student Details", image=button2_image, compound=tk.TOP, bg="white", borderwidth=0, highlightthickness=0)
button2.place(relx=0.7, rely=0.5, anchor=tk.CENTER)
button2.bind("<Button-1>", lambda event: button2_click())

# Run the Tkinter event loop
root.mainloop()
