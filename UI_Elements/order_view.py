import flet as ft
from UI_Elements.order_item import OrderItem
from order_operations import ItemsInOrder

class OrderView(ft.UserControl):
    def __init__(self, route:str, title:str, navigation_bar:ft.NavigationBar|None, page_session, submit_action, settings_button):
        super().__init__()
        self.page_session = page_session
        self.ordert_items = page_session.get("current_order")
        self.submit_action = submit_action
        self.listView = ft.ExpansionPanelList()
        self._load_items()
        self.create_banner()
        self.view = ft.View(
            route,
            scroll=ft.ScrollMode.AUTO,
            appbar=ft.AppBar(title=ft.Text(title),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    actions=[ft.TextButton("Bestellung beenden", on_click=self.order),
                             ft.IconButton(icon=ft.icons.SETTINGS, on_click=settings_button)],
                    automatically_imply_leading=False),
            controls=[self.listView],
            navigation_bar=navigation_bar
        )
    
    def order(self, e):
        if len(self.ordert_items.return_items()) <= 0:
            self.view.page.open(self.banner)
            return
        order = self.ordert_items.finish_order(0)
        self.show_total_modal(order)
        self.view.page.open(self.modal)
        self.page_session.set("current_order", ItemsInOrder())
        self.view.navigation_bar.selected_index = 0
    
    def show_total_modal(self, order):
        text_block = [ft.Text(value=f"{item.size_and_price.product.name}, {item.size_and_price.price}€") for item in order.ordered_products]
        text_block.append(ft.Text(value=f"{order.total:.2f}€", size=60))
        self.modal = ft.AlertDialog(modal=True,
            title=ft.Text("Last Steps"),
            content=ft.Column(text_block, horizontal_alignment=ft.CrossAxisAlignment.END),
            actions=[
                ft.TextButton("Bezahlt", on_click=self.close_and_update),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    
    def close_and_update(self, e):
        self.view.page.close(self.modal)
        self.submit_action("/")

    def close_banner(self, e):
        self.view.page.close(self.banner)

    def create_banner(self):
        action_button_style = ft.ButtonStyle(color=ft.colors.BLUE)
        self.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                value="You can't send an empty order!",
                color=ft.colors.BLACK,
            ),
            actions=[
                ft.TextButton(text="Close", style=action_button_style, on_click=self.close_banner),
            ],
        )

    def _load_items(self):
        for key, value in self.ordert_items.return_items():
            item = OrderItem(key, value)
            item.attach(self)
            self.listView.controls.append(item)

    def build(self):
        return self.view
    
    def changed(self, item: OrderItem):
        self.ordert_items.remove_item(item.id)
        self.view.update()
    