import flet as ft
from UI_Elements.order_item import OrderItem
from order_operations import ItemsInOrder

class OrderView(ft.UserControl):
    def __init__(self, route:str, title:str, navigation_bar:ft.NavigationBar|None, ordered_items: ItemsInOrder):
        super().__init__()
        self.ordert_items = ordered_items
        self.listView = ft.ExpansionPanelList()
        self._load_items()
        self.view = ft.View(
            route,
            scroll=ft.ScrollMode.AUTO,
            appbar=ft.AppBar(title=ft.Text(title),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    automatically_imply_leading=False),
            controls=[self.listView],
            navigation_bar=navigation_bar
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
    