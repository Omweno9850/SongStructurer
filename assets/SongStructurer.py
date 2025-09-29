import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import librosa
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pygame
import soundfile as sf
import time
import os
import sys
import csv
import tempfile

class AudioSegmentEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Audio Segment Editor with Progressbar, Transport Slider, and Timestamps")
        self.geometry("950x1050")

        pygame.mixer.init()
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.audio_path = None
        self.temp_wav_file = None

        self.playing = False
        self.current_segment_index = None
        self.segment_length = None
        self.updating_slider = False  # Flag to prevent recursion on slider updates

        # Progress bar and time label
        self.progress_var = tk.DoubleVar()
        self.progressbar = ttk.Progressbar(self, orient="horizontal", length=800, mode="determinate", variable=self.progress_var)
        self.progressbar.pack(pady=5)

        self.time_label = tk.Label(self, text="00:00 / 00:00")
        self.time_label.pack(pady=2)

        # Transport slider, interactive, scaled with zoomed segment
        self.position_slider = ttk.Scale(self, from_=0, to=1000, orient="horizontal", length=800, command=self.on_slider_change)
        self.position_slider.pack(pady=5)
        # Seek on slider release only
        self.position_slider.bind("<ButtonRelease-1>", self.on_slider_release)

        # Buttons
        self.btn_load = tk.Button(self, text="Carica file audio", command=self.load_audio)
        self.btn_load.pack(pady=3)

        self.btn_analyze = tk.Button(self, text="Analizza segmenti", command=self.analyze_segments, state=tk.DISABLED)
        self.btn_analyze.pack(pady=3)

        self.btn_play_segment = tk.Button(self, text="Ascolta segmento", command=self.play_segment, state=tk.DISABLED)
        self.btn_play_segment.pack(pady=3)

        self.btn_stop_segment = tk.Button(self, text="Ferma riproduzione", command=self.stop_playback, state=tk.DISABLED)
        self.btn_stop_segment.pack(pady=3)

        self.btn_rename_segment = tk.Button(self, text="Rinomina segmento", command=self.rename_segment, state=tk.DISABLED)
        self.btn_rename_segment.pack(pady=3)

        self.btn_merge_segments = tk.Button(self, text="Unisci segmenti selezionati", command=self.merge_selected_segments, state=tk.DISABLED)
        self.btn_merge_segments.pack(pady=3)

        export_frame = tk.Frame(self)
        export_frame.pack(pady=5)
        self.btn_export_csv = tk.Button(export_frame, text="Esporta segmenti CSV", command=self.export_csv, state=tk.DISABLED)
        self.btn_export_csv.pack(side=tk.LEFT, padx=5)
        self.btn_export_png = tk.Button(export_frame, text="Esporta immagine PNG", command=self.export_png, state=tk.DISABLED)
        self.btn_export_png.pack(side=tk.LEFT, padx=5)

        zoom_frame = tk.Frame(self)
        zoom_frame.pack(fill=tk.X, padx=10, pady=5)
        self.zoom_scale = tk.Scale(zoom_frame, from_=1, to=10000, orient=tk.HORIZONTAL, label="Zoom (%)", command=self.on_zoom_change)
        self.zoom_scale.set(100)
        self.zoom_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.zoom_entry = tk.Entry(zoom_frame, width=6)
        self.zoom_entry.pack(side=tk.LEFT)
        self.zoom_entry.insert(0, "100")
        self.zoom_entry.bind("<Return>", self.on_zoom_entry)

        scroll_frame = tk.Frame(self)
        scroll_frame.pack(fill=tk.X, padx=20)
        self.h_scroll = tk.Scrollbar(scroll_frame, orient=tk.HORIZONTAL, command=self.on_scroll)
        self.h_scroll.pack(fill=tk.X)

        self.btn_exit = tk.Button(self, text="Esci", command=self.on_exit)
        self.btn_exit.pack(pady=5)

        self.segments_listbox = tk.Listbox(self, height=10, selectmode=tk.EXTENDED)
        self.segments_listbox.pack(fill=tk.X, padx=20)
        self.segments_listbox.bind("<<ListboxSelect>>", self.on_segment_select)

        self.fig, self.ax = plt.subplots(figsize=(12, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(pady=10)

        self.audio = None
        self.sr = None
        self.decimated_audio = None
        self.decimation_factor = 100
        self.segments = []
        self.drag_idx = None
        self.dragging_edge = None
        self.selected_segment = None
        self.view_start = 0
        self.view_end = 1
        self.redraw_pending = False

        # playback cursor time (absolute seconds from start of file)
        self.play_cursor_time = None

        self.cid_press = self.canvas.mpl_connect('button_press_event', self.on_press)
        self.cid_release = self.canvas.mpl_connect('button_release_event', self.on_release)
        self.cid_motion = self.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def load_audio(self):
        path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3 *.wav *.flac")])
        if not path:
            return
        self.audio_path = path
        self.audio, self.sr = librosa.load(path, sr=None, mono=True)
        self.decimated_audio = self.decimate_audio(self.audio, self.decimation_factor)
        self.segments.clear()
        self.segments_listbox.delete(0, tk.END)
        self.view_start = 0
        self.view_end = len(self.audio) / self.sr
        self.zoom_scale.set(100)
        self.zoom_entry.delete(0, tk.END)
        self.zoom_entry.insert(0, "100")
        self.h_scroll.set(0.0, 1.0)
        self.draw_waveform()
        self.btn_analyze.config(state=tk.NORMAL)
        self.btn_play_segment.config(state=tk.DISABLED)
        self.btn_stop_segment.config(state=tk.DISABLED)
        self.btn_rename_segment.config(state=tk.DISABLED)
        self.btn_merge_segments.config(state=tk.DISABLED)
        self.btn_export_csv.config(state=tk.DISABLED)
        self.btn_export_png.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.progressbar['maximum'] = int(len(self.audio) / self.sr * 1000)
        self.time_label.config(text="00:00 / 00:00")
        self.position_slider.config(value=0, to=int(len(self.audio) / self.sr * 1000))

    def decimate_audio(self, audio, factor):
        if factor <= 1:
            return audio
        length = len(audio) // factor
        audio = audio[:length * factor]
        audio = audio.reshape(-1, factor)
        return audio.mean(axis=1)

    def analyze_segments(self):
        tempo, beats = librosa.beat.beat_track(y=self.audio, sr=self.sr)
        times = librosa.frames_to_time(beats, sr=self.sr)
        if times is None or len(times) < 2:
            messagebox.showerror("Errore", "Impossibile segmentare il brano automaticamente.")
            return
        min_seg_len = 8
        self.segments.clear()
        self.segments_listbox.delete(0, tk.END)
        start = times[0]
        for i in range(1, len(times)):
            if times[i] - start >= min_seg_len:
                label = f"segment_{len(self.segments)}"
                self.segments.append([start, times[i], label])
                self.segments_listbox.insert(tk.END, label)
                start = times[i]
        if start < times[-1]:
            label = f"segment_{len(self.segments)}"
            self.segments.append([start, times[-1], label])
            self.segments_listbox.insert(tk.END, label)
        self.draw_waveform()
        self.btn_play_segment.config(state=tk.NORMAL)
        self.btn_rename_segment.config(state=tk.NORMAL)
        self.btn_merge_segments.config(state=tk.NORMAL)
        self.btn_export_csv.config(state=tk.NORMAL)
        self.btn_export_png.config(state=tk.NORMAL)

    def draw_waveform(self):
        if self.redraw_pending:
            return
        self.redraw_pending = True
        self.after(20, self._perform_draw)

    def _perform_draw(self):
        self.redraw_pending = False
        self.ax.clear()
        if self.audio is None or self.decimated_audio is None:
            self.canvas.draw_idle()
            return
        total_len = len(self.audio) / self.sr
        times = np.linspace(0, total_len, len(self.decimated_audio))
        mask = (times >= self.view_start) & (times <= self.view_end)
        if not np.any(mask):
            self.canvas.draw_idle()
            return
        times_view = times[mask]
        audio_view = self.decimated_audio[mask]
        self.ax.plot(times_view, audio_view, color='black', alpha=0.6)
        for start, end, label in self.segments:
            if end < self.view_start or start > self.view_end:
                continue
            draw_start = max(start, self.view_start)
            draw_end = min(end, self.view_end)
            self.ax.axvspan(draw_start, draw_end, alpha=0.3, color='orange')
            self.ax.text((draw_start + draw_end) / 2, 0.7, label, ha='center', fontsize=8)
            if self.view_start <= start <= self.view_end:
                self.ax.axvline(start, color='blue', linewidth=2)
            if self.view_start <= end <= self.view_end:
                self.ax.axvline(end, color='blue', linewidth=2)
        # draw play cursor if playing
        if self.playing and self.play_cursor_time is not None:
            if self.view_start <= self.play_cursor_time <= self.view_end:
                self.ax.axvline(self.play_cursor_time, color='red', linewidth=1.5)
        self.ax.set_xlim(self.view_start, self.view_end)
        self.canvas.draw_idle()

    def play_segment(self):
        if self.selected_segment is None:
            messagebox.showinfo("Info", "Seleziona un segmento dalla lista.")
            return
        if self.playing:
            self.stop_playback()
        self.current_segment_index = self.selected_segment
        start, end, _ = self.segments[self.selected_segment]
        segment_audio = self.audio[int(start * self.sr):int(end * self.sr)]

        if self.temp_wav_file is not None and os.path.exists(self.temp_wav_file):
            try:
                os.remove(self.temp_wav_file)
            except Exception:
                pass

        # write temporary WAV in 16-bit PCM which pygame handles well
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tf:
            self.temp_wav_file = tf.name
            # soundfile will write floats unless subtype specified; use PCM_16
            sf.write(self.temp_wav_file, segment_audio, self.sr, subtype='PCM_16')

        try:
            pygame.mixer.music.load(self.temp_wav_file)
        except Exception as e:
            messagebox.showerror("Errore riproduzione", f"Impossibile caricare il segmento audio:\n{e}")
            return
        pygame.mixer.music.play()
        self.segment_length = end - start
        self.play_start_time = time.time()  # real-world time when playback started
        self.segment_start_in_file = start  # absolute time in file where segment begins
        self.playing = True
        self.progress_var.set(0)
        self.position_slider.config(value=0, to=int(self.segment_length * 1000))
        self.time_label.config(text="00:00 / " + self.format_time(self.segment_length))
        self.btn_stop_segment.config(state=tk.NORMAL)
        # initialize cursor
        self.play_cursor_time = self.segment_start_in_file
        self.update_progressbar()

    def update_progressbar(self):
        if not self.playing:
            return
        pos_ms = pygame.mixer.music.get_pos()
        if pos_ms == -1:
            # playback finished
            self.stop_playback()
            return
        current_sec = pos_ms / 1000.0
        self.progress_var.set(pos_ms)
        self.time_label.config(text=f"{self.format_time(current_sec)} / {self.format_time(self.segment_length)}")

        # update play cursor absolute time
        self.play_cursor_time = self.segment_start_in_file + current_sec
        # update slider if not being actively changed programmatically
        if not self.updating_slider:
            # slider in milliseconds relative to segment start
            self.position_slider.set(int(current_sec * 1000))

        # redraw waveform to show moving cursor (lightweight)
        self.draw_waveform()

        self.after(50, self.update_progressbar)

    def on_slider_change(self, value):
        # do not trigger seeking continuously; only update label/time while dragging
        try:
            ms = int(float(value))
        except Exception:
            return
        # show provisional time while dragging
        if self.segment_length is not None:
            self.time_label.config(text=f"{self.format_time(ms/1000.0)} / {self.format_time(self.segment_length)}")

    def on_slider_release(self, event):
        # Seek to chosen position only on release
        if not self.playing or self.current_segment_index is None:
            # if not playing, just set slider position value (no playback)
            return
        try:
            pos_ms = int(float(self.position_slider.get()))
        except Exception:
            return
        # stop current playback and restart from new position within temp file
        # pygame.mixer.music.rewind() then set_pos via play(start=...) is not guaranteed across builds.
        # Instead stop and play, and rely on "start" param if available; if not, accept small limitation.
        try:
            pygame.mixer.music.stop()
            # attempt to use start parameter; may raise TypeError on some pygame versions
            pygame.mixer.music.play(start=pos_ms / 1000.0)
        except TypeError:
            # fallback: restart from beginning and skip updating pos (some pygame builds don't support start)
            pygame.mixer.music.play()
            # set internal play_start_time offset so cursor matches requested seek
            # we emulate by adjusting play_start_time backwards so get_pos shows correct relative time
            # but since get_pos returns from actual audio playback start, we can't fully emulate seeking without start support
            pass
        # update internal tracking
        self.play_start_time = time.time() - (pos_ms / 1000.0)
        self.play_cursor_time = self.segment_start_in_file + (pos_ms / 1000.0)
        self.progress_var.set(pos_ms)
        self.time_label.config(text=f"{self.format_time(pos_ms / 1000.0)} / {self.format_time(self.segment_length)}")

    def stop_playback(self):
        if self.playing:
            pygame.mixer.music.stop()
        self.playing = False
        self.current_segment_index = None
        self.segment_length = None
        self.progress_var.set(0)
        self.time_label.config(text="00:00 / 00:00")
        self.position_slider.set(0)
        self.btn_stop_segment.config(state=tk.DISABLED)
        self.play_cursor_time = None
        self.draw_waveform()

    def rename_segment(self):
        if self.selected_segment is None:
            messagebox.showinfo("Info", "Seleziona un segmento dalla lista")
            return
        new_label = simpledialog.askstring("Rinomina segmento", "Inserisci nuova etichetta:")
        if new_label:
            self.segments[self.selected_segment][2] = new_label
            self.segments_listbox.delete(self.selected_segment)
            self.segments_listbox.insert(self.selected_segment, new_label)
            self.draw_waveform()

    def merge_selected_segments(self):
        selected = self.segments_listbox.curselection()
        if len(selected) < 2:
            messagebox.showinfo("Info", "Seleziona almeno due segmenti da unire.")
            return
        indices = sorted(selected)
        start = self.segments[indices[0]][0]
        end = self.segments[indices[-1]][1]
        label = simpledialog.askstring("Unisci segmenti", "Inserisci etichetta per il segmento unito:")
        if not label:
            label = f"segment_{indices[0]}"
        for i in reversed(indices):
            self.segments.pop(i)
            self.segments_listbox.delete(i)
        self.segments.insert(indices[0], [start, end, label])
        self.segments_listbox.insert(indices[0], label)
        self.draw_waveform()

    def export_csv(self):
        if not self.segments:
            messagebox.showinfo("Info", "Nessun segmento da esportare.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            with open(path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Start", "End", "Label"])
                for start, end, label in self.segments:
                    writer.writerow([self.format_time(start), self.format_time(end), label])
            messagebox.showinfo("Esporta CSV", "Esportazione completata.")
        except Exception as e:
            messagebox.showerror("Errore export CSV", str(e))

    def export_png(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG image", "*.png")])
        if not path:
            return
        try:
            old_start, old_end = self.view_start, self.view_end
            self.view_start = 0
            self.view_end = len(self.audio) / self.sr
            self._perform_draw()
            self.fig.savefig(path)
            messagebox.showinfo("Esporta PNG", "Esportazione immagine completata.")
            self.view_start, self.view_end = old_start, old_end
            self._perform_draw()
        except Exception as e:
            messagebox.showerror("Errore export PNG", str(e))

    def format_time(self, seconds):
        m = int(seconds // 60)
        s = int(seconds % 60)
        return f"{m:02}:{s:02}"

    def on_press(self, event):
        if event.xdata is None or event.ydata is None:
            return
        for i, (start, end, _) in enumerate(self.segments):
            if abs(event.xdata - start) < 0.05:
                self.drag_idx = i
                self.dragging_edge = 'start'
                return
            if abs(event.xdata - end) < 0.05:
                self.drag_idx = i
                self.dragging_edge = 'end'
                return

    def on_motion(self, event):
        if self.drag_idx is None or event.xdata is None:
            return
        if self.dragging_edge == 'start':
            new_start = max(0, min(event.xdata, self.segments[self.drag_idx][1] - 0.01))
            if self.drag_idx > 0 and new_start <= self.segments[self.drag_idx - 1][1]:
                new_start = self.segments[self.drag_idx - 1][1] + 0.01
            self.segments[self.drag_idx][0] = new_start
        elif self.dragging_edge == 'end':
            new_end = min(event.xdata, len(self.audio) / self.sr)
            if self.drag_idx < len(self.segments) - 1 and new_end >= self.segments[self.drag_idx + 1][0]:
                new_end = self.segments[self.drag_idx + 1][0] - 0.01
            if new_end > self.segments[self.drag_idx][0]:
                self.segments[self.drag_idx][1] = new_end
        self.draw_waveform()

    def on_release(self, event):
        self.drag_idx = None
        self.dragging_edge = None
        self.draw_waveform()

    def on_zoom_change(self, val):
        try:
            zoom_pct = int(val)
        except Exception:
            return
        self.zoom_entry.delete(0, tk.END)
        self.zoom_entry.insert(0, str(zoom_pct))
        self.apply_zoom(zoom_pct)
        # Update slider max if playing segment
        if self.playing and self.current_segment_index is not None:
            segment_start, segment_end, _ = self.segments[self.current_segment_index]
            visible_len = min(self.view_end - self.view_start, segment_end - segment_start)
            self.position_slider.config(to=int(visible_len * 1000))

    def on_zoom_entry(self, event):
        try:
            zoom_pct = int(self.zoom_entry.get())
        except Exception:
            messagebox.showerror("Errore", "Valore zoom non valido")
            return
        if zoom_pct < 1:
            zoom_pct = 1
        if zoom_pct > 10000:
            zoom_pct = 10000
        self.zoom_scale.set(zoom_pct)
        self.apply_zoom(zoom_pct)
        if self.playing and self.current_segment_index is not None:
            segment_start, segment_end, _ = self.segments[self.current_segment_index]
            visible_len = min(self.view_end - self.view_start, segment_end - segment_start)
            self.position_slider.config(to=int(visible_len * 1000))

    def apply_zoom(self, zoom_pct):
        if self.audio is None or self.audio.size == 0:
            return
        total_len = len(self.audio) / self.sr
        display_len = total_len * 100 / zoom_pct
        if display_len < 0.1:
            display_len = 0.1
        center = (self.view_start + self.view_end) / 2
        new_start = max(0, center - display_len / 2)
        new_end = min(total_len, center + display_len / 2)
        self.view_start = new_start
        self.view_end = new_end
        self.h_scroll.set(new_start / total_len, new_end / total_len)
        self.draw_waveform()

    def on_scroll(self, *args):
        if self.audio is None or self.audio.size == 0:
            return
        total_len = len(self.audio) / self.sr
        if args[0] == 'moveto':
            pos = float(args[1])
            display_len = self.view_end - self.view_start
            new_start = pos * total_len
            if new_start + display_len > total_len:
                new_start = total_len - display_len
            if new_start < 0:
                new_start = 0
            self.view_start = new_start
            self.view_end = new_start + display_len
            self.h_scroll.set(self.view_start / total_len, self.view_end / total_len)
            self.draw_waveform()

    def on_segment_select(self, event):
        sel = self.segments_listbox.curselection()
        if not sel:
            self.selected_segment = None
            self.btn_merge_segments.config(state="disabled")
            self.btn_play_segment.config(state="disabled")
            self.btn_stop_segment.config(state="disabled")
            self.btn_rename_segment.config(state="disabled")
            return
        self.selected_segment = sel[0]
        self.btn_play_segment.config(state="normal")
        self.btn_stop_segment.config(state="normal")
        self.btn_rename_segment.config(state="normal")
        self.btn_merge_segments.config(state="normal" if len(sel) > 1 else "disabled")

    def on_exit(self):
        self.stop_playback()
        if hasattr(self, 'cursor_after_id') and self.cursor_after_id is not None:
            self.after_cancel(self.cursor_after_id)
            self.cursor_after_id = None
        if self.temp_wav_file is not None and os.path.exists(self.temp_wav_file):
            try:
                os.remove(self.temp_wav_file)
            except Exception:
                pass
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = AudioSegmentEditor()
    app.mainloop()
