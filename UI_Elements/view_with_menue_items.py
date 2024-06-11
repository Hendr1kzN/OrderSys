import flet as ft
from UI_Elements.item import Item
from UI_Elements.product_category import ProductCategorie
from data_model import Category, Product

class PageViewOfProducts:
    def __init__(self, route:str, title:str, actions:list, categorys:list[Category], products:list[Product], navigation_bar:ft.NavigationBar|None):
        self.route = route
        self.app_bar = ft.AppBar(title=ft.Text(title), actions=actions, bgcolor=ft.colors.SURFACE_VARIANT, automatically_imply_leading=False)
        self.ui_elements = [ProductCategorie(category) for category in categorys] #TODO: build something so that the View can access its items and categories or gets notified 
        self.ui_elements += [Item(product) for product in products]
        if navigation_bar:
            self.ui_elements.append(navigation_bar)
    
    def build(self):
        self.view = ft.View(
            self.route,
            appbar=self.app_bar,
            controls=self.ui_elements
        )
        return self.view
    
    def change_controls(self, products):
        self.view.controls = [Item(product) for product in products]