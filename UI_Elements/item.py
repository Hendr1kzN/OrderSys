import flet as ft
from data_model import Product
from publisher import Publisher

class MenueItem(ft.Card, Publisher):
    def __init__(self, product: Product):
        super().__init__(content=ft.Container(
                content=ft.Text(product.name),
                alignment=ft.alignment.center,
                
                width=250,
                padding=10,
                ink=True,
                on_click=self.add_item,
            ),
            height=70
        )
        self.product: Product = product

    def add_item(self, e):
        #self.close_dialoge(e)
        if len(self.product.prices) == 1:
            self.size = self.product.prices[0]
        #else:
        #    for price in self.product.prices:
        #        if price.size == self.dropdown.value:
        #            self.size = price
        #            break
        self.notify()
            