import flet as ft
from data_model import Product
from publisher import Publisher


class OrderItem(ft.ExpansionPanel, Publisher):
    def __init__(self, id, product: Product):
        self.product = product
        self.id = id
        self.addon = ""
        ft.ExpansionPanel.__init__(self, 
                                    header = ft.ListTile(title=ft.Text(self.product.name)),
                                    can_tap_header=True,
                                    content=ft.ListTile(
                                        title=ft.Text(self.product.info),
                                        subtitle=ft.TextField(label="Zusätzlich", value=self.addon, on_change=self.saving),
                                        trailing=ft.IconButton(ft.icons.DELETE, on_click=self.remove_item),
                                    ))
        Publisher.__init__(self)
    
    def saving(self, field):
        self.addon = field.control.value
    
    def remove_item(self, e):
        self.parent.controls.remove(self)
        self.notify()
