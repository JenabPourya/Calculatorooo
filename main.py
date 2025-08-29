from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.core.window import Window
import math
import json
import os

class Calculator(BoxLayout):
    result_preview = StringProperty("")
    theme_mode = StringProperty("system")
    current_language = StringProperty("fa")
    translations = ObjectProperty({})
    history = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_translations()
        self.apply_theme()

    def load_translations(self):
        """بارگذاری ترجمه‌ها از فایل JSON"""
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_path, "assets", "translations.json")
            with open(path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            self.translations = {}
            print("⚠️ فایل ترجمه پیدا نشد.")

    def translate(self, key):
        """دریافت ترجمه بر اساس زبان فعلی"""
        return self.translations.get(self.current_language, {}).get(key, key)

    def on_input_change(self, text):
        """نمایش پیش‌نمایش محاسبه هنگام تایپ"""
        try:
            preview = eval(text, {"__builtins__": None}, math.__dict__)
            self.result_preview = str(round(preview, 6))
        except:
            self.result_preview = ""

    def calculate(self):
        """انجام محاسبه اصلی"""
        try:
            expr = self.ids.input.text.strip()
            result = eval(expr, {"__builtins__": None}, math.__dict__)
            self.ids.output.text = str(round(result, 6))
            self.history.append(f"{expr} = {result}")
        except:
            self.ids.output.text = self.translate("error")

    def change_language(self, lang_code):
        """تغییر زبان رابط کاربری"""
        self.current_language = lang_code
        self.ids.output.text = ""
        self.result_preview = ""

    def change_theme(self, mode):
        """تغییر حالت تم"""
        self.theme_mode = mode
        self.apply_theme()

    def apply_theme(self):
        """اعمال رنگ‌بندی تم"""
        if self.theme_mode == "dark":
            Window.clearcolor = (0.1, 0.1, 0.1, 1)
        elif self.theme_mode == "light":
            Window.clearcolor = (1, 1, 1, 1)
        else:
            Window.clearcolor = (0.95, 0.95, 0.95, 1)

    def show_history(self):
        """نمایش تاریخچه محاسبات"""
        hist_text = "\n".join(self.history[-10:]) or self.translate("no_history")
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        popup = Popup(title=self.translate("history"),
                      content=Label(text=hist_text),
                      size_hint=(0.8, 0.6))
        popup.open()

class CalcApp(App):
    def build(self):
        return Calculator()

if __name__ == "__main__":
    CalcApp().run()
