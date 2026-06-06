from tkinter import *
from tkinter import ttk
def setup_ui(window, header):
    frame = Frame(window)
    frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

    scrolly = Scrollbar(frame, orient=VERTICAL)
    scrollx = Scrollbar(frame, orient=HORIZONTAL)

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview.Heading", 
                    background="#d4ece9",     
                    foreground="#4a5568",     
                    font=("Segoe UI", 9, "bold"),
                    borderwidth=1,
                    relief="solid")
    style.map("Treeview.Heading",background=[('active','#bee3db')])
    style.configure("Treeview", 
                    rowheight=24,         
                    font=("Segoe UI", 9),
                    background="white",
                    fieldbackground="white",
                    foreground="#4a5568",
                    gridlinecolor="#e2e8f0",
                    cellborderwidth=1,
                    borderwidth=1,
                    relief="solid") 
    style.element_create("Custom.Treeview.cell", "from", "default")
    style.layout("Treeview.Item", [
        ('Treeview.padding', {
            'sticky': 'nswe', 
            'children': [
                ('Treeview.background', {'sticky': 'nswe'}),
                ('Custom.Treeview.cell', {
                    'sticky': 'nswe',
                    'children': [
                        ('Treeview.label', {'sticky': 'nswe', 'side': 'left'})
                    ]
                })
            ]
        })
    ])
    style.configure("Treeview", cellborderwidth=1, relief="solid")
    style.map("Treeview", 
              background=[('selected', '#cce3ff0')], 
              foreground=[('selected', '#2d3748')])
    
    tree = ttk.Treeview(frame,
                        columns=header,
                        show="headings",
                        style ="Treeview",
                        yscrollcommand=scrolly.set,
                        xscrollcommand=scrollx.set)
    
    

    scrolly.config(command=tree.yview)
    scrollx.config(command=tree.xview)

    tree.grid(row=0, column=0, sticky="nsew")
    scrolly.grid(row=0, column=1, sticky="ns")
    scrollx.grid(row=1, column=0, sticky="ew")

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    tree.tag_configure('oddrow', background="#fbf2f2")
    tree.tag_configure('evenrow', background="#f7f9fa")
 

    for col in header:
        tree.heading(col, text=col) 
        tree.column(col, width=80,minwidth=50, anchor=CENTER)          
    return tree