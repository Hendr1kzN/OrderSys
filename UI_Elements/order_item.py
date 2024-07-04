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
                                        trailing=ft.IconButton(ft.icons.DELETE, on_click=self.open_dialoge),
                                    ))
        Publisher.__init__(self)
        self.create_alert()
    
    def saving(self, field):
        self.addon = field.control.value
    
    def create_alert(self):
        self.dlg_window = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text(f"Do you really want to delete {self.product.name}?"),
        actions=[
            ft.TextButton("Yes", on_click=self.remove_item),
            ft.TextButton("No", on_click=self.close_dialoge),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    
    def open_dialoge(self, e):
        self.page.open(self.dlg_window)

    def close_dialoge(self, e):
        self.page.close(self.dlg_window)

    def remove_item(self, e):
        self.close_dialoge(e)
        self.parent.controls.remove(self)
        self.notify()
