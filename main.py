import cv2
import tkinter as tk
from tkinter import ttk, simpledialog
from tkinter.filedialog import askopenfilename, askdirectory
import os
from threading import Thread
import time

def format_time(seconds):
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return f"{int(days)}:{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def get_video_stats(video_path):
    # Ouvrir la vidéo
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps  # Durée en secondes
    width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    file_size = os.path.getsize(video_path) / (1024 * 1024)  # Taille en Mo
    vidcap.release()

    return fps, total_frames, duration, width, height, file_size

def extract_frames(video_path, output_folder, frame_name, progress_bar, label, time_label):
    # Ouvrir la vidéo
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    total_frames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    count = 0
    success, image = vidcap.read()

    start_time = time.time()  # Temps de début
    
    while success:
        # Sauvegarder chaque frame avec le nom personnalisé
        frame_filename = os.path.join(output_folder, f"{frame_name}_{count:06d}.jpg")
        cv2.imwrite(frame_filename, image)
        count += 1
        success, image = vidcap.read()

        # Mise à jour de la barre de progression
        progress_bar['value'] = (count / total_frames) * 100
        progress_bar.update()

        # Mettre à jour le timer
        elapsed_time = time.time() - start_time
        time_label.config(text=f"Temps écoulé: {format_time(elapsed_time)}")
    
    vidcap.release()
    
    # Temps total de l'extraction
    total_time = time.time() - start_time
    time_label.config(text=f"Extraction terminée en {format_time(total_time)}")

def start_extraction():
    # Sélection de la vidéo
    video_path = askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
    if not video_path:
        return

    # Sélection de l'emplacement de sauvegarde
    output_folder = askdirectory(title="Choisissez le dossier de sauvegarde")
    if not output_folder:
        return
    
    # Demande du nom des frames
    frame_name = simpledialog.askstring("Nom des frames", "Entrez le nom des frames (ex: frame)")
    if not frame_name:
        return

    # Récupérer les stats de la vidéo
    fps, total_frames, duration, width, height, file_size = get_video_stats(video_path)
    label.config(text=f"FPS: {fps}, Frames: {total_frames}, Durée: {format_time(duration)}, Résolution: {width}x{height}, Taille: {file_size:.2f} Mo")
    
    # Lancer le traitement dans un thread séparé
    Thread(target=extract_frames, args=(video_path, output_folder, frame_name, progress_bar, label, time_label)).start()

# Interface graphique
root = tk.Tk()
root.title("Extracteur de Frames Vidéo")

label = tk.Label(root, text="Sélectionnez une vidéo")
label.pack(pady=10)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=20)

time_label = tk.Label(root, text="Temps écoulé: 00:00:00")
time_label.pack(pady=10)

button = tk.Button(root, text="Choisir une vidéo", command=start_extraction)
button.pack(pady=10)

root.mainloop()
