import tkinter as tk
import webbrowser
from os import walk
from pathlib import Path
from tkinter import *
from pytube import Search
from pytube import YouTube
import getpass


CURRENT_USER = getpass.getuser()
downloads_path = (str(Path.home() / "Downloads").replace("\\", "/") + '/')
liste_fichiers = []
is_auto_play_on = True
downloaded_movies = set()  # Utiliser un ensemble pour stocker les noms des films déjà téléchargés
opened_videos = set()  # Utiliser un ensemble pour stocker les vidéos déjà ouvertes sur YouTube


class Application(tk.Tk):
    def __init__(self):
        super().__init__()  # Appel du constructeur de la classe parente (Tk)
        self.creer_widgets()

    def files_management(self):
        test = self.path_entry.get()
        for (repertoire, sousRepertoires, fichiers) in walk(test):
            liste_fichiers.extend(fichiers)
            print(liste_fichiers)
            print(self.path_entry.get())

            break
        else:
            print("Le chemin n'existe pas ou n'est pas bien indiqué")

    def download(self):
        for fichier in liste_fichiers:
            # Vérifie si le fichier est un fichier vidéo
            if any(ext in fichier for ext in ['.mp4', '.avi', '.mkv', '.mov', '.webm', '.mpeg']):
                film_name = fichier[:15]  # Extrait le nom du film à partir du nom du fichier (15 premiers caractères)
                if not self.is_movie_downloaded(film_name):
                    video_url = self.get_video_url(film_name)
                    if video_url:
                        if is_auto_play_on:
                            self.open_video(video_url)
                        else:
                            self.download_video(video_url, self.path_entry2.get())
                        downloaded_movies.add(film_name)  # Ajouter le film à l'ensemble des téléchargements

    def is_movie_downloaded(self, film_name):
        return film_name in downloaded_movies

    def get_video_url(self, film_name):
        s = Search(film_name + " Bande d'annonce VF")
        try:
            new = str((s.results[0]))
        except IndexError:
            print(f"Aucune bande-annonce trouvée pour {film_name}.")
            return None
        with open('assets/stats.txt', 'r+') as files:
            files.write(new + '\n')
        with open('assets/stats.txt', 'r+') as files:
            ouverture = (files.readline(52).split('Id='))
            video_id = ouverture[+1]
        return f"https://www.youtube.com/watch?v={video_id}"

    def open_video(self, video_url):
        webbrowser.open(video_url)

    def download_video(self, video_url, download_path):
        try:
            yt = YouTube(video_url)
            yt.streams \
                .filter(progressive=True, file_extension='mp4') \
                .order_by('resolution') \
                .desc() \
                .first() \
                .download(download_path)
        except pytube.exceptions.AgeRestrictedError:
            print(f"La vidéo pour {film_name} est restreinte en raison de l'âge. Ignorer et passer au suivant.")
            return

    def creer_widgets(self):
        background_image = PhotoImage(file="assets/Trailer2.png")
        self.background = Label(self, image=background_image)
        self.background.photo = background_image
        self.background.place(x=-16, y=0)

        self.my_label = Label(self,
                              text="Ouvrir les bandes d'annonces via Youtube",
                              fg="green", bg='white',
                              font=("Arial", 15))

        self.my_label.place(x=200, y=150)

        # Image du switch
        self.on = tk.PhotoImage(file="assets/on.png")
        self.off = tk.PhotoImage(file="assets/off.png")

        # Button switch
        self.on_button = tk.Button(self, image=self.on, bd=0,
                                   command=self.switch, bg='WHITE', activebackground='WHITE')
        self.on_button.place(x=80, y=130)

        # Entry the path
        self.path_entry = tk.Entry(self, width=40)
        self.path_entry.insert(END, downloads_path)
        self.path_entry.configure(font=('Arial', 15))
        self.path_entry.place(x=100, y=270)

        self.path_entry2 = tk.Entry(self, width=40)
        self.path_entry2.insert(END, downloads_path + 'Trailer ')
        self.path_entry2.configure(font=('Arial', 15))
        self.path_entry2.place(x=100, y=380)

        # Button Start
        self.Start_image = PhotoImage(file='assets/Button.png')
        self.Button_start = tk.Button(self, command=self.start,
                                      image=self.Start_image, borderwidth=0, bg='WHITE',
                                      activebackground='WHITE')
        self.Button_start.place(x=210, y=450)

    def switch(self):
        global is_auto_play_on
        # Determine si le switch est sur ON ou OFF
        if is_auto_play_on:
            self.on_button.config(image=self.off)
            self.my_label.config(text="Ne pas ouvrir les bandes d'annonces via Youtube",
                                 fg="grey")
            is_auto_play_on = False
        else:
            self.on_button.config(image=self.on)
            self.my_label.config(text="Ouvrir les bandes d'annonces via Youtube", fg="green")
            is_auto_play_on = True

    def start(self):
        self.files_management()
        self.download()


def main():
    app = Application()
    app.title("Trailer Downloader")
    app.geometry('720x630')
    app.resizable(False, False)
    app.iconbitmap('assets/trailer.ico')

    app.mainloop()


if __name__ == '__main__':
    main()
