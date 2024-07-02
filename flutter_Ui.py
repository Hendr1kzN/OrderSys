import flet as ft
from UI_Elements.show_order import OrderView
from UI_Elements.view_with_menue_items import MenueView
from order_operations import ItemsInOrder


def main(page):
    page.session.set("current_table", None)
    page.title = "App Example"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    page.dark_theme = ft.theme.Theme(color_scheme_seed="white")

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.RESTAURANT_MENU_ROUNDED, label="Menu"),
            ft.NavigationBarDestination(icon=ft.icons.TABLE_RESTAURANT_ROUNDED, label="Tables"),
        ],
    )
    def set_table_number(event) -> None:
        page.session.set("current_table", event.control.value)
        page.session.set("current_order", ItemsInOrder())

    def change_view(route):
        page.views.clear()
        if page.session.get("current_table") is None:
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.AppBar(title=ft.Text("Select Table"), bgcolor=ft.colors.SURFACE_VARIANT, automatically_imply_leading=False),
                        ft.TextField(label="table number", on_blur=set_table_number),
                        ft.TextButton(text="Submit", on_click=change_view),
                    ],
                )
            )
        elif page.navigation_bar.selected_index == 0 or page.navigation_bar.selected_index is None:
            page.views.append(MenueView("/menue", "Menue", page.navigation_bar, page.session.get("current_order")).build())

        elif page.navigation_bar.selected_index == 1:
                page.views.append(OrderView("/order", "Order", page.navigation_bar, page.session.get("current_order")).build())
        page.update()
    
    page.on_route_change = change_view
    page.navigation_bar.on_change = change_view
    page.update()

    change_view("/")

ft.app(target=main)