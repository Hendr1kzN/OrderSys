import flet as ft
from data_model import Category
from publisher import Publisher

class ProductCategorie(ft.Card, Publisher):
    def __init__(self, categorie: Category):
        self.category: Category = categorie
        self.is_active = False
        self._button = ft.ElevatedButton(self.category.name, on_click=self.show_items_with_tag,)
        super().__init__( content=ft.Container(
                content=self._button,
                width=250,
                padding=10,
            ),
            height=70
        )
    
    def show_items_with_tag(self, button):
        self.is_active = not self.is_active
        if self.is_active:
            self.color = ft.colors.BLUE_400
        else:
            self.color = None
        self.notify()
        
        