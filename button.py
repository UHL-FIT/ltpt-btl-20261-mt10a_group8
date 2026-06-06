from datetime import datetime
import tkinter as tk
from tkinter import BOTH, BOTTOM, CENTER, LEFT, ttk, messagebox, Label, Entry, Button, Toplevel, END, Frame
from tinhtoan import tinh
from tkcalendar import DateEntry
from database import db_cap_nhat_luong, db_cap_nhat_nhan_vien, themnvdb, xoa    
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

bang_luong_cban = {
    "Giám đốc": ["50000000", "15000000"],
    "Trưởng ban": ["30000000", "8000000"],
    "Phó ban": ["22000000", "5000000"],
    "Chuyên viên": ["15000000", "2000000"],
    "Nhân viên": ["10000000", "1000000"],
    "Thực tập sinh": ["4000000", "0"],
}

def lam_moi_dinh_dang_bang(tree):
    for count, item in enumerate(tree.get_children()):
        row_list = list(tree.item(item)['values'])
        for idx in range(8, len(row_list)):
            try:
                val = row_list[idx]
                if val is not None and val != "":
                    clean_val = str(val).replace(",", "").replace(" VNĐ", "")
                    num_val = float(clean_val)
                    if num_val.is_integer():
                        row_list[idx] = f"{int(num_val):,}"
                    else:
                        row_list[idx] = f"{num_val:,.1f}"
            except ValueError:
                pass
        if count % 2 == 0:
            tree.item(item, values=row_list, tags=('evenrow',))
        else:
            tree.item(item, values=row_list, tags=('oddrow',))
           
def goi_y_tien_luong(event, cbo_chuc_vu, entry_luong_cb, entry_phu_cap_cv):
    ten_chuc_vu = cbo_chuc_vu.get()    
    if ten_chuc_vu in bang_luong_cban:
        entry_luong_cb.delete(0, tk.END)
        entry_luong_cb.insert(0, bang_luong_cban[ten_chuc_vu][0])
        
        entry_phu_cap_cv.delete(0, tk.END)
        entry_phu_cap_cv.insert(0, bang_luong_cban[ten_chuc_vu][1])

def luunv(entries, popup, tree):   
    try:    
        ma_nv = str(entries[0].get()).strip()
        ten_nv = str(entries[1].get()).strip()
    except Exception:    
        ma_nv = ""
        ten_nv = ""       
    if not ma_nv:
        messagebox.showerror("Lỗi dữ liệu", "Mã nhân viên là bắt buộc, không được để trống!")
        return
    if not ten_nv:
        messagebox.showerror("Lỗi dữ liệu", "Họ tên nhân viên là bắt buộc, không được để trống!")
        return
    data_moi = []
    for en in entries:
        if isinstance(en, tk.StringVar):
            data_moi.append(en.get())
        else:
            data_moi.append(en.get().strip())
    if not themnvdb(data_moi):
        messagebox.showerror("Thất bại", "Mã nhân viên này đã tồn tại trong hệ thống!")
        return
        
    tree.insert("", END, values=data_moi)
    lam_moi_dinh_dang_bang(tree)
    popup.destroy()
    messagebox.showinfo("Thành công", "Đã thêm nhân viên mới thành công!")

def themnv(parent_window, header, tree):
    themnhanvien = Toplevel(parent_window)
    themnhanvien.title("Thêm nhân viên mới")
    themnhanvien.geometry("1200x450")
    themnhanvien.configure(bg="#F8FAFC") 
    entries_dict = {}

    frame_ca_nhan = Frame(themnhanvien, bg="#EAF7F4", padx=10, pady=10, highlightbackground="#D4ECE9", highlightthickness=1)
    frame_ca_nhan.pack(fill="x", padx=15, pady=15)
    Label(frame_ca_nhan, text="THÔNG TIN CÁ NHÂN", font=("Segoe UI", 10, "bold"), fg="#4A5568", bg="#EAF7F4").grid(row=0, column=0, columnspan=10, sticky="w", pady=(0, 10))
    gioi_tinh_var = tk.StringVar(value="Nam")

    for i in range(6): 
        lbl = Label(frame_ca_nhan, text=header[i].strip() + ":", bg="#EAF7F4", fg="#4A5568")
        lbl.grid(row=1, column=i*2, padx=5, pady=5, sticky="e")

        if i == 2:
            frame_gioi_tinh = Frame(frame_ca_nhan, bg="#EAF7F4")
            frame_gioi_tinh.grid(row=1, column=i*2 + 1, padx=5, pady=5, sticky="w")
            rb_nam = tk.Radiobutton(frame_gioi_tinh, text="Nam", variable=gioi_tinh_var, value="Nam", bg="#EAF7F4", activebackground="#EAF7F4", fg="#4A5568")
            rb_nu = tk.Radiobutton(frame_gioi_tinh, text="Nữ", variable=gioi_tinh_var, value="Nữ", bg="#EAF7F4", activebackground="#EAF7F4", fg="#4A5568")
            rb_nam.pack(side=LEFT)
            rb_nu.pack(side=LEFT)
            entries_dict[i] = gioi_tinh_var
        elif i == 3:
            danh_sach_trinh_do = ["Trung Cấp", "Cao Đẳng", "Đại Học", "Sau Đại Học"]
            en = ttk.Combobox(frame_ca_nhan, values=danh_sach_trinh_do, state="readonly", width=13)
            en.current(0)
            en.grid(row=1, column=i*2 + 1, padx=5, pady=5, sticky="w")
            entries_dict[i] = en
        elif i == 4:
            danh_sach_chuc_vu = ["Giám đốc", "Trưởng ban", "Phó ban", "Chuyên viên", "Nhân viên", "Thực tập sinh"]  
            en = ttk.Combobox(frame_ca_nhan, values=danh_sach_chuc_vu, state="readonly", width=13) 
            en.current(4) 
            en.grid(row=1, column=i*2 + 1, padx=5, pady=5, sticky="w")
            entries_dict[i] = en
        elif i == 5:
            danh_sach_phong_ban = ["Ban Điều Khiển", "Ban Thông Tin", "Ban Huấn Luyện", "Ban Y Tế", "Ban Chỉ Huy Trung Tâm", "Ban Kỷ Luật", "Ban Phúc Lợi", "Ban Trích Xuất", "Ban Lưu Trữ", "Ban Kiến Trúc"]
            en = ttk.Combobox(frame_ca_nhan, values=danh_sach_phong_ban, state="readonly", width=13)
            en.current(0)
            en.grid(row=1, column=i*2 + 1, padx=5, pady=5, sticky="w")
            entries_dict[i] = en
        else:
            en = Entry(frame_ca_nhan, width=15, relief="flat", highlightbackground="#CBD5E1", highlightthickness=1)
            en.grid(row=1, column=i*2 + 1, padx=5, pady=5, sticky="w")
            entries_dict[i] = en

    for j in range(6, 8):
        lbl = Label(frame_ca_nhan, text=header[j].strip() + ":", bg="#EAF7F4", fg="#4A5568")
        lbl.grid(row=2, column=(j-6)*2, padx=5, pady=5, sticky="e")
        en = DateEntry(frame_ca_nhan, width=15, date_pattern='dd/mm/yyyy')
        en.grid(row=2, column=(j-6)*2 + 1, padx=5, pady=5, sticky="w")
        entries_dict[j] = en    
    entries = [entries_dict[key] for key in sorted(entries_dict.keys())]
    
    Button(themnhanvien, text="Lưu thông tin nhân viên", bg="#E2F5E9", fg="#2D3748", 
           activebackground="#C8E6C9", font=("Segoe UI", 10, "bold"), padx=25, pady=6, bd=0, relief="flat", cursor="hand2",
           command=lambda e=entries: luunv(e, themnhanvien, tree)).pack(pady=15)
def thuc_hien_cap_nhat(item_id, entries, popup, tree):
    try:
        ma_nv = entries[0].get().strip() if not isinstance(entries[0], tk.StringVar) else entries[0].get().strip()
        ten_nv = entries[1].get().strip() if not isinstance(entries[1], tk.StringVar) else entries[1].get().strip()
    except Exception:
        ma_nv = ""
        ten_nv = ""    

    if not ma_nv:
        messagebox.showerror("Lỗi dữ liệu", "Mã nhân viên là bắt buộc, không được để trống!")
        return
    if not ten_nv:
        messagebox.showerror("Lỗi dữ liệu", "Họ tên nhân viên là bắt buộc, không được để trống!")
        return
    data_cap_nhat = []
    for en in entries:
        if isinstance(en, tk.StringVar):
            data_cap_nhat.append(en.get())
        else:
            data_cap_nhat.append(en.get().strip())
    ma_nv_cu = tree.item(item_id)['values'][0]
    db_cap_nhat_nhan_vien(str(ma_nv_cu), data_cap_nhat)
    dong_cu = list(tree.item(item_id)['values'])
    cac_cot_luong_cu = dong_cu[8:] if len(dong_cu) > 8 else []
    tree.item(item_id, values=data_cap_nhat + cac_cot_luong_cu)
    lam_moi_dinh_dang_bang(tree)
    popup.destroy()
    messagebox.showinfo("Thành công", "Đã cập nhật thông tin nhân viên thành công!")   

def suanv(parent_window, tree, header): 
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên cần sửa trong bảng!")
        return
    item_id = selected_item[0]
    current_values = tree.item(item_id)['values']

    sua = Toplevel(parent_window)
    sua.geometry("1200x450")
    sua.title("Chỉnh sửa thông tin nhân viên")
    sua.configure(bg="#F8FAFC") 
    num_fields = len(header) - 1
    entries_dict = {}

    frame_ca_nhan = Frame(sua, bg="#EAF7F4", padx=10, pady=10, highlightbackground="#D4ECE9", highlightthickness=1)
    frame_ca_nhan.pack(fill="x", padx=15, pady=15)
    Label(frame_ca_nhan, text="THÔNG TIN CÁ NHÂN", font=("Segoe UI", 10, "bold"), fg="#4A5568", bg="#EAF7F4").grid(row=0, column=0, columnspan=10, sticky="w", pady=(0, 10))
   
    for i in range(6): 
        lbl = Label(frame_ca_nhan, text=header[i].strip() + ":", bg="#EAF7F4", fg="#4A5568")
        lbl.grid(row=1, column=i*2, padx=5, pady=5, sticky="e")
        if i == 2:
            val_gt = current_values[i] if i < len(current_values) else "Nam"
            gioi_tinh_var = tk.StringVar(value=str(val_gt).strip())
            frame_gioi_tinh = Frame(frame_ca_nhan, bg="#EAF7F4")
            frame_gioi_tinh.grid(row=1, column=i*2 + 1, padx=5, pady=5, sticky="w")
            rb_nam = tk.Radiobutton(frame_gioi_tinh, text="Nam", variable=gioi_tinh_var, value="Nam", bg="#EAF7F4", activebackground="#EAF7F4", fg="#4A5568")
            rb_nu = tk.Radiobutton(frame_gioi_tinh, text="Nữ", variable=gioi_tinh_var, value="Nữ", bg="#EAF7F4", activebackground="#EAF7F4", fg="#4A5568")
            rb_nam.pack(side=LEFT)
            rb_nu.pack(side=LEFT)
            entries_dict[i] = gioi_tinh_var
        elif i == 3:
            danh_sach_trinh_do = ["Trung Cấp", "Cao Đẳng", "Đại Học", "Sau Đại Học"]
            en = ttk.Combobox(frame_ca_nhan, values=danh_sach_trinh_do, state="readonly", width=13)
            if i < len(current_values) and current_values[i] in danh_sach_trinh_do:
                en.current(danh_sach_trinh_do.index(current_values[i]))
            else:
                en.current(0)
            en.grid(row=1, column=i*2 + 1, padx=5, pady=5, sticky="w")
            entries_dict[i] = en
        elif i == 4:
            danh_sach_chuc_vu = ["Giám đốc", "Trưởng ban", "Phó ban", "Chuyên viên", "Nhân viên", "Thực tập sinh"]
            en = ttk.Combobox(frame_ca_nhan, values=danh_sach_chuc_vu, state="readonly", width=13) 
            if i < len(current_values) and current_values[i] in danh_sach_chuc_vu:
                en.set(current_values[i])
            else:
                en.current(4)
            en.grid(row=1, column=i*2 + 1, padx=5, pady=5, sticky="w")
            entries_dict[i] = en
        elif i == 5:
            danh_sach_phong_ban = ["Ban Điều Khiển", "Ban Thông Tin", "Ban Huấn Luyện", "Ban Y Tế", "Ban Chỉ Huy Trung Tâm", "Ban Kỷ Luật", "Ban Phúc Lợi", "Ban Trích Xuất", "Ban Lưu Trữ", "Ban Kiến Trúc"]
            en = ttk.Combobox(frame_ca_nhan, values=danh_sach_phong_ban, state="readonly", width=13)
            if i < len(current_values):
                en.set(current_values[i])
            else:
                en.current(0)
            en.grid(row=1, column=i*2 + 1, padx=5, pady=5, sticky="w")
            entries_dict[i] = en
        else:       
            en = Entry(frame_ca_nhan, width=15, relief="flat", highlightbackground="#CBD5E1", highlightthickness=1)
            if i < len(current_values):
                clean_val = str(current_values[i]).replace(",", "")
                en.insert(0, clean_val)
            en.grid(row=1, column=i*2 + 1, padx=5, pady=5, sticky="w")
            entries_dict[i] = en       
        
    for j in range(6, 8):
        lbl = Label(frame_ca_nhan, text=header[j].strip() + ":", bg="#EAF7F4", fg="#4A5568")
        lbl.grid(row=2, column=(j-6)*2, padx=5, pady=5, sticky="e")
        en = DateEntry(frame_ca_nhan, width=15, date_pattern='dd/mm/yyyy')
        en.grid(row=2, column=(j-6)*2 + 1, padx=5, pady=5, sticky="w")
        if j < len(current_values):
            try:
                en.set_date(current_values[j])
            except:
                pass
        entries_dict[j] = en 
    entries = [entries_dict[key] for key in sorted(entries_dict.keys())]
    Button(sua, text="Lưu thay đổi", bg="#E3F2FD", fg="#2D3748", 
           activebackground="#BBDEFB", font=("Segoe UI", 10, "bold"), padx=25, pady=6, bd=0, relief="flat", cursor="hand2",
           command=lambda i=item_id, e=entries: thuc_hien_cap_nhat(i, e, sua, tree)).pack(pady=15) 
def luu_luong_thang_vao_db(ma_nv, thang_nam, entries_luong, popup, tree, item_id):
    tong_luong = tinh(entries_luong)
    if tong_luong is None:
        messagebox.showerror("Lỗi tính toán", "Không thể tính toán lương, vui lòng kiểm tra lại các ô nhập liệu!")
        return 
        
    try:
        luong_cb          = entries_luong[0].get().strip().replace(",", "")
        phu_cap_cv        = entries_luong[1].get().strip().replace(",", "")
        tien_chuyen_can   = entries_luong[2].get().strip().replace(",", "")
        suat_com          = entries_luong[3].get().strip().replace(",", "")
        tang_ca           = entries_luong[4].get().strip().replace(",", "")
        ngay_nghi_khong_phep= entries_luong[5].get().strip().replace(",", "")
        ngay_nghi_co_phep = entries_luong[6].get().strip().replace(",", "")
        
        ghi_thành_công = db_cap_nhat_luong(
            ma_nv, thang_nam, luong_cb, phu_cap_cv, tien_chuyen_can, 
            suat_com, tang_ca, ngay_nghi_khong_phep, ngay_nghi_co_phep, tong_luong
        )
        if ghi_thành_công:
            dong_hien_tai = list(tree.item(item_id)['values'])
            thong_tin_ca_nhan = dong_hien_tai[:8]
            du_lieu_luong_moi = [
                luong_cb, phu_cap_cv, tien_chuyen_can, suat_com, 
                tang_ca, ngay_nghi_khong_phep, ngay_nghi_co_phep, tong_luong
            ]
            tree.item(item_id, values=thong_tin_ca_nhan + du_lieu_luong_moi)
            lam_moi_dinh_dang_bang(tree)
            
            messagebox.showinfo("Thành công", 
                                f"Đã ghi nhận dữ liệu lương tháng {thang_nam} thành công!\n"
                                f"Tổng lương thực nhận: {tong_luong:,} VNĐ")
            popup.destroy()
        else:
            messagebox.showerror("Thất bại", "Lỗi kết nối cơ sở dữ liệu. Không thể lưu bảng lương!")
            
    except Exception as e:
        messagebox.showerror("Lỗi hệ thống", f"Đã xảy ra sự cố trong quá trình xử lý dữ liệu: {e}")

def luong(parent_window, tree, thang, nam):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân viên dưới bảng trước khi nhập lương!")
        return
    item_id = selected_item[0]
    item_values = tree.item(selected_item[0])['values']
    ma_nv = item_values[0]
    ten_nv = item_values[1]
    chuc_vu = item_values[4] 
    thang_nam_ky_nhan = f"{thang}/{nam}"
    
    popup_luong = Toplevel(parent_window)
    popup_luong.title(f"Nhập thông tin lương kỳ {thang_nam_ky_nhan}")
    popup_luong.geometry("460x540") 
    popup_luong.configure(bg="#F8FAFC")
    
    info_frame = Frame(popup_luong, bg="#FDF3F2", pady=10, padx=10,highlightbackground="#FCE4E4")
    info_frame.pack(fill="x")
    Label(info_frame, text=f"Nhân viên: {ten_nv} ({ma_nv}) — Chức vụ: {chuc_vu}", font=("Segoe UI", 9, "bold"), bg="#FDF3F2", fg="#E06666").pack()
    Label(info_frame, text=f"Áp dụng tính tiền cho kỳ lương tháng: {thang_nam_ky_nhan}", font=("Segoe UI", 9, "italic"), bg="#FDF3F2", fg="#718096").pack()
    
    form_frame = Frame(popup_luong, bg="#F8FAFC", pady=15)
    form_frame.pack(fill="both", expand=True, padx=30)
    
    labels_luong = [
        "Lương cơ bản (Tự động):",  
        "Phụ cấp CV (Tự động):",
        "Tiền Chuyên Cần (đ):", 
        "Số Suất Cơm Dùng:", 
        "Số buổi/giờ tăng ca:", 
        "Số ngày nghỉ không phép:",
        "Số ngày nghỉ có phép:"
    ]
    entries_luong = []
    for idx, text in enumerate(labels_luong):
        Label(form_frame, text=text, bg="#F8FAFC", fg="#4A5568", font=("Segoe UI", 9, "bold")).grid(row=idx, column=0, sticky="e", pady=8, padx=5)
        en = Entry(form_frame, width=22, relief="flat", highlightbackground="#CBD5E1", highlightthickness=1, font=("Segoe UI", 9))
        en.grid(row=idx, column=1, sticky="w", pady=8, padx=5)
        entries_luong.append(en)
    for idx in range(7):
        entry_o_nhap = entries_luong[idx]
        vi_tri_cot_treeview = 8 + idx
        if vi_tri_cot_treeview < len(item_values):
            gia_tri_goc = str(item_values[vi_tri_cot_treeview]).strip().replace(",", "")
            if gia_tri_goc and gia_tri_goc != "0" and gia_tri_goc != "0.0":
                entry_o_nhap.insert(0, gia_tri_goc)
                continue
        if idx == 0 and chuc_vu in bang_luong_cban: 
            entry_o_nhap.insert(0, bang_luong_cban[chuc_vu][0])
        elif idx == 1 and chuc_vu in bang_luong_cban:
            entry_o_nhap.insert(0, bang_luong_cban[chuc_vu][1])
        elif idx == 2:
            entry_o_nhap.insert(0,"200000")
        else:
            entry_o_nhap.insert(0, "0")
    entries_luong[0].config(state="readonly",readonlybackground="#E2E8F0")
    entries_luong[1].config(state="readonly",readonlybackground="#E2E8F0")

    Button(popup_luong, 
        text="Tính & Ghi Nhận Lương",
        font=("Segoe UI", 10, "bold"), 
        bg="#EAF7F4", 
        fg="#2D3748",
        activebackground="#D4ECE9",
        bd=0,
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=8,
        command=lambda m=ma_nv, t=thang_nam_ky_nhan, e=entries_luong: luu_luong_thang_vao_db(
            m, t, e, popup_luong, tree, item_id)).pack(pady=15)
def xoanv(tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Cảnh báo", "Chọn nhân viên cần xóa!")
        return
    confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa nhân viên này?")
    if confirm:
        item_id = selected_item[0]
        ma_nv = tree.item(item_id)['values'][0]
        xoa(ma_nv)
        tree.delete(item_id)
        lam_moi_dinh_dang_bang(tree)
        messagebox.showinfo("Thành công", "Đã xóa nhân viên khỏi hệ thống!")  

def timkiem(entry_ma_nv, tree):
    ma_nv = entry_ma_nv.get().strip()
    if not ma_nv:  
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập mã nhân viên để tìm kiếm!")
        return
    lam_moi_dinh_dang_bang(tree)
    tree.tag_configure("highlight", foreground="#2D3748", background="#D4ECE9", font=("Segoe UI", 10, "bold"))
    find = False
    for item in tree.get_children():
        if str(tree.item(item)['values'][0]) == ma_nv:
            tree.selection_set(item)
            tree.focus(item)
            tree.see(item)
            tree.item(item, tags=("highlight",))
            find = True
            break
    if not find:
        messagebox.showinfo("Kết quả", f"Không tìm thấy nhân viên với mã: {ma_nv}")
def thongke():
    import sqlite3
    try:
        conn = sqlite3.connect("quanlynhansu.db")
        query = "SELECT thang_nam, tong_luong FROM bang_luong"
        df = pd.read_sql_query(query, conn)
        conn.close()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể kết nối cơ sở dữ liệu để làm thống kê: {e}")
        return
    if df.empty:
        messagebox.showinfo("Thông báo", "Chưa có dữ liệu lương trong hệ thống để thực hiện thống kê!")
        return
    try:
        df['datetime'] = pd.to_datetime(df['thang_nam'], format='%m/%Y')
        df_thong_ke = df.groupby(['datetime', 'thang_nam']).agg(
            tong_quy_luong=('tong_luong', 'sum'),
            luong_trung_binh=('tong_luong', 'mean')
        ).reset_index()
        df_thong_ke = df_thong_ke.sort_values('datetime')
    except Exception as e:
        messagebox.showerror("Lỗi xử lý", f"Lỗi cấu trúc định dạng tháng năm: {e}")
        return
    popup_tk = Toplevel()
    popup_tk.title("Thống kê và Phân tích Quỹ lương giữa các tháng")
    popup_tk.geometry("900x600")
    popup_tk.configure(bg="#F8FAFC")
    lbl_title = Label(popup_tk, text="BIỂU ĐỒ TỔNG QUỸ LƯƠNG CHI TRẢ QUA CÁC THÁNG", 
                      font=("Segoe UI", 12, "bold"), bg="#F8FAFC", fg="#1E293B")
    lbl_title.pack(pady=(15, 5))
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
    bars = ax.bar(df_thong_ke['thang_nam'], df_thong_ke['tong_quy_luong'] / 1_000_000, 
                  color='#3B82F6', edgecolor='#2563EB', width=0.5, label='Quỹ lương (Triệu VNĐ)')
    ax.set_ylabel("Số tiền (Triệu VNĐ)", fontname="Segoe UI", fontsize=10, fontweight="bold")
    ax.set_xlabel("Kỳ lương (Tháng/Năm)", fontname="Segoe UI", fontsize=10, fontweight="bold")
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:,.1f} M',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # Đẩy chữ lên trên 3 điểm
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9, fontweight='bold', color='#1E293B')
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=popup_tk)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=BOTH, expand=True, padx=20, pady=10)
    canvas.draw()
    def on_close():
        plt.close(fig) 
        popup_tk.destroy()
    popup_tk.protocol("WM_DELETE_WINDOW", on_close)
    frame_summary = Frame(popup_tk, bg="#F1F5F9", padx=15, pady=10)
    frame_summary.pack(fill="x", padx=20, pady=(0, 20))
    
    thang_max = df_thong_ke.loc[df_thong_ke['tong_quy_luong'].idxmax()]['thang_nam']
    tien_max = df_thong_ke['tong_quy_luong'].max()
    
    lbl_summary = Label(frame_summary, 
                        text=f"Thống kê nhanh: Kỳ có tổng chi trả cao nhất là Tháng {thang_max} "
                             f"với số tiền: {int(tien_max):,} VNĐ.", 
                        font=("Segoe UI", 9, "italic"), bg="#F1F5F9", fg="#334155")
                        
    lbl_summary.pack(anchor="w")