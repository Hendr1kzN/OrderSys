import flet as ft
from UI_Elements.order_view import OrderView
from UI_Elements.table_selection_view import SelectionView
from UI_Elements.view_with_menue_items import MenueView


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

    def change_view(route):
        page.views.clear()
        if page.session.get("current_table") is None:
            page.views.append(SelectionView("/", change_view, page.session))
        elif page.navigation_bar.selected_index == 0 or page.navigation_bar.selected_index is None:
            page.views.append(MenueView("/menue", "Menue", page.navigation_bar, page.session).build())
        elif page.navigation_bar.selected_index == 1:
            page.views.append(OrderView("/order", "Order", page.navigation_bar, page.session).build())
        page.update()
    
    page.on_route_change = change_view
    page.navigation_bar.on_change = change_view
    page.on_view_pop = change_view
    page.update()

    change_view("/")

ft.app(target=main)