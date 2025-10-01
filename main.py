from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.window import Window
import math
import json

class Calculator(BoxLayout):
    result_preview = StringProperty("")
    theme_mode = StringProperty("system")
    current_language = StringProperty("en")
    translations = ObjectProperty({})
    history = []
    def show_history(self):
        hist_text = "\n".join(self.history[-10:]) or self.translate("no_history")
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        popup = Popup(title=self.translate("history"), content=Label(text=hist_text), size_hint=(0.8, 0.6))
        popup.open()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_translations()
        self.apply_theme()

    def load_translations(self):
        with open("assets/translations.json", "r", encoding="utf-8") as f:
            self.translations = json.load(f)

    def translate(self, key):
        return self.translations.get(self.current_language, {}).get(key, key)

    def on_input_change(self, text):
        try:
            preview = eval(text, {"__builtins__": None}, math.__dict__)
            self.result_preview = str(round(preview, 6))
        except:
            self.result_preview = ""

    def calculate(self):
        try:
            expr = self.ids.input.text
            result = eval(expr, {"__builtins__": None}, math.__dict__)
            self.ids.output.text = str(round(result, 6))
        except:
            self.ids.output.text = self.translate("error")

    def change_language(self, lang_code):
        self.current_language = lang_code
        self.ids.output.text = ""
        self.result_preview = ""

    def change_theme(self, mode):
        self.theme_mode = mode
        self.apply_theme()

    def apply_theme(self):
        if self.theme_mode == "dark":
            Window.clearcolor = (0.1, 0.1, 0.1, 1)
        elif self.theme_mode == "light":
            Window.clearcolor = (1, 1, 1, 1)
        else:
            Window.clearcolor = (0.95, 0.95, 0.95, 1)

from kivy.lang import Builder

class CalcApp(App):
    def build(self):
        Builder.load_file("calculator.kv")
        return Calculator()

CalcApp().run()
