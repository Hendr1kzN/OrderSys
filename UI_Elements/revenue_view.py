import flet as ft
from UI_Elements.revenue_box import DayRevenue
import db_actions

class RevenueView(ft.View):
    def __init__(self, route:str, title:str, submit_action):
        super().__init__(route,
            scroll=ft.ScrollMode.AUTO,
            appbar=ft.AppBar(title=ft.Text(title),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    actions=[ft.TextButton("Zurück", on_click=submit_action)],
                    automatically_imply_leading=False),
            )
        self.submit_action = submit_action
        self.show_data()
    
    def show_data(self):
        all_revenue = db_actions.get_total_revenue()
        info = DayRevenue("alle Einnahmen", f"{all_revenue:.2f}€")
        self.controls.append(info)


if __name__ == "__main__":
    def main(page):
        page.title = "Test Sesstings View"
        page.views.append(RevenueView("/", "Settings", None))
        page.update()

    ft.app(target=main)