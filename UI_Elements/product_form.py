import flet as ft
import re
from db_actions import create_product, get_all_categorys

class ProductTab(ft.Tab): #TODO: big refactoring
    def __init__(self):
        self._generate_product_form()
        super().__init__(text="Produkte", content=self.content)
        self._generate_product_form()
        self.generate_banner()
        self.info = None
        
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
        
        self.content=ft.Container(ft.Column(controls=[
            ft.TextField(label="Produkt Name", on_change=self.set_name, autofocus=True),
            ft.TextField(label="Info", on_change=self.set_info),
            ft.Row([
                self.search_bar,
                ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_to_categories)
            ]),
            selected_categories := ft.Row(wrap=True),
            ft.TextField(label="Preis",
                        input_filter=ft.InputFilter(regex_string=r"[0-9,.]"),
                        autofill_hints=ft.AutofillHint.TRANSACTION_AMOUNT,
                        on_change=self.set_price),
            ft.Row([ft.ElevatedButton(text="Zurücksetzen", on_click=self.clean_all), ft.ElevatedButton(text="Hinzufügen", on_click=self.generate_product)],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN)],
            spacing=20,
        ),
        margin=5)
    
    def set_name(self, e):
        self.name = e.control.value
    
    def set_info(self, e):
        self.info = e.control.value
    
    def set_price(self, e):
        if re.match(r"[0-9]+(,|.){1}[0-9]{2}", e.control.value):
            self.price = e.control.value
        else:
            self.price = ""
        
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

    def generate_banner(self):
        self.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
            value="Es muss zumindesten ein Name vergeben sein, ein Preis gesetzt sein und eine Kategorie ausgewählt sein.",
            color=ft.colors.BLACK,
            ),
            actions=[
                ft.TextButton(text="schließen", on_click=self.close_banner),
            ],)
    
    def close_banner(self, e):
        self.page.close(self.banner)

    def generate_product(self, e):
        if self._is_form_invalid():
            self.banner.content.value = "Es muss zumindesten ein Name vergeben sein, ein Preis gesetzt sein und eine Kategorie ausgewählt sein."
            self.update()
            self.page.open(self.banner)
            return
        if "," in self.price:
            self.price.replace(",", ".")
        self.name.replace(" ", "")
        success = create_product(self.name, self.info, self.price, self.categories)
        if success:
            self.clean_all(e)
            return
        
        self.banner.content.value = "Es existiert schon ein Produkt mit diesem Namen."
        self.update()
        self.page.open(self.banner)
    
    def _is_form_invalid(self):
        return len(self.categories) <= 0 or self.price == "" or self.name == ""