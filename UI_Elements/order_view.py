import flet as ft
from UI_Elements.order_item import OrderItem

class OrderView(ft.UserControl):
    def __init__(self, route:str, title:str, navigation_bar:ft.NavigationBar|None, page_session):
        super().__init__()
        self.page_session = page_session
        self.ordert_items = page_session.get("current_order")
        self.listView = ft.ExpansionPanelList()
        self._load_items()
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
            return #TODO: make alert banner
        self.ordert_items.finish_order(self.page_session.get("current_table"))
        self.page_session.set("current_table", None)
        self.view.page.views.pop()
        self.view.page.update() #TODO: make it go back to the table Selection

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
    