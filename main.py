from kivy.app import App
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.relativelayout import RelativeLayout

Builder.load_file('gui.kv')

class FunkyButton(Button):
    def __init__(self, size_hint, pos_hint):
        super().__init__(pos_hint=pos_hint,size_hint=size_hint, text ="Hello World")

class MyPaintApp(App):
    def build(self):
        parent = RelativeLayout(size =(300, 300))
        parent.add_widget(FunkyButton((.5, .2), {'center_x':.5, 'center_y':.5}))
        return parent

    def change_color(self, obj):
        pass

if __name__ == '__main__':
    MyPaintApp().run()