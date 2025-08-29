from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.window import Window
import math
import json

class Calculator(BoxLayout):
    result_preview = StringProperty("")
    theme_mode = StringProperty("system")
    current_language = StringProperty("fa")
    translations = ObjectProperty({})

history = []

def calculate(self):
    try:
        expr = self.ids.input.text  # User input
        allowed = {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "log": math.log10,
            "ln": math.log,
            "sqrt": math.sqrt,
            "pow": math.pow,
            "fact": math.factorial,
            "pi": math.pi,
            "e": math.e
        }
        result = eval(expr, {"__builtins__": None}, allowed)
        self.ids.output.text = str(round(result, 6))
        self.history.append(f"{expr} = {result}")
    except Exception as e:
        self.ids.output.text = "Error"

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

class CalcApp(App):
    def build(self):
        return Calculator()

CalcApp().run()
