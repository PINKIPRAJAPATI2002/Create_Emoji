# import cv2
# import numpy as np
# from tkinter import Tk, Label, Button, filedialog
# from PIL import Image, ImageTk

# def cartoonify_image(image):
#     """Apply cartoon effect to an image."""
#     # Convert to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Apply median blur
#     gray = cv2.medianBlur(gray, 5)
    
#     # Get edges
#     edges = cv2.adaptiveThreshold(
#         gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
#     )
    
#     # Apply bilateral filter to smooth colors
#     color = cv2.bilateralFilter(image, 9, 300, 300)
    
#     # Combine edges and color
#     cartoon = cv2.bitwise_and(color, color, mask=edges)
#     return cartoon

# def capture_avatar():
#     """Capture image from webcam."""
#     cap = cv2.VideoCapture(0)
#     ret, frame = cap.read()
#     if ret:
#         cartoon = cartoonify_image(frame)
#         cv2.imwrite("avatar.png", cartoon)
#         show_avatar("avatar.png")
#     cap.release()
#     cv2.destroyAllWindows()

# def show_avatar(image_path):
#     """Display the avatar in the GUI."""
#     img = Image.open(image_path)
#     img = img.resize((300, 300))
#     img = ImageTk.PhotoImage(img)
#     label.config(image=img)
#     label.image = img

# def load_existing_image():
#     """Load an existing image from the disk."""
#     file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
#     if file_path:
#         cartoon = cartoonify_image(cv2.imread(file_path))
#         cv2.imwrite("avatar.png", cartoon)
#         show_avatar("avatar.png")

# # Create GUI
# root = Tk()
# root.title("Avatar Creator")

# label = Label(root, text="Avatar will appear here", width=40, height=15)
# label.pack(pady=10)

# capture_button = Button(root, text="Capture Avatar", command=capture_avatar)
# capture_button.pack(pady=5)

# load_button = Button(root, text="Load Existing Image", command=load_existing_image)
# load_button.pack(pady=5)

# exit_button = Button(root, text="Exit", command=root.quit)
# exit_button.pack(pady=5)

# root.mainloop()


import cv2
import numpy as np
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox
from PIL import Image, ImageTk

def cartoonify_image(image):
    """Apply cartoon effect to an image."""
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply median blur
    gray = cv2.medianBlur(gray, 5)
    
    # Get edges
    edges = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9
    )
    
    # Apply bilateral filter to smooth colors
    color = cv2.bilateralFilter(image, 9, 300, 300)
    
    # Combine edges and color
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

def capture_avatar():
    """Capture image from webcam."""
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cartoon = cartoonify_image(frame)
        cv2.imwrite("avatar_temp.png", cartoon)
        show_avatar("avatar_temp.png")
        messagebox.showinfo("Capture Complete", "Avatar captured successfully!")
    else:
        messagebox.showerror("Error", "Failed to capture image.")
    cap.release()
    cv2.destroyAllWindows()

def show_avatar(image_path):
    """Display the avatar in the GUI."""
    img = Image.open(image_path)
    img = img.resize((300, 300))
    img = ImageTk.PhotoImage(img)
    avatar_label.config(image=img)
    avatar_label.image = img

def save_avatar():
    """Save the avatar with a custom file name."""
    file_name = file_name_entry.get()
    if not file_name.strip():
        messagebox.showerror("Error", "Please enter a valid file name.")
        return
    file_path = f"{file_name}.png"
    try:
        img = Image.open("avatar_temp.png")
        img.save(file_path)
        messagebox.showinfo("Save Complete", f"Avatar saved as {file_path}")
    except FileNotFoundError:
        messagebox.showerror("Error", "No avatar found. Please capture one first.")

def load_existing_image():
    """Load an existing image from the disk and process it."""
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image = cv2.imread(file_path)
        cartoon = cartoonify_image(image)
        cv2.imwrite("avatar_temp.png", cartoon)
        show_avatar("avatar_temp.png")
        messagebox.showinfo("Processing Complete", "Avatar created from the selected image!")

# Create GUI
root = Tk()
root.title("Avatar Creator")
root.geometry("400x500")

# Avatar display
avatar_label = Label(root, text="Avatar will appear here", width=40, height=15)
avatar_label.pack(pady=10)

# Buttons
capture_button = Button(root, text="Capture Avatar", command=capture_avatar)
capture_button.pack(pady=5)

load_button = Button(root, text="Load Existing Image", command=load_existing_image)
load_button.pack(pady=5)

# File name entry and save button
file_name_label = Label(root, text="Enter File Name:")
file_name_label.pack(pady=5)
file_name_entry = Entry(root, width=30)
file_name_entry.pack(pady=5)

save_button = Button(root, text="Save Avatar", command=save_avatar)
save_button.pack(pady=5)

exit_button = Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=20)

root.mainloop()
