import pyperclip
import cv2
from tkinter import filedialog
import tkinter as tk
import os


class ImageConverter(object):
    def __init__(self, master, **kwargs):

        master.winfo_toplevel().title("Image to rgb565 converter")
        path_to_icon = os.path.dirname(os.path.abspath(__file__))+"\\dva.ico"
        try:
            master.iconbitmap(path_to_icon)
        except tk.TclError:
            print("Wrong path to icon!")

        self.file_loaded = False

        self.master = master

        # Define frames for widgets
        self.image_path_frame = tk.Frame(self.master)
        self.width_frame = tk.Frame(self.master)
        self.height_frame = tk.Frame(self.master)
        self.array_name_frame = tk.Frame(self.master)
        self.convert_frame = tk.Frame(self.master)
        self.result_text_frame = tk.Frame(self.master)

        # Define file path, desired width and height inputs
        self.file_path = tk.StringVar()
        self.file_path.set("File path.")

        self.file_width = tk.IntVar()
        self.file_width.set(0)

        self.file_height = tk.IntVar()
        self.file_width.set(0)

        self.image_path_input = tk.Entry(self.image_path_frame, textvariable=self.file_path)
        self.image_path_label = tk.Label(self.image_path_frame, text="Path to file: ")
        self.image_load_button = tk.Button(self.image_path_frame, text="Open file", command=self.open_file)

        self.width_input = tk.Entry(self.width_frame, textvariable=self.file_width)
        self.height_input = tk.Entry(self.height_frame, textvariable=self.file_height)
        self.width_label = tk.Label(self.width_frame, text="Width: ")
        self.height_label = tk.Label(self.height_frame, text="Height: ")

        self.array_name = tk.StringVar()
        self.array_name.set("obstacle")

        self.array_name_label = tk.Label(self.array_name_frame, text="Array name: ")
        self.array_name_input = tk.Entry(self.array_name_frame, textvariable=self.array_name)

        self.convert_button = tk.Button(self.convert_frame, text="Convert image", command=self.convert)
        self.copy_button = tk.Button(self.convert_frame, text="Copy result", command=self.copy_to_clipboard)

        self.result_label = tk.Label(self.result_text_frame,
                                     text="Conversion result will appear in text area below.\nNote that Copy button "
                                          "will automatically copy result to your clipboard.")
        self.result_text = tk.Text(self.result_text_frame)
        self.result_scrollbar = tk.Scrollbar(self.result_text_frame)

        # Pack all frames
        self.image_path_frame.pack()
        self.width_frame.pack()
        self.height_frame.pack()
        self.array_name_frame.pack()
        self.convert_frame.pack()
        self.result_text_frame.pack()

        # Pack widgets in frames
        self.image_path_label.pack(side=tk.LEFT)
        self.image_path_input.pack(side=tk.LEFT)
        self.image_load_button.pack(side=tk.LEFT, padx=5)

        self.width_label.pack(side=tk.LEFT)
        self.width_input.pack(side=tk.LEFT)

        self.height_label.pack(side=tk.LEFT)
        self.height_input.pack(side=tk.LEFT)

        self.array_name_label.pack(side=tk.LEFT)
        self.array_name_input.pack(side=tk.LEFT)

        self.convert_button.pack(side=tk.LEFT, padx=5, pady=5)
        self.copy_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.result_label.pack()
        self.result_text.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.result_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

        # Config scrollbar
        self.result_scrollbar.config(command=self.result_text.yview)
        self.result_text.config(yscrollcommand=self.result_scrollbar.set)

        # Disable result_text area
        self.result_text.configure(state='disabled')

        # Define image
        self.image = None

    def open_file(self):
        print("Here we go!")
        initial_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path.set(filedialog.askopenfilename(initialdir=initial_dir, title="Select file",
                                                      filetypes=(("png files", "*.png"), ("jpeg files", "*.jpg*"))))

        self.image = cv2.imread(self.file_path.get())

        if self.image is not None:
            height, width, channels = self.image.shape
            self.file_width.set(width)
            self.file_height.set(height)

    def convert(self):
        array_name = self.array_name_input.get()

        width = self.file_width.get()
        height = self.file_height.get()

        resized = self.resize(self.image)

        result = "static const uint16_t PROGMEM " + array_name + "[] = { " + hex(width) + ", " + hex(
            height) + ", " + "\n"
        for x in range(len(resized)):
            for y in range(len(resized[x])):
                result += self.convert_to_565(resized[x][y][0], resized[x][y][1], resized[x][y][2]) + ', '
            result += "\n"

        result = result[0:-3] + "\n};"

        self.result_text.configure(state='normal')
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert('end', result)
        self.result_text.configure(state='disabled')

        file = open("result.txt", "w")

        file.write(result)

        file.close()

        cv2.imshow('Converted image', resized)

    def convert_to_565(self, b, g, r):
        result = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
        return '0x' + format(result, '04X')

    def resize(self, img):
        dim = (self.file_width.get(), self.file_height.get())
        # resize image
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_NEAREST)

        return resized

    def copy_to_clipboard(self):
        pyperclip.copy(self.result_text.get('1.0', 'end-1c'))


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverter(root)
    root.mainloop()
