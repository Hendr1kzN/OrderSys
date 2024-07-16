import flet as ft
from UI_Elements.order_item import OrderItem

class OrderView(ft.UserControl):
    def __init__(self, route:str, title:str, navigation_bar:ft.NavigationBar|None, page_session, submit_action):
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
                    actions=[ft.TextButton("Order", on_click=self.order)],
                    automatically_imply_leading=False),
            controls=[self.listView],
            navigation_bar=navigation_bar
        )
    
    def order(self, e):
        if len(self.ordert_items.return_items()) <= 0:
            self.view.page.open(self.banner)
            return
        self.ordert_items.finish_order(self.page_session.get("current_table"))
        self.page_session.set("current_table", None)
        self.page_session.set("current_order", None)
        self.submit_action("/")
        
    def close_banner(self, e):
        self.view.page.close(self.banner)
        self.view.page.add(ft.Text("Action clicked: " + e.control.text))

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
    