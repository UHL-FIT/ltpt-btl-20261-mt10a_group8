import sqlite3
import os

# Quy nhất về một file database để tránh phân mảnh dữ liệu
DB_NAME = "quanlynhansu.db"

def tao():
    """Khởi tạo cấu trúc các bảng nếu chưa tồn tại trong hệ thống"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # 1. Tạo bảng thông tin hồ sơ gốc của nhân viên
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nhan_vien (
            ma_nv TEXT PRIMARY KEY,
            ten_nv TEXT NOT NULL,
            gioi_tinh TEXT NOT NULL,
            trinh_do TEXT NOT NULL,
            chuc_vu TEXT NOT NULL,
            phong_ban TEXT NOT NULL,
            ngay_sinh TEXT NOT NULL,
            ngay_vao_lam TEXT NOT NULL
        )
    ''')
    
    # 2. Tạo bảng biến động lương theo từng tháng
    # Khóa chính bao gồm cả (ma_nv + thang_nam) để dùng được tính năng REPLACE
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bang_luong (
            ma_nv TEXT,
            thang_nam TEXT,
            luong_cb REAL NOT NULL,
            phu_cap_cv REAL NOT NULL,
            tien_chuyen_can REAL NOT NULL,
            suat_com REAL NOT NULL,
            tang_ca REAL NOT NULL,
            ngay_nghi REAL NOT NULL,
            ngay_nghi_co_phep REAL NOT NULL,
            tong_luong REAL NOT NULL,
            PRIMARY KEY (ma_nv, thang_nam),
            FOREIGN KEY (ma_nv) REFERENCES nhan_vien(ma_nv) ON DELETE CASCADE
        )
    ''')
    conn.commit()
    conn.close()

def themnvdb(data_list):
    """Thêm mới nhân viên vào danh sách hồ sơ gốc"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        # Cắt lấy đúng 8 thông tin cơ bản từ giao diện truyền xuống
        thong_tin_co_ban = list(data_list)[:8]
        
        cursor.execute('''
            INSERT INTO nhan_vien (ma_nv, ten_nv, gioi_tinh, trinh_do, chuc_vu, phong_ban, ngay_sinh, ngay_vao_lam)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', thong_tin_co_ban)
        
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("[DATABASE ERROR] Trùng mã nhân viên!")
        return False
    except Exception as e:
        print(f"[DATABASE ERROR] Lỗi khi thêm nhân viên: {e}")
        return False
    finally:
        conn.close()

def full():
    """Lấy toàn bộ danh sách nhân viên gốc (dự phòng)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nhan_vien")
    rows = cursor.fetchall()
    conn.close()
    return rows

def xoa(ma_nv):
    """Xóa nhân viên khỏi hệ thống (Tự động xóa sạch bảng lương liên quan nhờ CASCADE)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        # Bật tính năng khóa ngoại để kích hoạt lệnh CASCADE xóa tự động ở bảng lương
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute("DELETE FROM nhan_vien WHERE ma_nv = ?", (ma_nv,))
        conn.commit()
    except Exception as e:
        print(f"[DATABASE ERROR] Lỗi khi xóa: {e}")
    finally:
        conn.close()

def db_cap_nhat_nhan_vien(ma_nv_cu, data_list):
    """Cập nhật thông tin lý lịch nhân viên dựa trên mã cũ"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("PRAGMA foreign_keys = ON")
        
        ma_nv_moi    = data_list[0]
        ten_nv       = data_list[1]
        gioi_tinh    = data_list[2]
        trinh_do     = data_list[3]
        chuc_vu      = data_list[4]
        phong_ban    = data_list[5]
        ngay_sinh    = data_list[6]
        ngay_vao_lam = data_list[7]

        chuoi_update = [
            ma_nv_moi, ten_nv, gioi_tinh, trinh_do, chuc_vu, phong_ban, 
            ngay_sinh, ngay_vao_lam, ma_nv_cu
        ]
        
        cursor.execute('''
            UPDATE nhan_vien SET 
                ma_nv=?, ten_nv=?, gioi_tinh=?, trinh_do=?, chuc_vu=?, phong_ban=?, 
                ngay_sinh=?, ngay_vao_lam=?
            WHERE ma_nv = ?
        ''', chuoi_update)
        
        conn.commit()
        print(f"[DATABASE SUCCESS] Cập nhật thông tin thành công nhân viên {ma_nv_cu}")
    except Exception as e:
        print(f"[DATABASE ERROR] Lỗi khi cập nhật nhân viên: {e}")
    finally:
        conn.close()

def db_lay_bang_luong_theo_thang(thang_nam):
    """Truy vấn kết hợp lấy hồ sơ nhân viên và dữ liệu lương tương ứng theo tháng"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    query = """
        SELECT nv.ma_nv, nv.ten_nv, nv.gioi_tinh, nv.trinh_do, nv.chuc_vu, nv.phong_ban, nv.ngay_sinh, nv.ngay_vao_lam,
               bl.luong_cb, bl.phu_cap_cv, bl.tien_chuyen_can, bl.suat_com, bl.tang_ca, bl.ngay_nghi, bl.ngay_nghi_co_phep, bl.tong_luong
        FROM nhan_vien nv
        LEFT JOIN bang_luong bl ON nv.ma_nv = bl.ma_nv AND bl.thang_nam = ?
    """
    cursor.execute(query, (thang_nam,))
    rows = cursor.fetchall()
    conn.close()
    
    ket_qua = []
    for r in rows:
        row_list = list(r)
        for i in range(8, 16):
            if row_list[i] is None:
                row_list[i] = 0
        ket_qua.append(row_list)
    return ket_qua

def db_cap_nhat_luong(ma_nv, thang_nam, luong_cb, phu_cap_cv, tien_chuyen_can, suat_com, tang_ca, ngay_nghi, ngay_nghi_co_phep, tong_luong):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        query = """
            INSERT OR REPLACE INTO bang_luong 
            (ma_nv, thang_nam, luong_cb, phu_cap_cv, tien_chuyen_can, suat_com, tang_ca, ngay_nghi, ngay_nghi_co_phep, tong_luong)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (ma_nv, thang_nam, luong_cb, phu_cap_cv, tien_chuyen_can, suat_com, tang_ca, ngay_nghi, ngay_nghi_co_phep, tong_luong))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print("Lỗi lưu DB lương tháng:", e)
        return False
tao()