import flet as ft
from UI_Elements.product_form import ProductTab

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
        self.product_form = ProductTab()
        self.add_item_tab = ft.Tabs(tabs=[self.product_form, self.category_form])

        
    def _generate_category_form(self):
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