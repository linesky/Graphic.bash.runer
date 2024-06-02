import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import subprocess
import shutil
import os

global replacess
replacess=""
class BareboneBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("copy structure")

        # Janela amarela
        self.root.configure(bg='yellow')

        # Área de texto
        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.pack(pady=10)
        self.text_area2 = tk.Text(self.root, height=10, width=50)
        self.text_area2.pack(pady=10)

        # Botões
        self.build_button = tk.Button(self.root, text="open", command=self.build_kernel)
        self.build_button.pack(pady=5)

        self.run_button = tk.Button(self.root, text="save", command=self.run_kernel)
        self.run_button.pack(pady=5)

        self.copy_button = tk.Button(self.root, text="find", command=self.copy_file)
        self.copy_button.pack(pady=5)
        self.copys_button = tk.Button(self.root, text="mount", command=self.copys_file)
        self.copys_button.pack(pady=5)
        self.text_area.delete(1.0, tk.END)
        self.text_area2.delete(1.0, tk.END)
        

    def execute_command(self, command,show:bool):
        try:
            
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
            if show:
                self.text_area.insert(tk.END, result)
            else:
                self.text_area2.insert(tk.END, result)
        except subprocess.CalledProcessError as e:
            if show:
                self.text_area.insert(tk.END,f"Error executing command:\n{e.output}")
            else:
                self.text_area2.insert(tk.END,f"Error executing command:\n{e.output}")
    def build_kernel(self):
        self.text_area2.delete(1.0, tk.END)
        filename = tk.filedialog.askopenfilename(title="Select file")
        f1=open(filename,"r")
        txts=f1.read()
        f1.close()
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, txts,True)
    
    def run_kernel(self):
        self.text_area2.delete(1.0, tk.END)
        filename = tk.filedialog.asksaveasfilename(title="Select file")
        txts=self.text_area.get("1.0", "end-1c")
        f1=open(filename,"w")
        f1.write(txts)
        f1.close()
        
    def copy_file(self):
        global replacess
        
        filename = tk.filedialog.askdirectory(title="Select folder to build")
        self.text_area.delete(1.0, tk.END)
        self.execute_command("find "+filename,True)
        
        replacess=filename

    def copys_file(self):
        global replacess
        ants=""
        ii:int=0
        self.execute_command("mkdir /tmp/dirs ",False)
        print(replacess)
        self.text_area2.delete(1.0, tk.END)
        txts=self.text_area.get("1.0", "end-1c")
        txts=txts.replace("\r","\n")
        txts=txts.replace("\n\n","\n")
        txts2=txts.split("\n")
        for tx1 in txts2:
            txts3=tx1.split(";")
            for tx2 in txts3:
                tx2=tx2.strip()
                if tx2!="":
                    
                   
                    if 0==0:   
                        tx22=tx2.replace(replacess,"")
                        trs=tx22.split("/")
                        mkdirs:str="/tmp/dirs"
                        for nn in range(len(trs)-1):
                            mkdirs=mkdirs+"/"+trs[nn]
                        if ants!=mkdirs and replacess!=tx2 and replacess+"/"!=tx2 and ii!=0:
                            self.execute_command("mkdir "+mkdirs,False)
                        ants=mkdirs
                    try:     
                        if replacess!=tx2:
                            
                            self.execute_command("cp "+tx2+" "+mkdirs,False)
                    except:
                        aa=0
                    ii=ii+1
        self.execute_command("nautilus --browser /tmp/dirs ",False)
if __name__ == "__main__":
    root = tk.Tk()
    builder = BareboneBuilder(root)
    root.mainloop()
