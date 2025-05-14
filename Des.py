import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import base64

class DESApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Mã hóa/Giải mã DES")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Biến lưu trữ
        self.file_path = ""
        self.output_file = ""
        
        # Tạo giao diện
        self.create_widgets()
    
    def create_widgets(self):
        # Frame chính
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tiêu đề
        title_label = tk.Label(main_frame, text="CHƯƠNG TRÌNH MÃ HÓA VÀ GIẢI MÃ DES", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Chọn file
        file_label = tk.Label(main_frame, text="File đầu vào:", font=("Arial", 10))
        file_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.file_entry = tk.Entry(main_frame, width=40)
        self.file_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        browse_button = tk.Button(main_frame, text="Chọn file", command=self.browse_file)
        browse_button.grid(row=1, column=2, padx=5, pady=5)
        
        # Nhập khóa
        key_label = tk.Label(main_frame, text="Khóa (8 ký tự):", font=("Arial", 10))
        key_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.key_entry = tk.Entry(main_frame, width=40, show="*")
        self.key_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        show_key_button = tk.Button(main_frame, text="Hiện", command=self.toggle_key_visibility)
        show_key_button.grid(row=2, column=2, padx=5, pady=5)
        
        # Chọn chế độ
        mode_label = tk.Label(main_frame, text="Chế độ:", font=("Arial", 10))
        mode_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.mode = tk.StringVar()
        self.mode.set("encrypt")
        
        encrypt_radio = tk.Radiobutton(main_frame, text="Mã hóa", variable=self.mode, value="encrypt")
        encrypt_radio.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        decrypt_radio = tk.Radiobutton(main_frame, text="Giải mã", variable=self.mode, value="decrypt")
        decrypt_radio.grid(row=3, column=1, padx=100, sticky=tk.W, pady=5)
        
        # Nút thực hiện
        process_button = tk.Button(main_frame, text="Thực hiện", command=self.process_file, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15, height=1)
        process_button.grid(row=4, column=0, columnspan=3, pady=15)
        
        # Kết quả
        result_label = tk.Label(main_frame, text="Kết quả:", font=("Arial", 10))
        result_label.grid(row=5, column=0, sticky=tk.W, pady=5)
        
        self.result_entry = tk.Entry(main_frame, width=40)
        self.result_entry.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        download_button = tk.Button(main_frame, text="Tải xuống", command=self.download_file)
        download_button.grid(row=5, column=2, padx=5, pady=5)
        
        # Trạng thái
        self.status_label = tk.Label(main_frame, text="Trạng thái: Sẵn sàng", font=("Arial", 10), fg="blue")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=10, sticky=tk.W)
    
    def browse_file(self):
        """Mở hộp thoại chọn file"""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path = file_path
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)
    
    def toggle_key_visibility(self):
        """Hiện/ẩn mật khẩu"""
        if self.key_entry.cget("show") == "*":
            self.key_entry.config(show="")
        else:
            self.key_entry.config(show="*")
    
    def validate_key(self, key):
        """Kiểm tra khóa có đúng 8 ký tự không"""
        if len(key) != 8:
            messagebox.showerror("Lỗi", "Khóa phải đúng 8 ký tự!")
            return False
        return True
    
    def process_file(self):
        """Xử lý file: mã hóa hoặc giải mã"""
        if not self.file_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn file đầu vào!")
            return
        
        key = self.key_entry.get()
        if not self.validate_key(key):
            return
        
        try:
            # Chuyển đổi key thành bytes
            key_bytes = key.encode('utf-8')
            
            # Xác định đường dẫn file đầu ra
            file_name, file_ext = os.path.splitext(self.file_path)
            mode = self.mode.get()
            
            if mode == "encrypt":
                self.output_file = f"{file_name}_encrypted{file_ext}"
                self.encrypt_file(self.file_path, self.output_file, key_bytes)
                self.status_label.config(text=f"Trạng thái: Mã hóa thành công!", fg="green")
            else:
                self.output_file = f"{file_name}_decrypted{file_ext}"
                self.decrypt_file(self.file_path, self.output_file, key_bytes)
                self.status_label.config(text=f"Trạng thái: Giải mã thành công!", fg="green")
            
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(0, self.output_file)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")
            self.status_label.config(text=f"Trạng thái: Lỗi - {str(e)}", fg="red")
    
    def encrypt_file(self, input_file, output_file, key):
        """Mã hóa file sử dụng thuật toán DES"""
        # Tạo đối tượng DES
        cipher = DES.new(key, DES.MODE_ECB)
        
        # Đọc dữ liệu từ file đầu vào
        with open(input_file, 'rb') as f:
            data = f.read()
        
        # Đệm dữ liệu để đảm bảo độ dài chia hết cho 8
        padded_data = pad(data, DES.block_size)
        
        # Mã hóa dữ liệu
        encrypted_data = cipher.encrypt(padded_data)
        
        # Ghi dữ liệu đã mã hóa vào file đầu ra
        with open(output_file, 'wb') as f:
            f.write(encrypted_data)
    
    def decrypt_file(self, input_file, output_file, key):
        """Giải mã file sử dụng thuật toán DES"""
        # Tạo đối tượng DES
        cipher = DES.new(key, DES.MODE_ECB)
        
        # Đọc dữ liệu từ file đầu vào
        with open(input_file, 'rb') as f:
            encrypted_data = f.read()
        
        # Giải mã dữ liệu
        decrypted_data = cipher.decrypt(encrypted_data)
        
        # Loại bỏ phần đệm
        try:
            unpadded_data = unpad(decrypted_data, DES.block_size)
        except ValueError:
            # Nếu có lỗi khi loại bỏ đệm, có thể file không được mã hóa đúng
            messagebox.showerror("Lỗi", "Không thể giải mã file. Kiểm tra lại khóa hoặc file đầu vào!")
            raise ValueError("Không thể giải mã file")
        
        # Ghi dữ liệu đã giải mã vào file đầu ra
        with open(output_file, 'wb') as f:
            f.write(unpadded_data)
    
    def download_file(self):
        """Mở file kết quả"""
        if not self.output_file:
            messagebox.showerror("Lỗi", "Chưa có file kết quả!")
            return
        
        try:
            # Mở file kết quả bằng ứng dụng mặc định
            os.startfile(self.output_file)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DESApp(root)
    root.mainloop()