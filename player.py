from tkinter import *
from tkinter import filedialog
import pygame
import time

root = Tk()

root.title("MP3 Player")
root.geometry("500x400")

# Initialize pygame
pygame.mixer.init()

# Create a function to deal with time
def play_time():
	# Grab current song time
	current_time = pygame.mixer.music.get_pos() / 1000
	# Convert song time to time format
	converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
	# Add current time to status bar
	status_bar.config(text=f'Time Elapsed: {converted_current_time}')
	# Create loop to check the time every second
	status_bar.after(1000, play_time)

# Create Function To Add One Song To Playlist
def add_song():
	song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
	#my_label.config(text=song)
	# strip out directory structure and .mp3 from song title
	song = song.replace("C:/mp3/audio/", "")
	song = song.replace(".mp3", "")
	# add to end of playlist
	playlist_box.insert(END, song)
	
# Create function to add many songs to playlist
def add_many_songs():
	songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
	
	# Loop through song list and replace directory structure and mp3 from song name
	for song in songs:
		# strip out directory structure and .mp3 from song title
		song = song.replace("C:/mp3/audio/", "")
		song = song.replace(".mp3", "")
		# add to end of playlist
		playlist_box.insert(END, song)

# Create function to delete one song from playlist
def delete_song():
	# Delete highlighted song from playlist
	playlist_box.delete(ANCHOR)

# Create function to delete all songs from playlist
def delete_all_songs():
	# Delete all songs from playlist
	playlist_box.delete(0, END)

# Create play function
def play():
	# Reconstruct song with directory structure stuff
	song = playlist_box.get(ACTIVE)
	song = f'C:/mp3/audio/{song}.mp3'
	
	# Load song with pygame mixer
	pygame.mixer.music.load(song)
	# Play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	# Get song time
	play_time()

# Create stop function
def stop():
	# Stop the song
	pygame.mixer.music.stop()
	# Clear playlist bar
	playlist_box.selection_clear(ACTIVE)

# Create function to play the next song
def next_song():
	# Get current song number
	next_one = playlist_box.curselection() 
	# Add one to the current song number tuple/list
	next_one = next_one[0] + 1

	# Grab the song title from the playlist
	song = playlist_box.get(next_one)
	# Add directory structure stuff to tht song title
	song = f'C:/mp3/audio/{song}.mp3'
	# Load song with pygame mixer
	pygame.mixer.music.load(song)
	# Play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	# Clear active bar in playlist
	playlist_box.selection_clear(0, END)

	# Move active bar to next song
	playlist_box.activate(next_one)

	# Set active bar to next song
	playlist_box.selection_set(next_one, last=None)


# Create function to play previous song
def previous_song():
	# Get current song number
	next_one = playlist_box.curselection() 
	# Minus one from the current song number tuple/list
	next_one = next_one[0] - 1

	# Grab the song title from the playlist
	song = playlist_box.get(next_one)
	# Add directory structure stuff to tht song title
	song = f'C:/mp3/audio/{song}.mp3'
	# Load song with pygame mixer
	pygame.mixer.music.load(song)
	# Play song with pygame mixer
	pygame.mixer.music.play(loops=0)

	# Clear active bar in playlist
	playlist_box.selection_clear(0, END)

	# Move active bar to next song
	playlist_box.activate(next_one)

	# Set active bar to next song
	playlist_box.selection_set(next_one, last=None)


# Create paused variable
global paused
paused = False

# Create pause function
def pause(is_paused):
	global paused
	paused = is_paused

	if paused:
		# Unpause
		pygame.mixer.music.unpause()
		paused = False
	else:
		pygame.mixer.music.pause()
		paused = True


# Create Playlist Box
playlist_box = Listbox(root, bg="black", fg="green", width=60, selectbackground="green", selectforeground="white")
playlist_box.pack(pady=20)

# Define Button Images For Controls
back_btn_img = PhotoImage(file='images/back.png')
forward_btn_img = PhotoImage(file='images/forward.png')
play_btn_img = PhotoImage(file='images/play.png')
pause_btn_img = PhotoImage(file='images/pause.png')
stop_btn_img = PhotoImage(file='images/stop.png')

# Create Button Frame
control_frame = Frame(root)
control_frame.pack(pady=20)

# Create Play/Stop etc.. Buttons
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

# Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

# Create Add Song Menu Dropdown
add_song_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
# Add One Song To Playlist
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)
# Add Many Songs To Playlist
add_song_menu.add_command(label="Add Many Songs To Playlist", command=add_many_songs)

# Create delete song menu dropdowns
remove_song_menu =Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Song From Playlist", command=delete_all_songs)

# Create status bar
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Temporary Label
my_label = Label(root, text='')
my_label.pack(pady=20)


root.mainloop()