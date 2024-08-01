import flet as ft
from db_actions import get_all_categorys


class ProductTab(ft.Tab):
    def __init__(self):
        self._generate_product_form()
        super().__init__(text="Produkte", content=self.content)
        self._generate_product_form()
        
    def _generate_product_form(self):
        self.generate_search_bar()
        categories = set()
        def add_to_categories(e):
            if self.search_bar.value in categories:
                return
            categories.add(self.search_bar.value)
            selected_categories.controls.append(ft.Chip(label=ft.Text(self.search_bar.value),
                                                         leading=ft.Icon(ft.icons.DELETE_ROUNDED),
                                                         data=self.search_bar.data,
                                                         on_click=delete_categorie))
            self.update()
        
        def delete_categorie(e):
            value = e.control.label.value
            selected_categories.controls.remove(e.control)
            categories.remove(value)
            self.update()
        
        self.content=ft.Column(controls=[
            ft.TextField(label="Produkt Name"),
            ft.TextField(label="Info",),
            ft.Row(
            [self.search_bar,
            ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_to_categories)]),
            selected_categories := ft.Row(),
            ft.FloatingActionButton(text="Variante/Preis hinzufügen", icon=ft.icons.ADD),
            ft.Row([ft.ElevatedButton(text="Abbrechen"), ft.ElevatedButton(text="Hinzufügen")],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN)], 
            spacing=20
        )
    
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