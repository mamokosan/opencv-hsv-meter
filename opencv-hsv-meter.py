import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np


class ColorMeterApp:
    """
    HSV値とRGB値を表示するためのデジタルカラーメーターアプリ。
    PILとOpenCVを利用して、選択した画像上でマウスカーソルが指す位置の色情報を表示します。
    """

    def __init__(self, master):
        self.master = master
        self.master.title("Digital Color Meter")

        self.initialize_ui()
        self.initialize_image_variables()

    def initialize_ui(self):
        """UIコンポーネントの初期化と配置を行います。"""
        self.master.geometry("300x100")
        self.label_message = tk.Label(self.master, text="画像を選択してください")
        self.label_message.pack(side=tk.TOP, pady=10)

        self.btn_open = tk.Button(self.master, text="Open", command=self.open_image)
        self.btn_open.pack(side=tk.LEFT, padx=120, pady=10)

        self.canvas = tk.Canvas(self.master, width=300, height=600)
        self.canvas.pack(side=tk.LEFT, padx=30)

        self.rgb_label = tk.Label(self.master, text="")
        self.rgb_label.place(relx=0.8, rely=0.45, anchor="center")

        self.hsv_label = tk.Label(self.master, text="")
        self.hsv_label.place(relx=0.8, rely=0.5, anchor="center")

        self.converted_hsv_label = tk.Label(self.master, text="")
        self.converted_hsv_label.place(relx=0.8, rely=0.55, anchor="center")

    def initialize_image_variables(self):
        """画像処理用の変数の初期化を行います。"""
        self.photo_image = None
        self.cv_image = None
        self.hsv_image = None

    def open_image(self):
        """画像ファイルを開くためのダイアログを表示し、選択された画像を処理します。"""
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        image = Image.open(file_path)
        self.adjust_ui_for_image(image)
        self.process_image(image)

    def adjust_ui_for_image(self, image):
        """画像選択後のUIの調整を行います。"""
        self.master.geometry("800x800")
        self.label_message.destroy()
        self.btn_open.pack(side=tk.BOTTOM, padx=10, pady=30)

    def process_image(self, image):
        """画像の処理とマウスイベントバインドを行います。"""
        resized_image = image.resize(
            (image.width // 2, image.height // 2), Image.Resampling.LANCZOS
        )
        self.photo_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo_image)
        self.canvas.bind("<Motion>", self.show_values)

        # OpenCVでの画像処理
        self.cv_image = cv2.cvtColor(np.array(resized_image), cv2.COLOR_RGB2BGR)
        self.hsv_image = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2HSV)

    def show_values(self, event):
        """マウスカーソル位置の色情報を表示します。"""
        if self.hsv_image is not None:
            x, y = event.x, event.y
            if x < self.cv_image.shape[1] and y < self.cv_image.shape[0]:
                self.display_color_values(x, y)

    def display_color_values(self, x, y):
        """指定された位置のRGBとHSVの色情報を表示します。"""
        hsv_value = self.hsv_image[y, x]
        rgb_value = self.cv_image[y, x]

        h, s, v = hsv_value
        b, g, r = rgb_value

        h_converted, s_converted, v_converted = h * 2, s / 255 * 100, v / 255 * 100

        self.rgb_label.config(text=f"RGB: ({r}, {g}, {b})")
        self.hsv_label.config(text=f"OpenCV HSV: ({h}, {s}, {v})")
        self.converted_hsv_label.config(
            text=f"HSV: ({h_converted:.0f}, {s_converted:.0f}, {v_converted:.0f})"
        )


def main():
    root = tk.Tk()
    app = ColorMeterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
