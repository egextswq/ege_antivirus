import tkinter as tk
from tkinter import filedialog, messagebox
import scanner
import updater

def start_scan():
    folder = filedialog.askdirectory()
    if not folder:
        return

    text.delete("1.0", tk.END)
    text.insert(tk.END, f"Taranıyor: {folder}\n\n")

    infected_files = scanner.scan_folder(folder, lambda f: text.insert(tk.END, f"BULUNDU: {f}\n"))

    if infected_files:
        if messagebox.askyesno("Virüs Bulundu!", f"{len(infected_files)} dosya bulundu. Karantinaya alalım mı?"):
            scanner.quarantine(infected_files)
            text.insert(tk.END, "\nKarantinaya alındı.\n")
    else:
        text.insert(tk.END, "\nTemiz! Virüs bulunamadı.\n")

def update_signatures():
    updater.update_signatures()
    messagebox.showinfo("Güncelleme", "Virüs veritabanı güncellendi.")

def restore_files():
    restored = scanner.restore_from_quarantine()
    messagebox.showinfo("Kurtarılan Dosyalar", f"{restored} dosya geri yüklendi.")
    text.insert(tk.END, f"\n{restored} dosya geri yüklendi.\n")

app = tk.Tk()
app.title("Ege Antivirus")

frame = tk.Frame(app, padx=10, pady=10)
frame.pack()

tk.Button(frame, text="Klasör Tara", command=start_scan, width=30).pack(pady=5)
tk.Button(frame, text="Veritabanını Güncelle", command=update_signatures, width=30).pack(pady=5)
tk.Button(frame, text="Karantinadan Geri Yükle", command=restore_files, width=30).pack(pady=5)

text = tk.Text(frame, height=20, width=60)
text.pack()

app.mainloop()
