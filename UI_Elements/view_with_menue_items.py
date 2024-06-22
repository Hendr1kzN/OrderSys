import flet as ft
from UI_Elements.item import Item
from data_model import Category
from order_operations import ItemFilter, load_categorys
from UI_Elements.product_category import ProductCategorie

class MenueView(ft.UserControl):
    def __init__(self, route:str, title:str, actions:list, navigation_bar:ft.NavigationBar|None):
        super().__init__()
        self.item_filter = ItemFilter()
        self.route = route
        self.app_bar = ft.AppBar(title=ft.Text(title), actions=actions, bgcolor=ft.colors.SURFACE_VARIANT, automatically_imply_leading=False)
        self._load_categoryies()
        self._load_items()
        if navigation_bar:
            self.navigation_bar = navigation_bar
    
    def _load_categoryies(self):
        self.categories = []
        for category in load_categorys():
            self.categories.append(ProductCategorie(category))
            self.categories[-1].attach(self)
    
    def _load_items(self):
        self.items = []
        for item in self.item_filter.sort_by_categorys():
            self.items.append(Item(item))
            self.items[-1].attach(self)

    def build(self):
        self.view = ft.View(
            self.route,
            scroll=ft.ScrollMode.AUTO,
            appbar=self.app_bar,
            controls=self.categories+self.items,
            navigation_bar=self.navigation_bar
        )
        return self.view
    
    def changed(self, category_or_item):
        if category_or_item.category:
            if category_or_item.is_active:
                self.add_category(category_or_item.category)
            else:
                self.remove_category(category_or_item.category)
        else:
            pass #TODO: order item

    def change_controls(self):
        self._load_items()
        self.view.controls = self.categories+self.items
        self.view.update()

    def add_category(self, category: Category):
        self.item_filter.add_category_to_sort_by(category.id)
        self.change_controls()
    
    def remove_category(self, category: Category):
        self.item_filter.remove_category_from_search(category.id)
        self.change_controls()