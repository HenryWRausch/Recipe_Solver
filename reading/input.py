import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import easyocr
import parser
import cv2


class OCRSelector:
    def __init__(self, root, image_path):
        self.root = root
        self.image = Image.open(image_path).convert("RGB")
        self.tk_image = ImageTk.PhotoImage(self.image)

        # EasyOCR reader
        self.reader = easyocr.Reader(['en'], gpu=True, verbose=False)

        # Layout: left for image, right for text editor
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.main_frame, width=self.image.width, height=self.image.height)
        self.canvas.pack(side="left")

        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")

        self.text_frame = tk.Frame(self.main_frame)
        self.text_frame.pack(side="right", fill="both", expand=True)

        self.text_label = tk.Label(self.text_frame, text="Extracted Text:")
        self.text_label.pack()

        self.text_box = tk.Text(self.text_frame, wrap="word", width=50)
        self.text_box.pack(fill="both", expand=True)

        self.parse_button = tk.Button(self.text_frame, text="Run Parser", command=self.run_parser)
        self.parse_button.pack(pady=5)

        # Canvas rectangle selector
        self.rect = None
        self.start_x = self.start_y = 0

        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_click(self, event):
        self.start_x, self.start_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="red")

    def on_drag(self, event):
        assert self.rect is not None
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        assert self.rect is not None
        x0, y0, x1, y1 = map(int, self.canvas.coords(self.rect))
        if x0 == x1 or y0 == y1:
            print("Selection too small or invalid.")
            return

        cropped = self.image.crop((x0, y0, x1, y1))
        np_img = np.array(cropped)

        results = self.reader.readtext(np_img, decoder='beamsearch')
        extracted_text = ''

        for (_, text, _) in results:
            extracted_text += f'{text}\n'

        # Populate text box with extracted text
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, extracted_text)

    def run_parser(self):
        edited_text = self.text_box.get(1.0, tk.END).strip()
        print("\nParsed Results:")
        print(parser.IngredientList(edited_text))


# Main Execution
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Select Region for OCR")

    path = filedialog.askopenfilename(title="Select an image file")
    if path:
        app = OCRSelector(root, path)
        root.mainloop()

