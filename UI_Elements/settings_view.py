import flet as ft

class SettingsView(ft.UserControl):
    def __init__(self, route:str, title:str, submit_action):
        super().__init__()
        self.view = ft.View(
            route,
            scroll=ft.ScrollMode.AUTO,
            appbar=ft.AppBar(title=ft.Text(title),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    actions=[ft.TextButton("Close Settings", on_click=submit_action)],
                    automatically_imply_leading=False),
            controls=[],
        ) #TODO: build 2 lists to add categories and products and list them below

    def build(self):
        return self.view
    