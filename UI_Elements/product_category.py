import flet as ft
from data_model import Category

class ProductCategorie(ft.UserControl):
    def __init__(self, categorie :Category):
        super().__init__()
        self.categorie :str = categorie.name
        self.is_active = False
        self.button = ft.ElevatedButton(self.categorie, on_click=self.show_items_with_tag,)
        
    def build(self):
        return ft.Card(
            content=ft.Container(
                content=self.button,
                width=250,
                padding=10,
            ),
            height=70
        )
    
    def show_items_with_tag(self, button):
        self.is_active = not self.is_active
        if self.is_active:
            self.button.elevation = 100
        else:
            self.button.elevation = 0
        self.update()