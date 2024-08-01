import flet as ft
from db_actions import get_all_categorys


class ProductTab(ft.Tab):
    def __init__(self):
        self._generate_product_form()
        super().__init__(text="Produkte", content=self.content)
        self._generate_product_form()
        
    def _generate_product_form(self):
        self.generate_search_bar()
        self.categories = set()
        def add_to_categories(e):
            if self.search_bar.value in self.categories:
                return
            self.categories.add(self.search_bar.value)
            selected_categories.controls.append(ft.Chip(label=ft.Text(self.search_bar.value),
                                                         leading=ft.Icon(ft.icons.DELETE_ROUNDED),
                                                         data=self.search_bar.data,
                                                         on_click=delete_categorie))
            self.update()
        
        def delete_categorie(e):
            value = e.control.label.value
            selected_categories.controls.remove(e.control)
            self.categories.remove(value)
            self.update()
        
        self.content=ft.Column(controls=[
            name := ft.TextField(label="Produkt Name"),
            info := ft.TextField(label="Info",),
            ft.Row(
            [self.search_bar,
            ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_to_categories)]),
            selected_categories := ft.Row(),
            ft.FloatingActionButton(text="Variante/Preis hinzufügen", icon=ft.icons.ADD),# TODO: make it posible to add variants 
            ft.Row([ft.ElevatedButton(text="Abbrechen", on_click=self.clean_all), ft.ElevatedButton(text="Hinzufügen", on_click=self.generate_product)],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN)], 
            spacing=20
        )
        self.name = name
        self.info = info
    
    def generate_search_bar(self):
        self.search_bar = ft.SearchBar(view_elevation=4, 
                            bar_hint_text="Suche Kategorie",
                            view_hint_text="Wähle eine oder mehrere Kategorien aus.",
                            on_tap=self.open_searchbar,
                            controls=[ft.ListTile(title=ft.Text(f"{category.name}"), on_click=self.close_searchbar, data=category) for category in get_all_categorys()],
                            )

    def close_searchbar(self, e):
            result = e.control.data
            self.search_bar.close_view(result.name)

    def open_searchbar(self, e):
        self.search_bar.open_view()
    
    def clean_all(self, e):
        self._generate_product_form()
        self.update()

    def generate_product(self, e):
        self.name
        self.info
        self.categories

        