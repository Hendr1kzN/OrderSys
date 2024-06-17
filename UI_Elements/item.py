import flet as ft
from data_model import Product

class Item(ft.UserControl):
    def __init__(self, produkt:Product):
        super().__init__()
        self.item_name = produkt.name
        self.info = produkt.info
        self.txt_number = ft.Text(text_align="center", width=100)
    
    def minus_click(self, e):
        self.update()

    def plus_click(self, e):
        self.update()
        print("add")
    
    def build(self):
        self.item = ft.Card(
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
        return self.item
    
    def get_current_amount(self):
        return self.counter.get_value()
    
    def delete(self):
        del self.item