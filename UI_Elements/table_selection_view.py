import flet as ft
from order_operations import ItemsInOrder


class SelectionView(ft.View):
    def __init__(self, route, submit_action, page_session):
        self.page_session = page_session
        super().__init__(
                    route=route,
                    controls=[
                                ft.AppBar(title=ft.Text("Select Table"), bgcolor=ft.colors.SURFACE_VARIANT, automatically_imply_leading=False),
                                ft.TextField(label="table number", on_blur=self.set_table_number),
                                ft.TextButton(text="Submit", on_click=submit_action),
                            ],
                )
        
    def set_table_number(self, event) -> None:
        self.page_session.set("current_table", event.control.value)
        self.page_session.set("current_order", ItemsInOrder())