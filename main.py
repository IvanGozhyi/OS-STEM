import tkinter as tk
from tkinter import ttk
import multiprocessing
import psutil
import os
from workers import cpu_worker, mem_worker, io_worker


class OsBenchmarkerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OS Performance Benchmarker")
        self.root.geometry("600x520")

        # State variables
        self.is_monitoring = False
        self.cpu_processes = []
        self.mem_process = None
        self.io_process = None

        # Safe initialization of disk counters
        io_counters = psutil.disk_io_counters()
        self.last_disk = io_counters.write_bytes if io_counters else 0

        self.init_ui()

    def init_ui(self):
        # Monitor Frame (Top)
        mon_frame = ttk.LabelFrame(self.root, text="Наочний перегляд (Телеметрія)", padding=10)
        mon_frame.pack(fill="x", padx=10, pady=10)

        self.lbl_cpu = ttk.Label(mon_frame, text="CPU: 0%", font=("Arial", 14))
        self.lbl_cpu.pack(anchor="w", pady=2)

        self.lbl_ram = ttk.Label(mon_frame, text="Вільна RAM: 0 MB", font=("Arial", 14))
        self.lbl_ram.pack(anchor="w", pady=2)

        self.lbl_io = ttk.Label(mon_frame, text="Запис на диск: 0.00 MB/s", font=("Arial", 14))
        self.lbl_io.pack(anchor="w", pady=2)

        # Button 1: Simple Monitor
        self.btn_monitor = ttk.Button(mon_frame, text="▶ Запустити простий перегляд (Монітор)",
                                      command=self.toggle_monitor)
        self.btn_monitor.pack(pady=10)

        # Workers Frame (Bottom)
        work_frame = ttk.LabelFrame(self.root, text="Керування навантаженням (Воркери)", padding=10)
        work_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # CPU Sub-frame
        cpu_frame = ttk.LabelFrame(work_frame, text="Керування CPU", padding=5)
        cpu_frame.pack(fill="x", pady=5)

        max_cores = multiprocessing.cpu_count()

        # Текстова мітка з кількістю потоків
        self.lbl_cpu_count = ttk.Label(cpu_frame, text=f"Кількість потоків: {max_cores}", font=("Arial", 10, "bold"))
        self.lbl_cpu_count.pack(anchor="w", pady=2)

        # Слайдер із прив'язкою до колбеку on_slider_change
        self.cpu_slider = ttk.Scale(
            cpu_frame,
            from_=1,
            to=max_cores,
            orient="horizontal",
            command=self.on_slider_change
        )
        self.cpu_slider.set(max_cores)
        self.cpu_slider.pack(fill="x", pady=2)

        self.btn_cpu = ttk.Button(cpu_frame, text="Навантажити CPU (Вимкнено)", command=self.toggle_cpu)
        self.btn_cpu.pack(fill="x", pady=5)

        # Memory & Disk Buttons
        self.btn_mem = ttk.Button(work_frame, text="Навантажити RAM (Вимкнено)", command=self.toggle_mem)
        self.btn_mem.pack(fill="x", pady=5)

        self.btn_io = ttk.Button(work_frame, text="Навантажити Диск (Вимкнено)", command=self.toggle_io)
        self.btn_io.pack(fill="x", pady=5)

    def on_slider_change(self, val):
        count = int(float(val))
        self.lbl_cpu_count.config(text=f"Кількість потоків: {count}")

    def toggle_monitor(self):
        if not self.is_monitoring:
            self.is_monitoring = True
            self.btn_monitor.config(text="⏹ Зупинити монітор")
            self.update_telemetry()
        else:
            self.is_monitoring = False
            self.btn_monitor.config(text="▶ Запустити простий перегляд (Монітор)")

    def update_telemetry(self):
        if not self.is_monitoring:
            return

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().available / (1024 * 1024)

        io_counters = psutil.disk_io_counters()
        curr_disk = io_counters.write_bytes if io_counters else 0
        disk_mb_s = (curr_disk - self.last_disk) / (1024 * 1024)
        self.last_disk = curr_disk

        self.lbl_cpu.config(text=f"CPU: {cpu:.1f}%")
        self.lbl_ram.config(text=f"Вільна RAM: {ram:.0f} MB")
        self.lbl_io.config(text=f"Запис на диск: {disk_mb_s:.2f} MB/s")

        # Schedule next UI update in 1000ms
        self.root.after(1000, self.update_telemetry)

    def toggle_cpu(self):
        if not self.cpu_processes:
            cores = int(self.cpu_slider.get())
            for _ in range(cores):
                p = multiprocessing.Process(target=cpu_worker, daemon=True)
                p.start()
                self.cpu_processes.append(p)
            self.btn_cpu.config(text=f"Навантажити CPU ({cores} потоків) (УВІМКНЕНО)")
        else:
            for p in self.cpu_processes:
                p.terminate()
            self.cpu_processes = []
            self.btn_cpu.config(text="Навантажити CPU (Вимкнено)")

    def toggle_mem(self):
        if self.mem_process is None:
            self.mem_process = multiprocessing.Process(target=mem_worker, daemon=True)
            self.mem_process.start()
            self.btn_mem.config(text="Навантажити RAM (УВІМКНЕНО)")
        else:
            self.mem_process.terminate()
            self.mem_process = None
            self.btn_mem.config(text="Навантажити RAM (Вимкнено)")

    def toggle_io(self):
        if self.io_process is None:
            self.io_process = multiprocessing.Process(target=io_worker, daemon=True)
            self.io_process.start()
            self.btn_io.config(text="Навантажити Диск (УВІМКНЕНО)")
        else:
            self.io_process.terminate()
            self.io_process = None
            self.btn_io.config(text="Навантажити Диск (Вимкнено)")


if __name__ == '__main__':
    # Required for Windows multiprocessing safety
    multiprocessing.freeze_support()
    root = tk.Tk()
    app = OsBenchmarkerApp(root)
    root.mainloop()