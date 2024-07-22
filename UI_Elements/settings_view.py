import flet as ft

class SettingsView(ft.View):
    def __init__(self, route:str, title:str, submit_action):
        self.generate_form()
        super().__init__(route,
            scroll=ft.ScrollMode.AUTO,
            appbar=ft.AppBar(title=ft.Text(title),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    actions=[ft.TextButton("Close Settings", on_click=submit_action)],
                    automatically_imply_leading=False),
            controls=[ft.Text("Hello world!"), self.add_item_tab],)
        
    def generate_form(self):
        self.add_item_tab = ft.Tabs(tabs=[ft.Tab(text="Produkte",
                                   content=ft.Column(controls=[
                                       ft.TextField(label="Produkt Name", hint_text="Hamburger"),
                                       ft.TextField(label="Info", hint_text="Gluten"),
                                       ft.Row(
                                       [ft.SearchBar(view_elevation=4, 
                                                    bar_hint_text="Suche Kategorie",
                                                    view_hint_text="Wähle eine oder mehrere Kategorien aus.",
                                                    controls=[ft.ListTile(title=ft.Text(f"Color {i}"), data=i) for i in range(10)],#TODO: load categories
                                                    ),#be able to add Categories
                                        ft.FloatingActionButton(icon=ft.icons.ADD)]),
                                        ft.Row(),
                                        ft.FloatingActionButton(text="Variante/Preis hinzufügen", icon=ft.icons.ADD),
                                        ft.Row([ft.ElevatedButton(text="Abbrechen"), ft.ElevatedButton(text="Hinzufügen")],
                                               alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

                                   ]))])


if __name__ == "__main__":
    def main(page):
        page.title = "Test Sesstings View"
        page.views.append(SettingsView("/", "Settings", None))
        page.update()

    ft.app(target=main)