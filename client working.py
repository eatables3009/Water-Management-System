import tkinter as tk
from tkinter import messagebox
import socket


def search_database(latitude, longitude):
    try:
        # Connect to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', 65432))

        # Send coordinates to server
        coordinates = f"{latitude},{longitude}"
        client_socket.sendall(coordinates.encode("utf-8"))

        # Receive response from server
        response = client_socket.recv(1024).decode("utf-8")

        # Close the client socket
        client_socket.close()

        return response
    except Exception as e:
        return f"Error: {e}"


def search_coordinates():
    try:
        latitude = float(latitude_entry.get())
        longitude = float(longitude_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for latitude and longitude.")
        return

    result = search_database(latitude, longitude)

    if result == "Coordinates present in CSV file":
        messagebox.showinfo("Result", "You are in a flood prone region.")
    else:
        messagebox.showinfo("Result", "You are safe from floods")


root = tk.Tk()

latitude_label = tk.Label(root, text="Latitude:")
latitude_label.pack()
latitude_entry = tk.Entry(root)
latitude_entry.pack()

longitude_label = tk.Label(root, text="Longitude:")
longitude_label.pack()
longitude_entry = tk.Entry(root)
longitude_entry.pack()

search_button = tk.Button(root, text="Search", command=search_coordinates)
search_button.pack()

root.mainloop()
