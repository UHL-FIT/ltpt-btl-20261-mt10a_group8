from tkinter import messagebox


def tinh(entries):
    try:
        def layso(s):
            chuoi= entries[s].get().strip()
            if not chuoi:
                return 0
            return int(chuoi)
        luongcb      = layso(0)
        phucapcv     = layso(1) 
        tiencom      = layso(3)
        tangca       = layso(4) 
        nghi_khong_phep = layso(5)
        nghi_co_phep = layso(6) 

        tong_nghi = nghi_khong_phep +nghi_co_phep

        if tong_nghi >30:
            messagebox.showerror("lỗi", "Tổng số ngày nghỉ (có phép và không phép) không thể vượt quá 30 ngày!")
            return None
        
        if tong_nghi>3:
            chuyencan_thuc =0

            entries[2].delete(0, "end")
            entries[2].insert(0, "0")
        else: 
            chuyencan_thuc = layso(2)
            chuyencan_thuc = 200000
            entries[2].delete(0,"end")
            entries[2].insert(0,"200000")

        tong_luong= (luongcb + phucapcv + chuyencan_thuc + (tiencom* 10000)+ (tangca *100000)-(nghi_co_phep*100000+nghi_khong_phep*200000))
        return tong_luong
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ cho tất cả các trường.")
        return None