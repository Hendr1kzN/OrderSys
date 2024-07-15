import flet as ft
from order_operations import ProductItem
from publisher import Publisher


class OrderItem(ft.ExpansionPanel, Publisher):
    def __init__(self, id, product_item: ProductItem):
        self.product_item = product_item
        self.product = self.product_item.get_product()
        self.id = id
        self.addon = product_item.addon_text
        ft.ExpansionPanel.__init__(self, 
                                    header = ft.ListTile(title=ft.Text(f"{self.product.name}, {self.product_item.size.size}")),
                                    can_tap_header=True,
                                    content=ft.ListTile(
                                        title=ft.TextField(label="Zusätzlich", value=self.addon, on_change=self.saving),
                                        trailing=ft.IconButton(ft.icons.DELETE, on_click=self.open_dialoge),
                                    ))
        Publisher.__init__(self)
        self.create_alert()
    
    def saving(self, field):
        self.product_item.set_addon_text(field.control.value) 
    
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
