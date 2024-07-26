import flet as ft

from db_actions import get_all_categorys

class SettingsView(ft.View):
    def __init__(self, route:str, title:str, submit_action):
        self.generate_forms()
        super().__init__(route,
            scroll=ft.ScrollMode.AUTO,
            appbar=ft.AppBar(title=ft.Text(title),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    actions=[ft.TextButton("Close Settings", on_click=submit_action)],
                    automatically_imply_leading=False),
            controls=[self.add_item_tab],)
        
    def generate_forms(self):
        self._generate_category_form()
        self._generate_product_form()
        self.add_item_tab = ft.Tabs(tabs=[self.product_form, self.category_form])

    def _generate_product_form(self):
        def close_searchbar(e):
            result = e.control.data
            search_bar.close_view(result.name)

        def open_searchbar(e):
            search_bar.open_view()

        def add_to_categories(e): #TODO: make it to not have duplicates in the categories, extract the tabs in seperate classes
            selected_categories.controls.append(ft.Chip(label=ft.Text(search_bar.value), leading=ft.Icon(ft.icons.DELETE_ROUNDED),data=search_bar.data ,on_click=lambda _ : print("clicked")))
            self.update()
        
        self.product_form = ft.Tab(text="Produkte",
            content=ft.Column(controls=[
                ft.TextField(label="Produkt Name"),
                ft.TextField(label="Info",),
                ft.Row(
                [search_bar := ft.SearchBar(view_elevation=4, 
                             bar_hint_text="Suche Kategorie",
                             view_hint_text="Wähle eine oder mehrere Kategorien aus.",
                             on_submit=None,
                             on_tap=open_searchbar,
                             controls=[ft.ListTile(title=ft.Text(f"{category.name}"),on_click=close_searchbar, data=category) for category in get_all_categorys()],
                             ),
                ft.FloatingActionButton(icon=ft.icons.ADD, on_click=add_to_categories)]),
                selected_categories := ft.Row(),
                ft.FloatingActionButton(text="Variante/Preis hinzufügen", icon=ft.icons.ADD),
                ft.Row([ft.ElevatedButton(text="Abbrechen"), ft.ElevatedButton(text="Hinzufügen")],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ],
            spacing=20))
        
    def _generate_category_form(self): #TODO: scrape all data
        self.category_form = ft.Tab(text="Kategorie", 
            content=ft.Column(controls=[
                ft.TextField(label="Kategorie Name"),
                ft.Row([
                    ft.ElevatedButton(text="Abbrechen"),
                    ft.ElevatedButton(text="Hinzufügen")],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ]))

if __name__ == "__main__":
    def main(page):
        page.title = "Test Sesstings View"
        page.views.append(SettingsView("/", "Settings", None))
        page.update()

    ft.app(target=main)