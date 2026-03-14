import tkinter as tk
from tkinter import filedialog, messagebox
import requests
import io

class FastenerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ISO Fastener Creator")
        self.api_url = "http://127.0.0.1:8080"

        # Screw Section
        tk.Label(root, text="SCREW", font=('Arial', 10, 'bold')).grid(row=0, column=0, pady=5)
        self.s_d = self.create_input("Diameter:", 1, 5)
        self.s_l = self.create_input("Length:", 2, 20)
        self.btn_screw = tk.Button(root, text="Save Screw", command=self.save_screw)
        self.btn_screw.grid(row=3, column=1, sticky="e", padx=5)

        # Washer Section
        tk.Label(root, text="WASHER", font=('Arial', 10, 'bold')).grid(row=4, column=0, pady=5)
        self.w_di = self.create_input("Inner D:", 5, 5.5)
        self.w_do = self.create_input("Outer D:", 6, 10)
        self.w_t = self.create_input("Thickness:", 7, 1)
        self.btn_washer = tk.Button(root, text="Save Washer", command=self.save_washer)
        self.btn_washer.grid(row=8, column=1, sticky="e", padx=5)

        # Assembly Section
        tk.Label(root, text="ASSEMBLY", font=('Arial', 10, 'bold')).grid(row=9, column=0, pady=10)
        self.btn_zip = tk.Button(root, text="Save Assembly (ZIP)", state="disabled", 
                                 command=self.save_zip, bg="#d1e7dd")
        self.btn_zip.grid(row=10, column=0, columnspan=2, pady=10, sticky="we", padx=10)

        for var in [self.s_d, self.s_l, self.w_di, self.w_do, self.w_t]:
            var.trace_add("write", self.toggle_assembly_button)

    def create_input(self, label, row, default):
        tk.Label(self.root, text=label).grid(row=row, column=0, sticky="w", padx=10)
        var = tk.StringVar(value=str(default))
        entry = tk.Entry(self.root, textvariable=var)
        entry.grid(row=row, column=1, padx=10)
        return var

    def toggle_assembly_button(self, *args):
        try:
            vals = [float(self.s_d.get()), float(self.w_di.get())]
            if all(vals) and float(self.w_di.get()) >= float(self.s_d.get()):
                self.btn_zip.config(state="normal")
            else:
                self.btn_zip.config(state="disabled")
        except:
            self.btn_zip.config(state="disabled")

    def save_file(self, endpoint, payload, default_name):
        path = filedialog.asksaveasfilename(defaultextension=".step", initialfile=default_name)
        if not path: return
        
        response = requests.post(f"{self.api_url}{endpoint}", json=payload)
        if response.status_code == 200:
            with open(path, "wb") as f:
                f.write(response.content)
            messagebox.showinfo("Success", "File saved successfully!")
        else:
            messagebox.showerror("Error", response.json().get("detail", "Unknown error"))

    def save_screw(self):
        payload = {"diameter": float(self.s_d.get()), "length": float(self.s_l.get())}
        self.save_file("/generate/screw", payload, "screw.step")

    def save_washer(self):
        payload = {"inner_diameter": float(self.w_di.get()), 
                   "outer_diameter": float(self.w_do.get()), "thickness": float(self.w_t.get())}
        self.save_file("/generate/washer", payload, "washer.step")

    def save_zip(self):
        path = filedialog.asksaveasfilename(defaultextension=".zip", initialfile="assembly.zip")
        if not path: return
        
        payload = {
            "screw": {"diameter": float(self.s_d.get()), "length": float(self.s_l.get())},
            "washer": {"inner_diameter": float(self.w_di.get()), 
                       "outer_diameter": float(self.w_do.get()), "thickness": float(self.w_t.get())}
        }
        response = requests.post(f"{self.api_url}/generate/assembly", json=payload)
        if response.status_code == 200:
            with open(path, "wb") as f:
                f.write(response.content)
            messagebox.showinfo("Success", "Assembly ZIP saved!")
        else:
            messagebox.showerror("Validation Failed", str(response.json()['detail']))

if __name__ == "__main__":
    root = tk.Tk()
    app = FastenerApp(root)
    root.mainloop()