import flet as ft
from data_model import Category

class Publisher:
    def __init__(self):
        self._observers = set()

    def notify(self):
        for observer in self._observers:
            observer.changed(self)

    def attach(self, observer):
        self._observers.add(observer)

    def detach(self, observer):
        self._observers.discard(observer)


class ProductCategorie(ft.UserControl, Publisher):
    def __init__(self, categorie: Category):
        super().__init__()
        self.category :str = categorie
        self.is_active = False
        self._button = ft.ElevatedButton(self.category.name, on_click=self.show_items_with_tag,)
        
    def build(self):
        return ft.Card(
            content=ft.Container(
                content=self._button,
                width=250,
                padding=10,
            ),
            height=70
        )
    
    def show_items_with_tag(self, button):
        self.is_active = not self.is_active
        if self.is_active:
            self._button.elevation = 100
        else:
            self._button.elevation = 0
        self.notify()
        self.update()
        