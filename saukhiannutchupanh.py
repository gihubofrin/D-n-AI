import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Camera App")

        self.camera = cv2.VideoCapture(0)  # Mở camera

        self.label = ttk.Label(root)
        self.label.pack()

        self.capture_button = ttk.Button(root, text="Chụp ảnh", command=self.capture_image)
        self.capture_button.pack()

        # Load mô hình CNN đã huấn luyện
        self.model = tf.keras.models.load_model('MODE_phan_loai_3_loai_rac_arcur.h5')
        # Các nhãn của các lớp rác thải
        self.labels = ["RÁC HỮU CƠ", "RÁC SINH HOẠT", "RÁC CÓ THỂ TÁI CHẾ"]

        # Mô tả cho từng loại rác
        self.descriptions = {
            "RÁC HỮU CƠ": "Rác hữu cơ bao gồm các vật liệu sinh học hoặc có thể phân hủy tự nhiên trong điều kiện môi trường thông thường, như thức ăn thừa, lá cây, vỏ trái cây, ...",
            "RÁC SINH HOẠT": "Rác sinh hoạt là các vật liệu từ hoạt động hàng ngày của con người như nhựa, giấy, kim loại, ...",
            "RÁC CÓ THỂ TÁI CHẾ": "Rác có thể tái chế bao gồm các vật liệu có thể được xử lý để tạo ra sản phẩm mới mà không gây hại đến môi trường, như giấy tái chế, chai nhựa tái chế, kim loại tái chế, ..."
        }

        # Label để hiển thị kết quả phân loại
        self.result_label = ttk.Label(root, text="", font=("Arial", 16))
        self.result_label.pack()

    def update_camera(self):
        ret, frame = self.camera.read()  # Đọc frame từ camera
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Chuyển đổi sang định dạng RGB
            image = Image.fromarray(frame_rgb)  # Tạo ảnh từ frame
            photo = ImageTk.PhotoImage(image=image)  # Chuyển ảnh thành PhotoImage để hiển thị trên tkinter
            self.label.configure(image=photo)
            self.label.image = photo

        self.root.after(10, self.update_camera)  # Lặp lại cập nhật sau mỗi 10ms

    def capture_image(self):
        ret, frame = self.camera.read()  # Đọc frame từ camera
        if ret:
            cv2.imwrite("captured_image.jpg", frame)  # Lưu ảnh đã chụp thành tệp JPEG
            print("Đã chụp ảnh và lưu thành công")
            # Hiển thị ảnh đã chụp và kết quả phân loại
            self.display_image_and_result("captured_image.jpg")

    # Hàm để nhận dạng rác thải từ ảnh
    def detect_waste(self, image_path):
        image = Image.open(image_path)
        # Resize ảnh thành kích thước mà mô hình yêu cầu
        image = image.resize((224, 224))
        # Chuyển ảnh thành numpy array và chuẩn hóa giá trị pixel
        image_array = np.asarray(image) / 255.0
        # Thêm một chiều mới cho batch (vì mô hình cần đầu vào dạng batch)
        image_array = np.expand_dims(image_array, axis=0)

        # Dự đoán nhãn của ảnh
        predictions = self.model.predict(image_array)
        # Lấy chỉ số của nhãn có xác suất cao nhất
        predicted_label_index = np.argmax(predictions[0])
        # Lấy nhãn tương ứng với chỉ số đó
        predicted_label = self.labels[predicted_label_index]

        return predicted_label

    def display_image_and_result(self, image_path):
        # Hiển thị ảnh đã chụp
        image = Image.open(image_path)
        image = image.resize((300, 300))  # Resize ảnh để hiển thị
        photo = ImageTk.PhotoImage(image=image)
        self.label.configure(image=photo)
        self.label.image = photo

        # Phân loại rác trong ảnh đã chụp
        predicted_label = self.detect_waste(image_path)
        # Hiển thị kết quả phân loại
        description = self.descriptions.get(predicted_label, "Không có mô tả")
        self.result_label.config(text=f"Kết quả: {predicted_label}\nMô tả: {description}")

root = tk.Tk()
app = CameraApp(root)
app.update_camera()  # Bắt đầu cập nhật camera
root.mainloop()
