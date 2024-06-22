import flet as ft
from UI_Elements.item import Item
from data_model import Category
from order_operations import ItemFilter, load_categorys
from UI_Elements.product_category import ProductCategorie

class MenueView(ft.UserControl):
    def __init__(self, route:str, title:str, *actions:list, navigation_bar:ft.NavigationBar|None):
        super().__init__()
        self.item_filter = ItemFilter()
        self.route = route
        self.app_bar = ft.AppBar(title=ft.Text(title), actions=actions, bgcolor=ft.colors.SURFACE_VARIANT, automatically_imply_leading=False)
        self.categories = []
        for category in load_categorys():
            self.categories.append(ProductCategorie(category))
            self.categories[-1].attach(self)
        
        self.items = [Item(item) for item in self.item_filter.sort_by_categorys()]
        if navigation_bar:
            self.navigation_bar = navigation_bar
    
    def build(self):
        self.view = ft.View(
            self.route,
            scroll=ft.ScrollMode.AUTO,
            appbar=self.app_bar,
            controls=self.categories+self.items,
            navigation_bar=self.navigation_bar
        )
        return self.view
    
    def changed(self, category):
        if category.is_active:
            self.add_category(category.category)
        else:
            self.remove_category(category.category)

    def change_controls(self):
        self.items = [Item(item) for item in self.item_filter.sort_by_categorys()]
        self.view.controls = self.categories+self.items
        self.view.update()

    def add_category(self, category: Category):
        self.item_filter.add_category_to_sort_by(category.id)
        self.change_controls()
    
    def remove_category(self, category: Category):
        self.item_filter.remove_category_from_search(category.id)
        self.change_controls()
