import flet as ft
from order_operations import ItemsInOrder

class OrderView(ft.UserControl):
    def __init__(self, route:str, title:str, navigation_bar:ft.NavigationBar|None, ordered_items: ItemsInOrder):
        super().__init__()
        self.ordert_items = ordered_items
        self._load_items()
        self.listView = ft.ListView(expand=1, spacing=0, padding=0, controls=self.items)
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
        self.items = self.ordert_items.return_items()

    def build(self):
        return self.view
    
    def changed(self, item):
        pass #TODO: item operations
    