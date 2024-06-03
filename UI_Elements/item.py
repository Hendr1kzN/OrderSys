import flet as ft
from UI_Elements.dialoge_window import DialogeWindow


class Item(ft.UserControl):
    def __init__(self, count:int, item_name:str, info:str):
        super().__init__()
        self.item_name = item_name
        self.info = info
        self.txt_number = ft.Text(value=str(count), text_align="center", width=100)
    
    def minus_click(self, e):
        if int(self.txt_number.value) > 0:
            self.txt_number.value = str(int(self.txt_number.value) - 1)
            self.update()

    def plus_click(self, e):
        self.txt_number.value = str(int(self.txt_number.value) + 1)
        self.update()
        print("add")
    
    def build(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Text(self.item_name),
                alignment=ft.alignment.center,
                width=250,
                padding=10,
                ink=True,
                on_click=self.plus_click,
            ),
            height=70
        )
    
    def get_current_amount(self):
        return self.counter.get_value()