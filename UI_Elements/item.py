import flet as ft
from data_model import Product
from publisher import Publisher

class MenueItem(ft.UserControl, Publisher):
    def __init__(self, product: Product):
        super().__init__()
        self.product: Product = product
        self.create_alert()
    
    def create_alert(self):
        dropdown_options = [ft.dropdown.Option(price.size) for price in self.product.prices]
        #if len(dropdown_options) == 0:
        #    dropdown_options = [ft.dropdown.Option("Normal")]

        self.dropdown = ft.Dropdown(
                width=100,
                options=dropdown_options,
                autofocus=True,
                value=dropdown_options[0].key)
        self.dlg_window = ft.AlertDialog(
        modal=True,
        title=ft.Text("Last Steps"),
        content=self.dropdown,
        actions=[
            ft.TextButton("Done", on_click=self.add_item),
            ft.TextButton("Cancel", on_click=self.close_dialoge),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        )
        
    def open_dialoge(self, e):
        self.page.open(self.dlg_window)

    def close_dialoge(self, e):
        self.page.close(self.dlg_window)

    def add_item(self, e):
        #self.close_dialoge(e)
        if len(self.product.prices) == 1:
            self.size = self.product.prices[0]
        #else:
        #    for price in self.product.prices:
        #        if price.size == self.dropdown.value:
        #            self.size = price
        #            break
        self.notify()

    def build(self):
        self.item = ft.Card(
            content=ft.Container(
                content=ft.Text(self.product.name),
                alignment=ft.alignment.center,
                
                width=250,
                padding=10,
                ink=True,
                on_click=self.add_item,
            ),
            height=70
        )
        return self.item