import flet as ft
from data_model import Product
from publisher import Publisher

class Item(ft.UserControl, Publisher):
    def __init__(self, produkt:Product):
        super().__init__()
        self.item_name = produkt.name
        self.info = produkt.info

    def click(self, e):
        self.notify()
        
    
    def build(self):
        self.item = ft.Card(
            content=ft.Container(
                content=ft.Text(self.item_name),
                alignment=ft.alignment.center,
                
                width=250,
                padding=10,
                ink=True,
                on_click=self.click,
            ),
            color=ft.colors.LIGHT_BLUE_100,
            height=70
        )
        return self.item
    
    #def build(self):
    #    self.item = ft.Card(
    #        content=ft.Dismissible(
    #            content=ft.Container(
    #                content=ft.Text(self.item_name),
    #                alignment=ft.alignment.center,
    #                width=250,
    #                padding=10,
    #                ink=True,
    #                on_click=self.click,
    #            ),
    #        ),
    #        height=70
    #    )