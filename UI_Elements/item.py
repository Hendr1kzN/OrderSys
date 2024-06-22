import flet as ft
from data_model import Product
from publisher import Publisher

class Item(ft.UserControl, Publisher):
    def __init__(self, produkt:Product, item_id:int = -1):
        super().__init__()
        self.item_name = produkt.name
        self.info = produkt.info
        self.item_id = item_id

    def plus_click(self, e):
        self.notify()
    
    def build(self):
        self.item = ft.Card(
            content=ft.Container(
                content=ft.Text(self.item_name),
                alignment=ft.alignment.center,
                width=250,
                padding=10,
                ink=True,
                on_click=self.notify,
            ),
            height=70
        )
        return self.item