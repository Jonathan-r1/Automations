import os
from PyPDF2 import PdfMerger
from tkinter import Tk, filedialog, Button, Label, Entry, messagebox

def merge_pdfs(pdf_list, output_file):
    merger = PdfMerger()

    for pdf in pdf_list:
        try:
            merger.append(pdf)
            print(f"Merged: {pdf}")
        except FileNotFoundError:
            print(f"File not found: {pdf}")
    
    with open(output_file, 'wb') as output_pdf:
        merger.write(output_pdf)
        print(f"Output PDF saved as {output_file}")
    
    merger.close()
    messagebox.showinfo("Success", f"PDFs merged and saved as {output_file}")

def select_files():
    files = filedialog.askopenfilenames(title="Select PDF Files", filetypes=[("PDF files", "*.pdf")])
    if files:
        pdf_list_label.config(text="\n".join(files))
        return list(files)
    return []

def save_file():
    file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file:
        return file
    return None

def merge_files():
    pdf_list = select_files()
    if pdf_list:
        output_file = save_file()
        if output_file:
            merge_pdfs(pdf_list, output_file)
        else:
            messagebox.showwarning("No output", "please specify a valid output file name.")
    else:
        messagebox.showwarning("no files selected", "please select pdf files to merge")

root = Tk()
root.title("PDF Merger")

select_button = Button(root, text="Select PDF files", command=select_files)
select_button.pack(pady=10)

pdf_list_label = Label(root, text="No files selected", wraplength=300, justify="left")
pdf_list_label.pack(pady=10)

merge_button = Button(root, text="Merge PDFs", command=merge_files)
merge_button.pack(pady=10)

# Run the GUI loop
root.mainloop()


