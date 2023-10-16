import tkinter
from tkinter import messagebox
import pyrebase
import time as sleep

config = {
    "apiKey": "AIzaSyAWUUWU3mlrSh7rl_98PUNGbrexEoxOfWY",
    "authDomain": "sensor-data-910f3.firebaseapp.com",
    "databaseURL": "https://sensor-data-910f3-default-rtdb.firebaseio.com",
    "projectId": "sensor-data-910f3",
    "storageBucket": "sensor-data-910f3.appspot.com",
    "messagingSenderId": "245439021088",
    "appId": "1:245439021088:web:bb503a36bfb939e838fc45",
    "measurementId": "G-HZY3KJSGSL"
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()

sensing_enabled = True

# Create the main window
window = tkinter.Tk()
window.title("Login form")
window.geometry('800x600')
window.configure(bg='#333333')


def retrieve_and_display_live_data():
    aqi_value = database.child("sensor_data/AQI").get().val()
    eco2_value = database.child("sensor_data/ECO2").get().val()
    tvoc_value = database.child("sensor_data/TVOC").get().val()
    pm1_value = database.child("sensor_data/PMS1_0").get().val()
    pm2_value = database.child("sensor_data/PMS2_5").get().val()
    pm10_value = database.child("sensor_data/PMS10").get().val()
    moist_value = database.child("sensor_data/soil_moist").get().val()
    water_value = database.child("sensor_data/water_level").get().val()

    aqi_label.config(text=f"AQI: {aqi_value}")
    eco2_label.config(text=f"CO2: {eco2_value}")
    tvoc_label.config(text=f"TVOC: {tvoc_value}")
    pm1_label.config(text=f"PM1.0: {pm1_value}")
    pm2_label.config(text=f"PM2.5: {pm2_value}")
    pm10_label.config(text=f"PM10.0: {pm10_value}")
    moist_label.config(text=f"Moisture: {moist_value}")
    water_label.config(text=f"Water Level: {water_value}")

    window.after(1000, retrieve_and_display_live_data)


def pump_options():
    if pump_var.get() == 1:  # If "Automate" is selected
        messagebox.showinfo("Pump", "Pump will be operated automatically.")
        database.child("sensing/mode/").set("Automatic")
        # Remove the sensing button when in automatic mode
        sensing_button.grid_forget()
    elif pump_var.get() == 2:  # If "Manual" is selected
        messagebox.showinfo("Pump", "Pump will be operated manually.")
        database.child("sensing/mode/").set("Manual")
        # Show the sensing button
        sensing_button.grid(row=3, column=0, pady=10, padx=20)
    else:
        messagebox.showwarning("Pump", "Please select an option for the pump.")


def toggle_pump_options():
    if pump_frame.winfo_viewable():
        pump_frame.pack_forget()
    else:
        pump_frame.pack(pady=20)


def login():
    username = "techmates"
    password = "12345"
    if username_entry.get() == username and password_entry.get() == password:
        messagebox.showinfo(title="Login Success",
                            message="You successfully logged in.")
        create_main_page()
    else:
        messagebox.showerror(title="Error", message="Invalid login.")


def create_main_page():
    # Clear the login page
    frame.pack_forget()

    # Create a new frame for the main page
    global main_frame
    main_frame = tkinter.Frame(bg='#333333')

    # Create the three buttons
    previous_data_button = tkinter.Button(
        main_frame, text="Previous Data", bg="#FF3399", fg="#FFFFFF", font=("Arial", 20), width=30, command=previous_data)
    live_data_button = tkinter.Button(
        main_frame, text="Live Data", bg="#FF3399", fg="#FFFFFF", font=("Arial", 20), width=30, command=live_data)
    pump_button = tkinter.Button(
        main_frame, text="Pump", bg="#FF3399", fg="#FFFFFF", font=("Arial", 20), width=30, command=pump)

    # Placing buttons in the center vertically
    previous_data_button.grid(row=1, column=0, pady=20)
    live_data_button.grid(row=2, column=0, pady=20)
    pump_button.grid(row=3, column=0, pady=20)

    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_rowconfigure(3, weight=1)

    main_frame.pack(expand=True)


def previous_data():
    # Handle the "Previous Data" action
    pass


def live_data():
    # Hide the main frame and show the live data frame
    main_frame.pack_forget()
    open_live_data_page()


def open_live_data_page():
    global live_data_frame
    live_data_frame = tkinter.Frame(bg='#333333')

    # Create labels to display live data
    global aqi_label, eco2_label, tvoc_label, pm1_label, pm2_label, pm10_label, moist_label, water_label
    aqi_label = tkinter.Label(live_data_frame, text="AQI: Loading...",
                              bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    eco2_label = tkinter.Label(
        live_data_frame, text="CO2: Loading...", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    tvoc_label = tkinter.Label(
        live_data_frame, text="TVOC: Loading...", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    pm1_label = tkinter.Label(live_data_frame, text="PM1.0: Loading...",
                              bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    pm2_label = tkinter.Label(
        live_data_frame, text="PM2.5: Loading...", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    pm10_label = tkinter.Label(
        live_data_frame, text="PM10.0: Loading...", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    moist_label = tkinter.Label(live_data_frame, text="Moisture: Loading...",
                                bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    water_label = tkinter.Label(
        live_data_frame, text="Water Level: Loading...", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
    # Placing labels on the screen
    aqi_label.pack(pady=10)
    eco2_label.pack(pady=10)
    tvoc_label.pack(pady=10)
    pm1_label.pack(pady=10)
    pm2_label.pack(pady=10)
    pm10_label.pack(pady=10)
    moist_label.pack(pady=10)
    water_label.pack(pady=10)

    # Retrieve and display live data
    retrieve_and_display_live_data()

    # Button to close the live data page
    close_button = tkinter.Button(live_data_frame, text="Close", bg="#FF3399", fg="#FFFFFF", font=(
        "Arial", 16), command=close_live_data_page)
    close_button.pack(pady=20)

    # Configure row weights for vertical centering
    live_data_frame.grid_rowconfigure(0, weight=1)
    live_data_frame.grid_rowconfigure(9, weight=1)

    # Expand the frame to fill the available space
    live_data_frame.pack(expand=True)


def close_live_data_page():
    # Hide the live data frame and show the main frame
    live_data_frame.pack_forget()
    create_main_page()


def pump():
    main_frame.pack_forget()
    pump_data_page()


def pump_data_page():
    global pump_frame
    pump_frame = tkinter.Frame(bg='#333333')

    pump_label = tkinter.Label(pump_frame, text="Pump Options", font=(
        "Helvetica", 25, "bold"), bg="black", fg="white")

    pump_label.grid(row=0, columnspan=2, pady=10)  # Increased padding

    # Create radio buttons for pump options
    global pump_var
    pump_var = tkinter.IntVar()

    # Center-align and style radio buttons
    automate_radio = tkinter.Radiobutton(
        pump_frame, text="Automate", variable=pump_var, value=1, font=("Helvetica", 20), bg="black", fg="white")
    automate_radio.grid(row=1, column=0, pady=10, padx=20, sticky="w")

    manual_radio = tkinter.Radiobutton(
        pump_frame, text="Manual", variable=pump_var, value=2, font=("Helvetica", 20), bg="black", fg="white")
    manual_radio.grid(row=2, column=0, pady=10, padx=20, sticky="w")

    #sensing_enabled = True
    global sensing_button
    sensing_button = tkinter.Button(
        pump_frame, text="Pump: OFF", relief=tkinter.RAISED, command=toggle_data_sensing)

    # Create a button to handle pump options
    pump_button = tkinter.Button(
        pump_frame, text="Submit Pump Options", command=pump_options, font=("Helvetica", 20), bg="blue", fg="white")
    pump_button.grid(row=4, columnspan=2, pady=15)

    close_button1 = tkinter.Button(pump_frame, text="Close", bg="#FF3399", fg="#FFFFFF", font=(
        "Arial", 16), command=close_pump_data_page)
    close_button1.grid(row=5, pady=20)

    pump_frame.pack(expand=True)


def toggle_data_sensing():
    global sensing_enabled
    sensing_enabled = not sensing_enabled
    if sensing_enabled:
        sensing_button.config(text="Pump: ON", relief=tkinter.SUNKEN)
        database.child("sensing/pump/").set("on")
    else:
        sensing_button.config(text="Pump: OFF", relief=tkinter.RAISED)
        database.child("sensing/pump/").set("off")


def close_pump_data_page():
    # Hide the live data frame and show the main frame
    pump_frame.pack_forget()
    create_main_page()


# Create widgets for the login form
frame = tkinter.Frame(bg='#333333')

eco_label = tkinter.Label(
    frame, text="EcoBreathe", bg='#333333', fg="#FF3399", font=("Arial", 30))
page_label = tkinter.Label(
    frame, text="by Team TechMates", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
login_label = tkinter.Label(
    frame, text="Login to Proceed", bg='#333333', fg="#FF3399", font=("Arial", 30))
username_label = tkinter.Label(
    frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_entry = tkinter.Entry(frame, font=("Arial", 16))
password_entry = tkinter.Entry(frame, show="*", font=("Arial", 16))
password_label = tkinter.Label(
    frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
login_button = tkinter.Button(
    frame, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=login)

# Placing widgets on the screen
eco_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=10)
page_label.grid(row=1, column=0, columnspan=2, sticky="news", pady=10)
login_label.grid(row=2, column=0, columnspan=2, sticky="news", pady=20)
username_label.grid(row=3, column=0)
username_entry.grid(row=3, column=1, pady=20)
password_label.grid(row=4, column=0)
password_entry.grid(row=4, column=1, pady=20)
login_button.grid(row=5, column=0, columnspan=2, pady=30, sticky='n')

# Configure row weights for vertical centering
frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(6, weight=1)

frame.pack(expand=True)  # Expand the frame to fill the available space
window.mainloop()