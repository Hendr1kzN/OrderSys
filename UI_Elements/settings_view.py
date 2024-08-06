import flet as ft
from UI_Elements.product_form import ProductTab
from db_actions import add_categorie
from data_model import create_or_reset_database

class SettingsView(ft.View):
    def __init__(self, route:str, title:str, submit_action, go_to_revenue):
        self.generate_forms()
        super().__init__(route,
            scroll=ft.ScrollMode.AUTO,
            appbar=ft.AppBar(title=ft.Text(title),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    actions=[ft.TextButton("Datenbank leeren", on_click=self.reset_all),ft.TextButton("Einstellungen schließen", on_click=submit_action), 
                             ft.IconButton(ft.icons.DATA_THRESHOLDING_OUTLINED, on_click=go_to_revenue)],
                    automatically_imply_leading=False),
            controls=[self.add_item_tab],)
        self.name = ""
        self.submit_action = submit_action
        self.generate_banner()
    
    def reset_all(self, e):
        create_or_reset_database()
        self.submit_action(e)

    def generate_forms(self):
        self._generate_category_form()
        self.product_form = ProductTab()
        self.add_item_tab = ft.Tabs(tabs=[self.product_form, self.category_form], scrollable=False, on_change=self.wrap_update_categories)
    
    def wrap_update_categories(self, e):
        self.product_form.update_categories()

    def _generate_category_form(self):
        self.category_form = ft.Tab(text="Kategorie hinzufügen", 
            content=ft.Container(ft.Column(controls=[
                ft.TextField(label="Kategorie Name", autofocus=True, on_change=self.on_name_change),
                ft.Row([
                    ft.ElevatedButton(text="Abbrechen", on_click=self._reset_category_form),
                    ft.ElevatedButton(text="Hinzufügen", on_click=self.generate_category)],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ]), 
                margin=5
                ))
    
    def on_name_change(self, e):
        self.name = e.control.value

    def _reset_category_form(self, e):
        self.category_form.content.content.controls[0].value = ""
        self.update()
    
    def generate_category(self, e):
        if self.name == "":
            self.open_banner_with_value("Es muss ein Name vergeben werden.")
            return
        if add_categorie(self.name):
            self._reset_category_form(e)
            return
        
        self.open_banner_with_value("Es existiert schon eine Kategorie mit diesem Namen.")
    
    def open_banner_with_value(self, value: str) -> None:
        self.banner.content.value = value
        self.update()
        self.page.open(self.banner)

    def generate_banner(self):
        self.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
            color=ft.colors.BLACK,
            ),
            actions=[
                ft.TextButton(text="schließen", on_click=self.close_banner),
            ],)
    
    def close_banner(self, e):
        self.page.close(self.banner)


if __name__ == "__main__":
    def main(page):
        page.title = "Test Sesstings View"
        page.views.append(SettingsView("/", "Settings", None))
        page.update()

    ft.app(target=main)