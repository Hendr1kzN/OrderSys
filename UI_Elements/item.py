import flet as ft
from data_model import Product
from publisher import Publisher

class MenueItem(ft.Card, Publisher):
    def __init__(self, product: Product):
        super().__init__(content=ft.Container(
                content=ft.Text(product.name),
                alignment=ft.alignment.center,
                
                padding=10,
                ink=True,
                on_click=self.add_item,
            ),
            width=250,
            height=70
        )
        self.product: Product = product

    def add_item(self, e):
        if len(self.product.prices) == 1:
            self.size = self.product.prices[0]
        self.notify()
            