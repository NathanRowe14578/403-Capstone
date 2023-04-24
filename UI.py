import tkinter as tk
import requests
# Create the main window
root = tk.Tk()
root.title("GPS Location and Distance")

# Define the GPS location labels
latitude_label = tk.Label(root, text="Lat:")
longitude_label = tk.Label(root, text="Lon:")

# Define the distance labels
front_left_label = tk.Label(root, text=" FL ")
front_middle_label = tk.Label(root, text=" FM ")
front_right_label = tk.Label(root, text=" FR ")
left_front_label = tk.Label(root, text=" LF ")
left_back_label = tk.Label(root, text=" LB ")
back_left_label = tk.Label(root, text=" BL ")
back_right_label = tk.Label(root, text=" BR ")
right_back_label = tk.Label(root, text=" RB ")
right_front_label = tk.Label(root, text=" RF ")

# Define the labels to display the actual values of the GPS location and distances
latitude_value = tk.Label(root, text="0.0")
longitude_value = tk.Label(root, text="0.0")
front_left_value = tk.Label(root, text="0.0")
front_middle_value = tk.Label(root, text="0.0")
front_right_value = tk.Label(root, text="0.0")
left_front_value = tk.Label(root, text="0.0")
left_back_value = tk.Label(root, text="0.0")
back_left_value = tk.Label(root, text="0.0")
back_right_value = tk.Label(root, text="0.0")
right_back_value = tk.Label(root, text="0.0")
right_front_value = tk.Label(root, text="0.0")

# Place the labels on the grid
latitude_label.grid(row=0, column=3)
longitude_label.grid(row=0, column=6)
front_left_label.grid(row=2, column=4)
front_middle_label.grid(row=2, column=5)
front_right_label.grid(row=2, column=6)
left_front_label.grid(row=4, column=3)
left_back_label.grid(row=6, column=3)
back_left_label.grid(row=8, column=4)
back_right_label.grid(row=8, column=6)
right_back_label.grid(row=4, column=7)
right_front_label.grid(row=6, column=7)

latitude_value.grid(row=0, column=4)
longitude_value.grid(row=0, column=7)
front_left_value.grid(row=3, column=4)
front_middle_value.grid(row=3, column=5)
front_right_value.grid(row=3, column=6)
left_front_value.grid(row=5, column=3)
left_back_value.grid(row=7, column=3)
back_left_value.grid(row=9, column=4)
back_right_value.grid(row=9, column=6)
right_back_value.grid(row=7, column=7)
right_front_value.grid(row=5, column=7)



def get_location():
    url = 'https://ipapi.co/json/'
    response = requests.get(url)
    data = response.json()

    latitude = data.get('latitude', 'N/A')
    longitude = data.get('longitude', 'N/A')

    print("Latitude:", latitude)
    print("Longitude:", longitude)

root.after(1000, get_location)


# Start the main event loop
root.mainloop()

