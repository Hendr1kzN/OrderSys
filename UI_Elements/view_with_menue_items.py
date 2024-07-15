import flet as ft
from UI_Elements.item import MenueItem
from data_model import Category
from order_operations import ItemFilter, ProductItem, load_categorys
from UI_Elements.product_category import ProductCategorie

class MenueView(ft.UserControl):
    def __init__(self, route:str, title:str, navigation_bar:ft.NavigationBar|None, page_session):
        super().__init__()
        self.item_filter = ItemFilter()
        self.page_session = page_session
        self.ordert_items = page_session.get("current_order")
        self._load_categoryies()
        self._load_items()
        self.listView = ft.ListView(expand=1, spacing=0, padding=0, controls=self._combine_categories_and_items())
        self.view = ft.View(
            route,
            scroll=ft.ScrollMode.AUTO,
            appbar=ft.AppBar(title=ft.Text(title),
                    actions=[ft.TextButton(text="Reset", on_click=self.reset_categorys)],
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    automatically_imply_leading=False),
            controls=[self.listView],
            navigation_bar=navigation_bar
        )

    def reset_categorys(self, e):
        self.item_filter.reset_categorys()
        self._load_categoryies()
        self._change_controls()

    def _load_categoryies(self):
        self.categories = {}
        for category in load_categorys():
            current = ProductCategorie(category)
            self.categories[category.id] = current
            current.attach(self)
    
    def _change_controls(self):
        self._load_items()
        self.listView.controls = self._combine_categories_and_items()
        self.listView.update()

    def _load_items(self):
        self.items = []
        for item in self.item_filter.sort_by_categories():
            self.items.append(MenueItem(item))
            self.items[-1].attach(self)

    def _combine_categories_and_items(self):
        return list(self.categories.values()) + self.items

    def build(self):
        return self.view
    
    def changed(self, category_or_item):
        if type(category_or_item) == ProductCategorie:
            if category_or_item.is_active:
                self.item_filter.add_category_to_sort_by(category_or_item.category.id)
            else:
                self.item_filter.remove_category_from_search(category_or_item.category.id)
            self._change_categories()
            self._change_controls()
        else:
            self.ordert_items.add_item(ProductItem(category_or_item.size))
    
    def _change_categories(self):
        categories = self.item_filter.return_valid_categories()
        keys_to_be_in_dict = self._add_categories_currently_missing(categories)
        keys = set(self.categories.keys())
        keys_to_remove = keys - keys_to_be_in_dict
        for e in keys_to_remove:
            self.categories.pop(e)
    
    def _add_categories_currently_missing(self, categories: list[Category]):
        all_ids = set()
        for categorie in categories:
            if categorie.id not in self.categories:
                new_categorie = ProductCategorie(categorie)
                self.categories[categorie.id] = new_categorie
                new_categorie.attach(self)
            all_ids.add(categorie.id)
        return all_ids
    