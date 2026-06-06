import datetime
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from menu import mofile, luufile, suagiaodien ,gioithieu
from tinhtoan import tinh
from button import  themnv, suanv, timkiem, xoanv, luong , thongke 
from datetime import datetime
from ui import setup_ui
from database import db_lay_bang_luong_theo_thang, full
window = Tk()
window.geometry("1300x700")

menubar = Menu(window)
window.config(menu=menubar)
frame_top = Frame(window)
frame_top.pack(fill="x", padx=15, pady=10)
Label(window, text="DANH SÁCH NHÂN VIÊN", font=("Times New Roman", 14, "bold")).pack(pady=10) 
frame_thoi_gian = LabelFrame(frame_top, text=" Kỳ tính lương hệ thống ", font=("Segoe UI", 9, "bold"), fg="#475569", labelanchor="n")
frame_thoi_gian.pack(side=RIGHT, padx=10)

Label(frame_thoi_gian, text="Tháng:", font=("Segoe UI", 9)).pack(side=LEFT, padx=(5, 2), pady=5)
cb_thang = ttk.Combobox(frame_thoi_gian, values=[f"{i:02d}" for i in range(1, 13)], width=5, state="readonly")
cb_thang.set(datetime.now().strftime("%m")) 
cb_thang.pack(side=LEFT, padx=5, pady=5)
Label(frame_thoi_gian, text="Năm:", font=("Segoe UI", 9)).pack(side=LEFT, padx=(5, 2), pady=5)
nam_hien_tai = datetime.now().year
cb_nam = ttk.Combobox(frame_thoi_gian, values=[str(year) for year in range(nam_hien_tai - 5, nam_hien_tai + 5)], width=6, state="readonly")
cb_nam.set(str(nam_hien_tai))
cb_nam.pack(side=LEFT, padx=5, pady=5)
header = [    "Mã NV" ,
              "Họ tên" ,
               "Giới tính" ,
               "Trình Độ", 
               "Chức Vụ", 
              "Phòng Ban" ,
              "Ngày sinh" ,
              "ngày vào làm" , 
              "Lương cơ bản" , 
              "Phụ Cấp Chức Vụ" ,
              "Chuyên Cần",
              "Số Suất Cơm" , 
              "Số buổi tăng ca",
              "số ngày nghỉ",
              "số ngày nghỉ có phép",
              "Tổng lương"]
data = []
tree = setup_ui(window,header)

filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open", command=lambda: mofile(tree))
filemenu.add_command(label="Save", command=lambda: luufile(window,tree, header))

editmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command(label="Edit", command=lambda: suagiaodien(window, tree , header))

helpmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Giới thiệu", command=lambda: gioithieu())

frame_tim_kiem = Frame(window)
frame_tim_kiem.pack(fill="x", padx=15, pady=5)
Button(frame_tim_kiem, text="tìm kiếm", command=lambda: timkiem(entry_ma_nv, tree)).pack(side=LEFT, padx=5, pady=10)
entry_ma_nv = Entry(frame_tim_kiem, width=20)
entry_ma_nv.pack(side=LEFT, padx=5, pady=5)

btn_frame = Frame(window)
btn_frame.pack(side=BOTTOM , fill=X, padx=10 ,pady=10)

Button(btn_frame, text="Thêm nhân viên", command=lambda: themnv(window,header,tree)).pack(side=LEFT, padx=5, pady=10) 
Button(btn_frame, text="Nhập lương tháng", command=lambda: luong(window, tree, cb_thang.get(), cb_nam.get())).pack(side=LEFT, padx=20)  
Button(btn_frame, text="Sửa nhân viên", command=lambda: suanv(window,tree,header)).pack(side=LEFT, padx=5, pady=10)   
Button(btn_frame, text="Xóa nhân viên", command=lambda: xoanv(tree)).pack(side=LEFT, padx=5, pady=10)
Button(btn_frame, text="Thống kê tăng trưởng", command=lambda: thongke()).pack(side=LEFT, padx=20)
Button(btn_frame, text="Thoát", command=window.quit).pack(side=LEFT, padx=5, pady=10)

def load_du_lieu_theo_thang(event=None):
    for item in tree.get_children():
        tree.delete(item)
    ky_luong_chon = f"{cb_thang.get()}/{cb_nam.get()}"
    
    try:
        count = 0
        du_lieu_tai_ve = db_lay_bang_luong_theo_thang(ky_luong_chon)
        
        for du_lieu_nv in du_lieu_tai_ve:
            row_list = list(du_lieu_nv)
            
         
            for idx in range(8, len(row_list)):
                try:
                    val = row_list[idx]
                    if val is not None and val != "":
                        num_val = float(val)
                        if num_val.is_integer():
                            row_list[idx] = f"{int(num_val):,}"
                        else:
                            row_list[idx] = f"{num_val:,.1f}"
                except ValueError:
                    pass
            if count % 2 == 0:
                tree.insert("", END, values=row_list, tags=('evenrow',))
            else:
                tree.insert("", END, values=row_list, tags=('oddrow',))
            count += 1         
    except Exception as e:
        print(f"Lỗi nạp database của kỳ {ky_luong_chon}:", e)
cb_thang.bind("<<ComboboxSelected>>", load_du_lieu_theo_thang)
cb_nam.bind("<<ComboboxSelected>>", load_du_lieu_theo_thang)
load_du_lieu_theo_thang()
window.mainloop()