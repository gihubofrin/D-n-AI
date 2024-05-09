from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
import os
import subprocess

class WelcomeScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)

        # Hiển thị hình ảnh đại diện
        self.background_image = AsyncImage(source="Premium Vector _ Containers waste sorting recycling plastic organic  garbage_ eco-friendly concept.jpg")
        self.add_widget(self.background_image)

        # Tạo nút "Chụp ảnh"
        capture_button = Button(text="Chụp ảnh", size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.3, 'center_y': 0.1})
        capture_button.bind(on_press=self.capture_image)
        self.add_widget(capture_button)

        # Tạo nút "Tải ảnh"
        upload_button = Button(text="Tải ảnh", size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.7, 'center_y': 0.1})
        upload_button.bind(on_press=self.open_file_dialog)
        self.add_widget(upload_button)

        # Hiển thị hình ảnh avatar đại diện
        avatar_image = AsyncImage(source="Premium Vector _ Containers waste sorting recycling plastic organic  garbage_ eco-friendly concept.jpg", size_hint=(None, None), size=(200, 200), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(avatar_image)

    # Hàm xử lý sự kiện khi nút "Chụp ảnh" được nhấn
    def capture_image(self, instance):
        # Code xử lý khi nút "Chụp ảnh" được nhấn
        subprocess.Popen(['python', 'saukhiannutchupanh.py'])

    # Hàm xử lý sự kiện khi nút "Tải ảnh" được nhấn
    def open_file_dialog(self, instance):
        # Gọi hàm để mở cửa sổ tải ảnh
        subprocess.Popen(['python', 'saukhiannuttaianh.py'])

        

class MyImageEditingApp(App):
    def build(self):
        return WelcomeScreen()

if __name__ == '__main__':
    MyImageEditingApp().run()
