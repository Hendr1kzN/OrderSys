import flet as ft
from UI_Elements.item import Item
from data_model import Category
from order_operations import ItemFilter, ItemsInOrder, load_categorys
from UI_Elements.product_category import ProductCategorie

class MenueView(ft.UserControl):
    def __init__(self, route:str, title:str, navigation_bar:ft.NavigationBar|None):
        super().__init__()
        self.item_filter = ItemFilter()
        self.order = ItemsInOrder()
        self.route = route
        self.app_bar = ft.AppBar(title=ft.Text(title),
                                actions=[ft.TextButton(text="Reset", on_click=self.reset_categorys)],
                                bgcolor=ft.colors.SURFACE_VARIANT,
                                automatically_imply_leading=False)
        self._load_categoryies()
        self._load_items()
        self.listView = ft.ListView(expand=1, spacing=0, padding=0, controls=self._combine_categories_and_items())
        if navigation_bar:
            self.navigation_bar = navigation_bar
    
    def _combine_categories_and_items(self):
        return list(self.categories.values()) + self.items

    def reset_categorys(self, e):
        self.item_filter.reset_categorys()
        self._load_categoryies()
        self.change_controls()

    def _load_categoryies(self):
        self.categories = {}
        for category in load_categorys():
            current = ProductCategorie(category)
            self.categories[category.id] = current
            current.attach(self)
    
    def _load_items(self):
        self.items = []
        for item in self.item_filter.sort_by_categories():
            self.items.append(Item(item))
            self.items[-1].attach(self)

    def build(self):
        self.view = ft.View(
            self.route,
            scroll=ft.ScrollMode.AUTO,
            appbar=self.app_bar,
            controls=[self.listView],
            navigation_bar=self.navigation_bar
        )
        return self.view
    
    def changed(self, category_or_item):
        if type(category_or_item) == ProductCategorie:
            if category_or_item.is_active:
                self.add_category(category_or_item.category)
            else:
                self.remove_category(category_or_item.category)
        else:
            pass #TODO: order item

    def change_controls(self):
        self._load_items()
        self.change_categories()
        self.listView.controls = self._combine_categories_and_items()
        self.listView.update()

    def add_category(self, category: Category):
        self.item_filter.add_category_to_sort_by(category.id)
        self.change_controls()
    
    def remove_category(self, category: Category):
        self.item_filter.remove_category_from_search(category.id)
        self.change_controls()
    
    def change_categories(self):
        categories = self.item_filter.return_valid_categories()
        all_ids = set()
        for categorie in categories:
            if categorie.id not in self.categories:
                new_categorie = ProductCategorie(categorie)
                self.categories[categorie.id] = new_categorie
                new_categorie.attach(self)
            all_ids.add(categorie.id)
        keys = set(self.categories.keys())
        result = keys - all_ids
        for e in result:
            self.categories.pop(e)
        
            
    