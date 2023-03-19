import customtkinter as ctk
from random import *
import time
from PIL import Image, ImageTk
import webbrowser
import pystray
import concurrent.futures
import threading
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class App:

	def __init__(self, master):
		self.master = master
		master.title("EYE PROTECTOR")
		master.geometry("600x440")
		master.resizable(width=False, height=False)

		# Create a title label and place it in the GUI
		title_label = ctk.CTkLabel(master, text="EYE PROTECTOR",font=('Century Gothic',24))
		title_label.place(x=200, y=20)
		
		# Create the input message
		screen_message_entry = ctk.CTkEntry(master, font=('Century Gothic',20,'bold'), width=520,height=150)
		screen_message_entry.place(x=50, y=80)
		screen_message_entry.insert(0,"EYE CARE")  # set default value

		# creat the input reminder time
		ontime_label = ctk.CTkLabel(master, font=('Century Gothic', 14), text="Give Reminder in:")
		ontime_label.place(x=50, y=250)

		ontime_entry = ctk.CTkComboBox(master, font=('Century Gothic', 14),
							   values=["5 Minutes", "10 Minutes", "30 Minutes", "1 Hour", "2 Hours", "24 Hours"] ,
							   state="readonly")
		ontime_entry.set("5 Minutes")
		ontime_entry.place(x=300, y=250)

		# Creat reminder time
		offtime_label = ctk.CTkLabel(master,font=('Century Gothic',14), text="Rest Time:")
		offtime_label.place(x=50, y=280)
		offtime_entry = ctk.CTkComboBox(root, font=('Century Gothic', 14),
									values=["30 Seconds", "60 Seconds", "2 Minutes", "5 Minutes"],
									state="readonly")
		offtime_entry.set("30 Seconds")
		offtime_entry.place(x=300, y=280)

		def get_varibles():
				global ontime_sec
				global offtime_sec
				global screen_message
				global isProgramRunning

				isProgramRunning=True
				screen_message =screen_message_entry.get()
				ontime =ontime_entry.get()
				offtime=offtime_entry.get()

				if ontime == "5 Minutes":
					ontime_sec = 30
				elif ontime == "10 Minutes":
					ontime_sec = 10 * 60
				elif ontime == "30 Minutes":
					ontime_sec = 30 * 60
				elif ontime == "1 Hour":
					ontime_sec = 60 * 60
				elif ontime == "2 Hours":
					ontime_sec = 2 * 60 * 60
				elif ontime == "24 Hours":
					ontime_sec = 24 * 60 * 60

				if offtime == "30 Seconds":
					offtime_sec = 30
				elif offtime == "60 Seconds":
					offtime_sec = 60
				elif offtime == "2 Minutes":
					offtime_sec = 2 * 60
				elif offtime == "5 Minutes":
					offtime_sec = 5 * 60

				if(isProgramRunning):
					self.open_window()
		
		# Create a button to open the second window
		self.open_button = ctk.CTkButton(master, text="START EYE PROTECTOR ", command=get_varibles)
		# self.open_button.place()
		self.open_button.place(x=210 ,y=320)

		# Create a button to close the second window
		self.close_button = ctk.CTkButton(master, text="STOP EYE PROTECTOR", command=self.close_window)
		# self.close_button.pack()
		self.close_button.place(x=210 ,y=350)
		self.top = None

		#Creat Donate button
		donate_btn = ctk.CTkButton(master, width=100, text="Donate", command=self.donate, corner_radius=6,font=('Century Gothic',14))
		donate_btn.place(x=50, y=400)
   
	def donate():
		webbrowser.open("https://www.buymeacoffee.com/siriuscodz")
	def close_window(self):
		if self.root is not None:
			global isProgramRunning
			# Close the window and reset variables
			isProgramRunning=False
			self.close_button.configure(state="disabled")
			self.open_button.configure(state="enable")
			
			#self.close_button.configure(state="enable")
			#self.root.destroy()
			#self.root = None

	def open_window(self):
		if not(isProgramRunning):
			return
		self.open_button.configure(state="disabled")
		self.close_button.configure(state="enable")

		# Create the window
		self.root = ctk.CTk()
		self.root.attributes("-fullscreen", True)

		# Set up canvas
		canvas = ctk.CTkCanvas(self.root, bg="#1e293b", highlightthickness=0)
		canvas.pack(expand=True, fill="both")

		# Set up screen dimensions
		screenWidth = canvas.winfo_screenwidth()
		screenHeight = canvas.winfo_screenheight()

		# Create background image
		try:
			background = ImageTk.PhotoImage(Image.open("background.jpg"))
			canvas.create_image((0, 0), image=background, anchor="nw")
		except:
			pass

		# Create rectangle and text
		width = 400
		height = 220
		x_coords = randint(0, screenWidth - width)
		y_coords = randint(0, screenHeight - height)
		x_speed = randint(40, 50)
		y_speed = randint(40, 50)
		x1 = x_coords
		y1 = y_coords
		x2 = x_coords + width
		y2 = y_coords + height
		rectangle = canvas.create_rectangle((x1, y1), (x2, y2), fill='#FFFFFF', outline='#FFFFFF')
		text = canvas.create_text((x_coords + width / 2, y_coords + height / 2), text=screen_message,
								fill="#333333", font=('Century Gothic', 12))

		last_update_time = time.monotonic()
		time_open = 0

		def moveRectAndText():
			#self.close_button.configure(state="enable")
			nonlocal x_coords, y_coords, x_speed, y_speed, last_update_time, time_open

			current_time = time.monotonic()
			time_diff = current_time - last_update_time
			last_update_time = current_time

			if x_coords > screenWidth - width or x_coords < 0:
				x_speed = -x_speed
			if y_coords > screenHeight - height or y_coords < 0:
				y_speed = -y_speed

			x_coords += x_speed * time_diff
			y_coords += y_speed * time_diff
			canvas.move(rectangle, x_speed * time_diff, y_speed * time_diff)
			canvas.move(text, x_speed * time_diff, y_speed * time_diff)

			time_open += time_diff
			if time_open >= offtime_sec:
				close_child_window()

			self.root.after(1, moveRectAndText)


		self.root.after(1, moveRectAndText)

		def close_child_window():
			global isProgramRunning
			self.root.destroy()
			if isProgramRunning:
				print(isProgramRunning)
				self.root.after((ontime_sec+offtime_sec)*1000, self.open_window)
			else:
				print(isProgramRunning)
		def donate():
			webbrowser.open("https://www.buymeacoffee.com/siriuscodz")


		# Create close button
		close_button = ctk.CTkButton(self.root, width=100, text="X", fg_color="red", corner_radius=6, font=('Century Gothic',20,'bold'),command=close_child_window)
		close_button.place(x=1000, y=0)

		# Create donate button
		donate_btn = ctk.CTkButton(self.root, width=100, text="Donate", corner_radius=6, font=('Century Gothic',14),command=donate)
		donate_btn.place(x=900, y=0)
		
		self.root.mainloop()

	def on_quit(self,icon, item):
		self.master.destroy()
		icon.stop()

	def on_show(self,icon, item):
		icon.stop()
		root.update()
		root.deiconify()

	def start_tray_loop(self,icon):
		icon.run()
	
	def minimize_main_window(self):
		# Minimize the main window instead of closing it
		root.withdraw()  # hide the main window
		#self.master.iconify()
		image = Image.open("icon.png")
		menu = pystray.Menu(pystray.MenuItem("Show", self.on_show), pystray.MenuItem("Quit", self.on_quit))
		icon = pystray.Icon("My App", image, menu=menu)
		tray_thread = threading.Thread(target=self.start_tray_loop, args=(icon,))
		tray_thread.start()
		
		

root = ctk.CTk()
app = App(root)

# Handle "WM_DELETE_WINDOW" protocol for main window

root.protocol("WM_DELETE_WINDOW", app.minimize_main_window)
root.mainloop()
