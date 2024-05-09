import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf

# Load mô hình CNN đã huấn luyện
model = tf.keras.models.load_model('MODE_phan_loai_3_loai_rac_arcur.h5')

# Các nhãn của các lớp rác thải
labels = ["RÁC HỮU CƠ", "RÁC SINH HOẠT", "RÁC CÓ THỂ TÁI CHẾ"]

# Mô tả cho từng loại rác
descriptions = {
    "RÁC HỮU CƠ": "Rác hữu cơ bao gồm các vật liệu có thể phân hủy tự nhiên trong điều kiện môi trường thông thường, như thức ăn thừa, lá cây, vỏ trái cây, ...",
    "RÁC SINH HOẠT": "Rác sinh hoạt là các vật liệu từ hoạt động hàng ngày của con người như nhựa, giấy, kim loại, ...",
    "RÁC CÓ THỂ TÁI CHẾ": "Rác có thể tái chế bao gồm các vật liệu có thể được xử lý để tạo ra sản phẩm mới mà không gây hại đến môi trường, như giấy tái chế, chai nhựa tái chế, kim loại tái chế, ..."
}

# Hàm để load ảnh từ đường dẫn và hiển thị trên GUI
def load_image_and_detect():
    file_path = filedialog.askopenfilename()
    image = Image.open(file_path)
    image = image.resize((224, 224))  # Resize ảnh thành 224x224
    photo = ImageTk.PhotoImage(image)
    panel.config(image=photo)
    panel.image = photo
    
    # Gọi hàm để nhận dạng rác thải từ ảnh
    detect_waste(image)

# Hàm để nhận dạng rác thải từ ảnh
def detect_waste(image):
    # Chuyển ảnh thành numpy array và chuẩn hóa giá trị pixel
    image_array = np.asarray(image) / 255.0
    # Thêm một chiều mới cho batch (vì mô hình cần đầu vào dạng batch)
    image_array = np.expand_dims(image_array, axis=0)
    
    # Dự đoán nhãn của ảnh
    predictions = model.predict(image_array)
    # Lấy chỉ số của nhãn có xác suất cao nhất
    predicted_label_index = np.argmax(predictions[0])
    # Lấy nhãn tương ứng với chỉ số đó
    predicted_label = labels[predicted_label_index]
    
    # Hiển thị kết quả nhận dạng lên giữa màn hình
    result_label.config(text="Loại rác: " + predicted_label + "\nMô tả: " + descriptions.get(predicted_label, "Không có mô tả"))
    result_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Tạo giao diện người dùng
root = tk.Tk()
root.title("Waste Detection App")

# Lấy kích thước của màn hình
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Thiết lập kích thước cửa sổ ứng dụng
app_width = int(screen_width * 0.7)
app_height = int(screen_height * 0.7)
app_x = (screen_width - app_width) // 2
app_y = (screen_height - app_height) // 2
root.geometry(f"{app_width}x{app_height}+{app_x}+{app_y}")

# Panel để hiển thị ảnh
panel = tk.Label(root)
panel.pack()

# Nút để tải ảnh
load_button = tk.Button(root, text="Tải ảnh rác mà bạn cần phân loại", command=load_image_and_detect, width=40, height=5)
load_button.pack(side=tk.BOTTOM, pady=10)

# Label để hiển thị kết quả nhận dạng
result_label = tk.Label(root, text="", font=("Arial", 16), wraplength=400, justify=tk.CENTER)
result_label.pack(pady=10)

root.mainloop()
