import tkinter as tk
from tkinter import filedialog, messagebox
from latex_docx import fix_docx


def do_open():
    path = filedialog.askopenfilename(
        title='Select a DOCX file',
        filetypes=[('Word Documents', '*.docx')],
    )
    if not path:
        return

    status_label.config(text='Processing...', fg='#333333')
    root.update()

    try:
        out_path, count = fix_docx(path)
        if count > 0:
            status_label.config(
                text=f'Done \u2014 {count} expression{"s" if count != 1 else ""} converted',
                fg='#1b5e20',
            )
        else:
            status_label.config(text='No LaTeX expressions found', fg='#795548')
            messagebox.showinfo(
                'No Math Found',
                'No LaTeX expressions ($...$ or $$...$$) were found.',
            )
    except Exception as e:
        status_label.config(text=f'Error: {e}', fg='#b71c1c')
        messagebox.showerror('Error', str(e))


root = tk.Tk()
root.title('LaTeX to DOCX Converter')
root.geometry('420x140')
root.resizable(False, False)

frame = tk.Frame(root, padx=24, pady=20)
frame.pack(fill=tk.BOTH, expand=True)

btn = tk.Button(
    frame,
    text='Open DOCX',
    command=do_open,
    width=20,
    height=2,
    font=('Segoe UI', 10, 'bold'),
    bg='#1565c0',
    fg='white',
    relief=tk.RAISED,
    cursor='hand2',
)
btn.pack(pady=(0, 12))

status_label = tk.Label(
    frame,
    text='Select a .docx file to fix LaTeX math',
    font=('Segoe UI', 10),
    fg='#555555',
)
status_label.pack()

root.mainloop()
