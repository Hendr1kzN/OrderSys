import flet as ft
from UI_Elements.item import Item
from UI_Elements.product_category import ProductCategorie
from UI_Elements.view_with_menue_items import MenueView
from order_operations import load_categorys_and_products


def main(page):
    page.session.set("current_table", None)
    page.title = "App Example"
    page.window_width = 256
    page.window_height = 512
    page.window_resizable = True
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.RESTAURANT_MENU_ROUNDED, label="Menu"),
            ft.NavigationDestination(icon=ft.icons.TABLE_RESTAURANT_ROUNDED, label="Tables"),
        ],
    )
    def set_table_number(event) -> None:
        page.session.remove("current_table")
        page.session.set("current_table", event.control.value)

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
            page.views.append(MenueView("/menue", "Menue", navigation_bar=page.navigation_bar).build())

        elif page.navigation_bar.selected_index == 1:
                page.views.append(
                    ft.View(
                        "/order",
                        [
                            ft.AppBar(title=ft.Text("Tables"), actions=[ft.TextButton("Send order")], bgcolor=ft.colors.SURFACE_VARIANT, automatically_imply_leading=False),
                            page.navigation_bar,
                        ],
                    )
                )
        page.update()
    
    page.on_route_change = change_view
    page.navigation_bar.on_change = change_view
    page.update()

    change_view("/")

ft.app(target=main)