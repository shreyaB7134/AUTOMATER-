import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk
import pywhatkit
import qrcode
from googletrans import Translator

# Main interface background images and icon paths
BACKGROUND_IMAGES = {
    "menu": "main background.jpeg",
    "whatsapp": "Sky-Desktop-Backgrounds-Hd-Images.jpg",
    "translation": "moon.jpg",
    "qr_code": "Sky-Desktop-Backgrounds-Hd-Images.jpg"
}
ICONS = {
    "whatsapp": "whatsapp logo.jpeg",
    "translation": "googel translator.jpeg",
    "qr_code": "qrcode.png"
}

# Function to show success message
def show_success_message(text):
    popup = Toplevel(root)
    popup.geometry("200x200")
    popup.configure(bg="lightgreen")
    popup.title("Success")
    
    msg = tk.Label(popup, text=text, font=("Arial", 12, "bold"), fg="green", bg="lightgreen")
    msg.pack(expand=True)

# WhatsApp Message Delivery function
def open_message_delivery():
    def send_whatsapp_message():
        try:
            phone_number = phone_entry.get()
            message = message_entry.get()
            scheduled_time = time_entry.get()
            translate_option = translate_var.get()
            
            if translate_option == 1:
                target_lang = lang_entry.get()
                translator = Translator()
                message = translator.translate(message, dest=target_lang).text
            
            hour, minute = map(int, scheduled_time.split(':'))
            pywhatkit.sendwhatmsg(phone_number, message, hour, minute)
            show_success_message("Message scheduled successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to schedule message: {e}")

    delivery_window = Toplevel(root)
    delivery_window.title("WhatsApp Message Delivery")
    delivery_window.geometry("800x600")
    set_background(delivery_window, BACKGROUND_IMAGES["whatsapp"])

    icon_label = tk.Label(delivery_window, image=icons["whatsapp"], bg="white")
    icon_label.pack(pady=10)

    tk.Label(delivery_window, text="Phone Number (with country code):", font=("Arial", 12), bg="white").pack(pady=5)
    phone_entry = tk.Entry(delivery_window, font=("Arial", 12))
    phone_entry.pack()

    tk.Label(delivery_window, text="Message:", font=("Arial", 12), bg="white").pack(pady=5)
    message_entry = tk.Entry(delivery_window, font=("Arial", 12))
    message_entry.pack()

    tk.Label(delivery_window, text="Scheduled Time (HH:MM):", font=("Arial", 12), bg="white").pack(pady=5)
    time_entry = tk.Entry(delivery_window, font=("Arial", 12))
    time_entry.pack()

    # Checkbox for translation option
    translate_var = tk.IntVar()
    translate_checkbox = tk.Checkbutton(delivery_window, text="Translate message before sending?", variable=translate_var, font=("Arial", 12), bg="white")
    translate_checkbox.pack(pady=5)

    # Entry for language code, shown only if the user wants translation
    lang_label = tk.Label(delivery_window, text="Target Language Code:", font=("Arial", 12), bg="white")
    lang_entry = tk.Entry(delivery_window, font=("Arial", 12))
    
    def toggle_lang_entry():
        if translate_var.get() == 1:
            lang_label.pack(pady=5)
            lang_entry.pack()
        else:
            lang_label.pack_forget()
            lang_entry.pack_forget()

    translate_checkbox.config(command=toggle_lang_entry)

    send_button = tk.Button(delivery_window, text="Schedule Message", command=send_whatsapp_message, font=("Arial", 12), bg="#4A90E2", fg="white")
    send_button.pack(pady=20)

# QR Code Generation function with multiple WhatsApp sending option
def open_qr_code():
    def generate_qr():
        try:
            url = url_entry.get()
            qr = qrcode.make(url)
            qr_path = "generated_qr.png"
            qr.save(qr_path)
            
            # Display a success message after QR is generated
            show_success_message("QR code generated successfully!")
            
            # Ask user if they want to send the QR via WhatsApp
            send_qr_var = messagebox.askyesno("Send QR Code", "Do you want to send this QR Code via WhatsApp?")
            if send_qr_var:
                try:
                    # Ask the user how many contacts to send to
                    num_contacts = int(number_of_contacts_entry.get())
                    phone_numbers = [entry.get() for entry in phone_entries[:num_contacts]]

                    # Send the QR code to each contact
                    for phone_number in phone_numbers:
                        pywhatkit.sendwhats_image(phone_number, qr_path, "Here is your QR code")
                    
                    show_success_message("QR code sent to all specified contacts successfully!")
                
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to send QR code to contacts: {e}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {e}")

    # Create QR generation interface
    qr_window = Toplevel(root)
    qr_window.title("QR Code Generator")
    qr_window.geometry("800x600")
    set_background(qr_window, BACKGROUND_IMAGES["qr_code"])

    icon_label = tk.Label(qr_window, image=icons["qr_code"], bg="white")
    icon_label.pack(pady=10)

    tk.Label(qr_window, text="Enter URL:", font=("Arial", 12), bg="white").pack(pady=5)
    url_entry = tk.Entry(qr_window, font=("Arial", 12), width=40)
    url_entry.pack()

    # Prompt to ask how many numbers the QR should be sent to
    tk.Label(qr_window, text="How many numbers to send QR Code to?", font=("Arial", 12), bg="white").pack(pady=5)
    number_of_contacts_entry = tk.Entry(qr_window, font=("Arial", 12), width=5)
    number_of_contacts_entry.pack()

    # Function to add phone number entry fields based on user input
    phone_entries = []
    def add_phone_number_fields():
        for entry in phone_entries:
            entry.destroy()  # Remove existing entry fields
        phone_entries.clear()

        try:
            count = int(number_of_contacts_entry.get())
            for i in range(count):
                tk.Label(qr_window, text=f"Enter phone number {i + 1}:", font=("Arial", 12), bg="white").pack()
                phone_entry = tk.Entry(qr_window, font=("Arial", 12), width=30)
                phone_entry.pack()
                phone_entries.append(phone_entry)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for contacts.")

    # Button to confirm number of contacts and create entry fields
    confirm_button = tk.Button(qr_window, text="Confirm", command=add_phone_number_fields, font=("Arial", 12), bg="#4A90E2", fg="white")
    confirm_button.pack(pady=10)

    # Button to generate QR Code and send it
    generate_button = tk.Button(qr_window, text="Generate QR Code and Send", command=generate_qr, font=("Arial", 12), bg="#4A90E2", fg="white")
    generate_button.pack(pady=20)



# Function to set background image for a window
def set_background(window, image_path):
    bg_image = Image.open(image_path)
    bg_photo = ImageTk.PhotoImage(bg_image.resize((800, 600)))
    bg_label = tk.Label(window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = bg_photo

# Main Menu
def main_menu():
    set_background(root, BACKGROUND_IMAGES["menu"])
    title = tk.Label(root, text="Choose an Option", font=("Arial", 24, "bold"), bg="white")
    title.pack(pady=30)

    message_button = tk.Button(root, image=icons["whatsapp"], command=open_message_delivery, width=100, height=100, compound="top", text="WhatsApp Message", font=("Arial", 12), bg="#4A90E2", fg="white")
    message_button.pack(pady=20)

    translation_button = tk.Button(root, image=icons["translation"], command=open_translation, width=100, height=100, compound="top", text="Translate Text", font=("Arial", 12), bg="#4A90E2", fg="white")
    translation_button.pack(pady=20)

    qr_button = tk.Button(root, image=icons["qr_code"], command=open_qr_code, width=100, height=100, compound="top", text="Generate QR Code", font=("Arial", 12), bg="#4A90E2", fg="white")
    qr_button.pack(pady=20)

# Initialize main window
root = tk.Tk()
root.title("Mini Project Hub")
root.geometry("800x600")
root.resizable(False, False)

# Load icons
icons = {name: ImageTk.PhotoImage(Image.open(path).resize((80, 80))) for name, path in ICONS.items()}

main_menu()
root.mainloop()