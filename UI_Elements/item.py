import flet as ft
from data_model import Product
from publisher import Publisher

class MenueItem(ft.UserControl, Publisher):
    def __init__(self, produkt: Product):
        super().__init__()
        self.product: Product = produkt

    def click(self, e):
        self.notify()
        
    def build(self):
        self.item = ft.Card(
            content=ft.Container(
                content=ft.Text(self.product.name),
                alignment=ft.alignment.center,
                
                width=250,
                padding=10,
                ink=True,
                on_click=self.click,
            ),
            height=70
        )
        return self.item