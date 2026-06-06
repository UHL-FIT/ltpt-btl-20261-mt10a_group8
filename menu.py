import csv
from tkinter import Label, StringVar, Toplevel, IntVar, filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import font as tkfont
from button import lam_moi_dinh_dang_bang
#file
def mofile(tree):
    filepath = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv"),("All files", "*.*")])
    if not filepath:
        return
    for item in tree.get_children():
        tree.delete(item)
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        first_row = next(reader, None)
        if first_row:
            if not ("Mã" in str(first_row[0]) or "Ma" in str(first_row[0])):
                tree.insert("", "end", values=first_row)
            for row in reader:
                tree.insert("", "end", values=row)
    lam_moi_dinh_dang_bang(tree)
    messagebox.showinfo("Thành công", "Đã nạp dữ liệu từ file và đồng bộ lưới bảng!")      
def luufile(tree,header,window):
    filepath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"),("All files", "*.*")])
    if not filepath:
        return
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        clean_headers = [h.strip() for h in header]
        writer.writerow(clean_headers)

        for item in tree.get_children():
            raw_row = list(tree.item(item)['values'])
            for idx in range(len(raw_row)):
                raw_row[idx] = str(raw_row[idx]).replace(",", "").replace(" VNĐ", "")
            writer.writerow(raw_row)
    lam_moi_dinh_dang_bang(tree)
    messagebox.showinfo("Thành công", "Đã lưu dữ liệu vào file!")
#edit
def suagiaodien(window, tree , header):
    settingwindow = Toplevel()
    settingwindow.title("Cài đặt giao diện")
    settingwindow.geometry("400x300")
    settingwindow.grab_set()
    style = ttk.Style(window)   
    ttk.Label(settingwindow, text="Chế độ giao diện:", font=("Segoe UI", 10)).grid(row=0, column=0, padx=15, pady=10, sticky="w")
    theme_var = StringVar(value="Light")   
    if style.theme_use() == "clam" and style.lookup(".", "background") == "#2d2d2d":
        theme_var.set("Dark")
    def toggle_theme():
        if theme_var.get() == "Light":
        #light
            style.theme_use("clam")
            style.configure(".", background="#f5f5f5", foreground="#000000", fieldbackground="#ffffff")
            style.configure("Treeview", background="#ffffff", foreground="#000000", fieldbackground="#ffffff")
            style.configure("Treeview.Heading", background="#e1e1e1", foreground="#000000")
            window.configure(bg="#f5f5f5")
        else:
        #dark
            style.theme_use("clam")
            style.configure(".", background="#2d2d2d", foreground="#ffffff", fieldbackground="#3d3d3d")
            style.configure("Treeview", background="#3d3d3d", foreground="#ffffff", fieldbackground="#3d3d3d")
            style.configure("Treeview.Heading", background="#4d4d4d", foreground="#ffffff")
            window.configure(bg="#2d2d2d") 
    theme_menu = ttk.Combobox(settingwindow, textvariable=theme_var, values=["Light", "Dark"], state="readonly", width=12)
    theme_menu.grid(row=0, column=1, padx=15, pady=10)
    theme_menu.bind("<<ComboboxSelected>>", lambda e: toggle_theme())


    Label(settingwindow, text="Phông chữ hiển thị:", font=("Segoe UI", 10)).grid(row=1, column=0, padx=15, pady=10, sticky="w")
    current_font = tkfont.Font(font=style.lookup("Treeview", "font"))
    
    font_family_var = StringVar(value=current_font.actual("family"))
    font_size_var = IntVar(value=current_font.actual("size"))
    def cap_nhat_font():
        f_family = font_family_var.get()
        f_size = font_size_var.get()
        style.configure(".", font=(f_family, f_size))
        style.configure("Treeview", font=(f_family, f_size), rowheight=f_size + 10)
        style.configure("Treeview.Heading", font=(f_family, f_size, "bold"))    
    font_menu = ttk.Combobox(settingwindow, textvariable=font_family_var, values=["Segoe UI", "Arial", "Times New Roman", "Courier New"], state="readonly", width=12)
    font_menu.grid(row=1, column=1, padx=15, pady=10)
    font_menu.bind("<<ComboboxSelected>>", lambda e: cap_nhat_font())
    Label(settingwindow, text="Kích thước chữ:", font=("Segoe UI", 10)).grid(row=2, column=0, padx=15, pady=10, sticky="w")
    size_spin = ttk.Spinbox(settingwindow, from_=8, to=24, textvariable=font_size_var, width=11, command=cap_nhat_font)
    size_spin.grid(row=2, column=1, padx=15, pady=10)
    size_spin.bind("<Return>", lambda e: cap_nhat_font())
def gioithieu():
    messagebox.showinfo("Giới thiệu", "Phần mềm quản lý nhân sự\nPhiên bản 1.0\nĐược phát triển bởi Nhóm 8\n Liên Hệ : 676767676767\n Phần mềm này được thiết kế để giúp quản lý thông tin nhân viên, tính lương và thống kê tăng trưởng một cách hiệu quả và dễ dàng sử dụng.")