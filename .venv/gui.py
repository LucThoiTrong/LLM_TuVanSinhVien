import os
import tkinter as tk
from tkinter import ttk, Frame, Label, Entry, Button, PhotoImage, Canvas, Scrollbar, messagebox
import threading
import time
from datetime import datetime

# Import các hàm và biến cần thiết từ backend.py
try:
    from backend import (
        initialize_openai_client,
        chat_with_model,
        messages
    )
except ImportError:
    print("LỖI: Không thể nhập từ backend.py. Đảm bảo tệp backend.py tồn tại và chứa các biến/hàm cần thiết.")


    # Thiết lập các giá trị mặc định hoặc hiển thị lỗi và thoát nếu backend là cốt lõi
    def initialize_openai_client():
        print("CẢNH BÁO: Hàm initialize_openai_client giả lập do backend.py không tìm thấy.")
        messagebox.showerror("Lỗi Backend", "Không thể tải tệp backend.py. Chức năng chatbot sẽ bị hạn chế.")
        return False


    def chat_with_model(user_text, conversation_history):
        print("CẢNH BÁO: Hàm chat_with_model giả lập do backend.py không tìm thấy.")
        time.sleep(1)  # Giả lập độ trễ
        return "Phản hồi giả lập do lỗi backend. Vui lòng kiểm tra tệp backend.py."

class ModernChatbotUI:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Chatbot Tư Vấn Chuyên Ngành CNTT")

        # --- BẮT ĐẦU MÃ ĐỂ CĂN GIỮA CỬA SỔ ---
        # Đặt kích thước cửa sổ mong muốn ban đầu
        window_width = 850
        window_height = 650

        # Lấy kích thước màn hình
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Tính toán vị trí x, y để cửa sổ nằm giữa
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        # Đặt vị trí và kích thước cho cửa sổ
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
        # --- KẾT THÚC MÃ ĐỂ CĂN GIỮA CỬA SỔ ---

        self.root.configure(bg="#f7fafc")  # Cấu hình màu nền sau khi đặt geometry

        self.send_icon = None
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.join(base_dir, "assets", "send_icon.png")
            if os.path.exists(icon_path):
                self.send_icon = PhotoImage(file=icon_path).subsample(2, 2)
            else:
                print(f"Không tìm thấy file icon tại: {icon_path}. Sử dụng nút văn bản.")
        except tk.TclError as e:
            print(f"Lỗi khi tải icon (TclError): {e}. Sử dụng nút văn bản.")
        except Exception as e:  # Bắt các lỗi khác có thể xảy ra
            print(f"Lỗi không xác định khi tải icon: {e}. Sử dụng nút văn bản.")

        self.BG_COLOR = "#f7fafc"
        self.TEXT_COLOR = "#1a202c"
        self.INPUT_BG_COLOR = "#ffffff"
        self.CHAT_AREA_BG_COLOR = "#ffffff"
        self.BUTTON_COLOR = "#5a67d8"  # Màu gradient bắt đầu
        self.BUTTON_HOVER_COLOR = "#4c51bf"
        self.BUTTON_TEXT_COLOR = "#ffffff"
        self.USER_BUBBLE_COLOR = "#5a67d8"
        self.USER_TEXT_COLOR = "#ffffff"
        self.ASSISTANT_BUBBLE_COLOR = "#edf2f7"
        self.ASSISTANT_TEXT_COLOR = "#2d3748"
        self.BORDER_COLOR = "#e2e8f0"
        self.ACCENT_COLOR = "#38b2ac"
        self.GRADIENT_END_COLOR = "#9f7aea"  # Màu gradient kết thúc

        self.header_font = ("Segoe UI", 20, "bold")  # Giảm kích thước font một chút
        self.chat_font = ("Segoe UI", 11)
        self.input_font = ("Segoe UI", 12)
        self.timestamp_font = ("Segoe UI", 8, "italic")
        self.placeholder_color = "grey"

        self.main_frame = Frame(self.root, bg=self.BG_COLOR)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.header_canvas = Canvas(self.main_frame, height=65, bg=self.BG_COLOR,
                                    highlightthickness=0)  # Giảm chiều cao header
        self.header_canvas.pack(fill=tk.X, pady=(0, 15))
        self.header_canvas.bind("<Configure>", self.on_header_canvas_configure)

        self.header_label_text = "Trợ Lý Tư Vấn Chuyên Ngành CNTT"
        # Sẽ tạo text item trên canvas thay vì Label widget để hòa trộn tốt hơn với gradient
        self.header_text_id = self.header_canvas.create_text(
            0, 0,  # Tọa độ sẽ được cập nhật trong on_header_canvas_configure
            text=self.header_label_text,
            font=self.header_font,
            fill="#ffffff",  # Màu chữ
            anchor="center"
        )

        self.chat_canvas_frame = Frame(self.main_frame, bg=self.CHAT_AREA_BG_COLOR, relief=tk.FLAT, bd=0)
        self.chat_canvas_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        self.chat_canvas_frame.configure(highlightbackground=self.BORDER_COLOR, highlightthickness=1)

        self.chat_canvas = Canvas(self.chat_canvas_frame, bg=self.CHAT_AREA_BG_COLOR, highlightthickness=0)
        self.scrollbar = Scrollbar(self.chat_canvas_frame, orient="vertical", command=self.chat_canvas.yview,
                                   relief=tk.FLAT, bd=0, width=12)
        self.chat_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.scrollbar.configure(troughcolor=self.BG_COLOR, bg=self.ACCENT_COLOR, activebackground=self.BUTTON_COLOR)
        self.chat_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.chat_display_frame = Frame(self.chat_canvas, bg=self.CHAT_AREA_BG_COLOR)
        self.canvas_window = self.chat_canvas.create_window((0, 0), window=self.chat_display_frame, anchor="nw")

        self.chat_display_frame.bind("<Configure>",
                                     lambda e: self.chat_canvas.configure(scrollregion=self.chat_canvas.bbox("all")))
        self.chat_canvas.bind("<Configure>", self.on_canvas_configure)
        self._bind_mousewheel_to_all(self.root)  # Bind mousewheel cho toàn bộ cửa sổ và các con

        self.input_frame_container = Frame(self.main_frame, bg=self.BG_COLOR)
        self.input_frame_container.pack(fill=tk.X, pady=(5, 0))

        self.input_frame = Frame(self.input_frame_container, bg=self.INPUT_BG_COLOR, bd=0, relief=tk.FLAT)
        self.input_frame.pack(fill=tk.X, ipady=5, ipadx=5)
        self.input_frame.configure(highlightbackground=self.BORDER_COLOR, highlightthickness=1)

        self.user_input_entry = Entry(
            self.input_frame, font=self.input_font, bg=self.INPUT_BG_COLOR, fg=self.placeholder_color,
            relief=tk.FLAT, insertbackground=self.TEXT_COLOR, bd=0
        )
        self.user_input_entry.pack(side=tk.LEFT, padx=(10, 5), pady=10, fill=tk.X, expand=True)
        self.user_input_entry.insert(0, "Nhập câu hỏi của bạn...")
        self.user_input_entry.bind("<Return>", self.send_message_event_handler)
        self.user_input_entry.bind("<FocusIn>", self.on_input_focus_in)
        self.user_input_entry.bind("<FocusOut>", self.on_input_focus_out)
        # Không cần focus_set() ở đây nếu bạn muốn placeholder hiển thị ban đầu

        self.send_button = Button(
            self.input_frame, text="Gửi" if self.send_icon is None else "", image=self.send_icon,
            compound=tk.CENTER if self.send_icon else tk.NONE, font=(self.chat_font[0], 10, "bold"),
            bg=self.BUTTON_COLOR, fg=self.BUTTON_TEXT_COLOR, relief=tk.FLAT,
            padx=10, pady=8, activebackground=self.BUTTON_HOVER_COLOR, activeforeground=self.BUTTON_TEXT_COLOR,
            command=self.send_message_event_handler, cursor="hand2", bd=0,
            width=35 if self.send_icon else None, height=35 if self.send_icon else None
        )
        self.send_button.pack(side=tk.RIGHT, padx=(0, 10), pady=(8, 8))  # Điều chỉnh pady
        self.send_button.bind("<Enter>", lambda e: self.send_button.config(bg=self.BUTTON_HOVER_COLOR))
        self.send_button.bind("<Leave>", lambda e: self.send_button.config(bg=self.BUTTON_COLOR))


        self.root.after(200, lambda: self.add_message_to_display(
            "Chào bạn! Mình là trợ lý tư vấn chuyên ngành CNTT. Bạn cần mình giúp gì hôm nay?", "assistant"
        ))

    def on_header_canvas_configure(self, event=None):
        canvas = self.header_canvas
        self.create_gradient(canvas, self.BUTTON_COLOR, self.GRADIENT_END_COLOR)
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        # Căn giữa text item
        canvas.coords(self.header_text_id, width / 2, height / 2)
        canvas.tag_raise(self.header_text_id)  # Đảm bảo text nằm trên gradient

    def create_gradient(self, canvas, color1_hex, color2_hex):
        canvas.delete("gradient_line")  # Xóa gradient cũ nếu có
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width <= 1 or height <= 1: return

        r1, g1, b1 = canvas.winfo_rgb(color1_hex)
        r2, g2, b2 = canvas.winfo_rgb(color2_hex)
        r1, g1, b1 = r1 // 256, g1 // 256, b1 // 256
        r2, g2, b2 = r2 // 256, g2 // 256, b2 // 256

        for i in range(width):
            nr = int(r1 + (r2 - r1) * i / width)
            ng = int(g1 + (g2 - g1) * i / width)
            nb = int(b1 + (b2 - b1) * i / width)
            color = f"#{nr:02x}{ng:02x}{nb:02x}"
            canvas.create_line(i, 0, i, height, fill=color, tags="gradient_line")

    def on_input_focus_in(self, event=None):
        if self.user_input_entry.get() == "Nhập câu hỏi của bạn...":
            self.user_input_entry.delete(0, tk.END)
            self.user_input_entry.config(fg=self.TEXT_COLOR)
        self.input_frame.config(highlightbackground=self.ACCENT_COLOR, highlightthickness=2)

    def on_input_focus_out(self, event=None):
        if not self.user_input_entry.get().strip():
            self.user_input_entry.delete(0, tk.END)  # Xóa khoảng trắng nếu có
            self.user_input_entry.insert(0, "Nhập câu hỏi của bạn...")
            self.user_input_entry.config(fg=self.placeholder_color)
        self.input_frame.config(highlightbackground=self.BORDER_COLOR, highlightthickness=1)

    def on_canvas_configure(self, event=None):
        canvas_width = self.chat_canvas.winfo_width()
        self.chat_canvas.itemconfig(self.canvas_window, width=canvas_width)
        # Không tự cuộn ở đây, để add_message_to_display xử lý

    def _bind_mousewheel_to_all(self, widget):
        # Sử dụng bind_all cho cửa sổ gốc (self.root) thay vì widget bất kỳ
        self.root.bind_all("<MouseWheel>", self._on_mousewheel_windows_mac, add="+")
        self.root.bind_all("<Button-4>", self._on_mousewheel_linux, add="+")
        self.root.bind_all("<Button-5>", self._on_mousewheel_linux, add="+")

    def _is_scrollable_widget(self, widget):
        # Kiểm tra xem widget có phải là chat_canvas hoặc con của nó không
        parent = widget
        while parent is not None:
            if parent == self.chat_canvas:
                return True
            # Thêm kiểm tra cho scrollbar để tránh lỗi nếu widget là None
            if hasattr(parent, 'master'):
                parent = parent.master
            else:  # Không có master, dừng lại
                break
        return False

    def _on_mousewheel_windows_mac(self, event):
        # event.widget có thể không phải là widget mà con trỏ đang trỏ tới
        # nếu bind_all được sử dụng. Thay vào đó, lấy widget dưới con trỏ.
        try:
            widget_under_cursor = self.root.winfo_containing(event.x_root, event.y_root)
            if widget_under_cursor is None: return
        except tk.TclError:  # Widget có thể không tồn tại (ví dụ: khi đóng cửa sổ)
            return

        if self._is_scrollable_widget(widget_under_cursor):
            current_yview = self.chat_canvas.yview()
            if (event.delta < 0 and current_yview[1] < 1.0) or \
                    (event.delta > 0 and current_yview[0] > 0.0):
                self.chat_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                return "break"

    def _on_mousewheel_linux(self, event):
        try:
            widget_under_cursor = self.root.winfo_containing(event.x_root, event.y_root)
            if widget_under_cursor is None: return
        except tk.TclError:
            return

        if self._is_scrollable_widget(widget_under_cursor):
            current_yview = self.chat_canvas.yview()
            if event.num == 4:  # Scroll up
                if current_yview[0] > 0.0:
                    self.chat_canvas.yview_scroll(-1, "units")
                    return "break"
            elif event.num == 5:  # Scroll down
                if current_yview[1] < 1.0:
                    self.chat_canvas.yview_scroll(1, "units")
                    return "break"

    def add_message_to_display(self, message_text, sender, show_typing=False):
        self.chat_canvas.update_idletasks()  # Đảm bảo kích thước canvas chính xác
        available_width = self.chat_canvas.winfo_width() - 25
        bubble_max_width = available_width * 0.78 if available_width > 100 else max(available_width - 10,
                                                                                    150)  # Đảm bảo chiều rộng tối thiểu

        align_frame = Frame(self.chat_display_frame, bg=self.CHAT_AREA_BG_COLOR)
        pack_options = {"side": tk.TOP, "fill": tk.X, "pady": (7, 3)}
        bubble_ipadx, bubble_ipady = 10, 8  # Tăng ipady một chút

        if sender == "user":
            align_frame.pack(**pack_options, padx=(max(20, available_width * 0.20), 10))
            bubble_bg = self.USER_BUBBLE_COLOR
            text_fg = self.USER_TEXT_COLOR
            text_justify = tk.LEFT
        else:  # Assistant
            align_frame.pack(**pack_options, padx=(10, max(20, available_width * 0.20)))
            bubble_bg = self.ASSISTANT_BUBBLE_COLOR
            text_fg = self.ASSISTANT_TEXT_COLOR
            text_justify = tk.LEFT

        bubble_container = Frame(align_frame, bg=self.CHAT_AREA_BG_COLOR)
        if sender == "user":
            bubble_container.pack(side=tk.RIGHT, anchor=tk.NE)
        else:
            bubble_container.pack(side=tk.LEFT, anchor=tk.NW)

        bubble_canvas = Canvas(bubble_container, bg=self.CHAT_AREA_BG_COLOR, highlightthickness=0, relief=tk.FLAT)

        msg_label_text = "Trợ lý đang soạn..." if show_typing else message_text
        msg_font = self.timestamp_font if show_typing else self.chat_font

        # Sử dụng Label ẩn để tính toán kích thước cần thiết cho Canvas text
        temp_label = Label(self.root, text=msg_label_text, font=msg_font, wraplength=bubble_max_width,
                           justify=text_justify, padx=bubble_ipadx, pady=bubble_ipady)
        temp_label.update_idletasks()  # Quan trọng
        req_width = temp_label.winfo_reqwidth()
        req_height = temp_label.winfo_reqheight()
        temp_label.destroy()  # Xóa label tạm

        bubble_canvas.config(width=req_width, height=req_height)

        radius = 10
        x0, y0, x1, y1 = 0, 0, req_width, req_height
        points = [
            x0 + radius, y0, x1 - radius, y0, x1, y0 + radius, x1, y1 - radius,
            x1 - radius, y1, x0 + radius, y1, x0, y1 - radius, x0, y0 + radius,
        ]
        bubble_canvas.create_polygon(points, fill=bubble_bg, smooth=True, splinesteps=12)  # Tăng splinesteps

        # Đặt text item trên canvas
        # Cần tính toán padding cho text item bên trong canvas
        text_width_for_canvas = req_width - (2 * bubble_ipadx)  # Chiều rộng cho text wrap bên trong canvas
        if text_width_for_canvas < 1: text_width_for_canvas = 1  # Đảm bảo không âm hoặc 0

        bubble_canvas.create_text(
            bubble_ipadx,  # x-offset từ cạnh trái canvas đến text
            bubble_ipady,  # y-offset từ cạnh trên canvas đến text
            text=msg_label_text,
            font=msg_font,
            fill=text_fg,
            anchor=tk.NW,
            width=text_width_for_canvas,  # Chiều rộng để text tự động xuống dòng
            justify=text_justify
        )
        bubble_canvas.pack()

        if show_typing:
            self.typing_indicator_bubble_canvas = bubble_canvas
            self.animate_typing_indicator()
        elif sender == "assistant" or sender == "user":
            timestamp_frame = Frame(bubble_container, bg=self.CHAT_AREA_BG_COLOR)
            pack_side = tk.RIGHT if sender == "user" else tk.LEFT
            timestamp_frame.pack(side=pack_side, anchor=tk.SE if sender == "user" else tk.SW, padx=5, pady=(0, 2))
            timestamp_text = datetime.now().strftime("%H:%M")
            timestamp_label = Label(
                timestamp_frame, text=timestamp_text, font=self.timestamp_font,
                bg=self.CHAT_AREA_BG_COLOR, fg="grey", pady=0
            )
            timestamp_label.pack(anchor=tk.S)

        self.chat_display_frame.update_idletasks()
        self.chat_canvas.config(scrollregion=self.chat_canvas.bbox("all"))
        self.root.after(50, lambda: self.chat_canvas.yview_moveto(1.0))  # Tăng delay một chút
        return align_frame

    _typing_animation_after_id = None

    def animate_typing_indicator(self):
        if hasattr(self, '_typing_animation_after_id') and self._typing_animation_after_id:
            self.root.after_cancel(self._typing_animation_after_id)
        self._typing_animation_after_id = None

        if hasattr(self, 'typing_indicator_bubble_canvas') and self.typing_indicator_bubble_canvas.winfo_exists():
            text_item_id = None
            all_items = self.typing_indicator_bubble_canvas.find_all()
            for item_id in all_items:
                if self.typing_indicator_bubble_canvas.type(item_id) == "text":
                    text_item_id = item_id
                    break

            if text_item_id:
                dots = ["Trợ lý đang soạn", "Trợ lý đang soạn.", "Trợ lý đang soạn..", "Trợ lý đang soạn..."]
                try:
                    current_text = self.typing_indicator_bubble_canvas.itemcget(text_item_id, "text")
                    next_index = (dots.index(current_text) + 1) % len(dots) if current_text in dots else 0
                    self.typing_indicator_bubble_canvas.itemconfig(text_item_id, text=dots[next_index])
                    self._typing_animation_after_id = self.root.after(500, self.animate_typing_indicator)
                except (tk.TclError, ValueError):  # Bắt lỗi nếu widget bị hủy hoặc text không có trong dots
                    if hasattr(self, '_typing_animation_after_id') and self._typing_animation_after_id:
                        self.root.after_cancel(self._typing_animation_after_id)
                    self._typing_animation_after_id = None
                    return
            else:
                print("Warning: Typing indicator text item not found on canvas.")
        else:
            if hasattr(self, '_typing_animation_after_id') and self._typing_animation_after_id:
                self.root.after_cancel(self._typing_animation_after_id)
            self._typing_animation_after_id = None

    def show_typing_indicator(self):
        self.remove_typing_indicator()
        if not (hasattr(self,
                        'typing_indicator_frame') and self.typing_indicator_frame and self.typing_indicator_frame.winfo_exists()):
            self.typing_indicator_frame = self.add_message_to_display("", "assistant", show_typing=True)

    def remove_typing_indicator(self):
        if hasattr(self, '_typing_animation_after_id') and self._typing_animation_after_id:
            self.root.after_cancel(self._typing_animation_after_id)
        self._typing_animation_after_id = None

        if hasattr(self,
                   'typing_indicator_frame') and self.typing_indicator_frame and self.typing_indicator_frame.winfo_exists():
            self.typing_indicator_frame.destroy()
        self.typing_indicator_frame = None

        if hasattr(self, 'typing_indicator_bubble_canvas'):
            delattr(self, 'typing_indicator_bubble_canvas')

        self.chat_display_frame.update_idletasks()
        self.chat_canvas.config(scrollregion=self.chat_canvas.bbox("all"))

    # Xử lý sự kiện nhập request từ người dùng
    def send_message_event_handler(self, event=None):
        user_text = self.user_input_entry.get().strip()
        if not user_text or user_text == "Nhập câu hỏi của bạn...":
            return

        self.add_message_to_display(user_text, "user")
        self.user_input_entry.delete(0, tk.END)
        self.user_input_entry.focus_set()

        self.show_typing_indicator()
        self.send_button.config(state=tk.DISABLED)

        thread = threading.Thread(target=self.get_bot_response_threaded,
                                  args=(user_text, list(messages)))
        thread.daemon = True
        thread.start()

    def get_bot_response_threaded(self, user_text, conversation_history):
        try:
            bot_reply = chat_with_model(user_text, conversation_history)
        except Exception as e:
            print(f"Lỗi trong luồng lấy phản hồi từ bot: {e}")
            bot_reply = "Xin lỗi, đã có lỗi xảy ra trong quá trình xử lý. Vui lòng thử lại."
        finally:
            self.root.after(0, self.update_ui_after_response, bot_reply)

    def update_ui_after_response(self, bot_reply):
        self.remove_typing_indicator()
        self.add_message_to_display(bot_reply, "assistant")
        self.send_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    if not initialize_openai_client():
        print("LỖI: Không thể khởi tạo Azure OpenAI client.")
        root_error_check = tk.Tk()
        root_error_check.withdraw()
        messagebox.showerror("Lỗi Khởi Tạo Client",
                             "Không thể khởi tạo Azure OpenAI client. Vui lòng kiểm tra API key, endpoint, API version trong backend.py và kết nối mạng.")
        root_error_check.destroy()
        exit()

    root = tk.Tk()
    app = ModernChatbotUI(root)  # __init__ sẽ canh giữa cửa sổ với 850x650
    root.minsize(750, 550)  # Sau đó đặt kích thước tối thiểu có thể co dãn
    root.mainloop()