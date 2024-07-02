import flet as ft
from data_model import Product
from publisher import Publisher

class OrderItem(ft.UserControl, Publisher):
    def __init__(self, produkt:Product):
        super().__init__()
        self.product: Product = produkt
        self.info = produkt.info
        self.dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to delete this item?"),
        actions=[
            ft.TextButton("Yes", data=True, on_click=self.handle_dlg_action_clicked),
            ft.TextButton("No", data=False, on_click=self.handle_dlg_action_clicked),
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
    )

    def click(self, e):
        self.notify()
    
    def build(self):
        self.item = ft.Card(
            content=ft.Dismissible(
                    content=ft.ListTile(title=ft.Text(self.product.name)),
                    background=ft.Container(bgcolor=ft.colors.GREEN),
                    secondary_background=ft.Container(bgcolor=ft.colors.RED),
                    width=250,
                    on_dismiss=self.handle_dismiss,
                    on_update=self.handle_update,
                    on_confirm_dismiss=self.handle_confirm_dismiss,
                    dismiss_thresholds={
                        ft.DismissDirection.END_TO_START: 0.2,
                        ft.DismissDirection.START_TO_END: 0.2,
                    },
                ),
                height=70
            )
        return self.item
    
    def handle_dismiss(self, e):
        e.control.parent.controls.remove(e.control)
        self.page.update()
    
    def handle_update(self, e: ft.DismissibleUpdateEvent):
        print(
            f"Update - direction: {e.direction}, progress: {e.progress}, reached: {e.reached}, previous_reached: {e.previous_reached}"
        )
    
    def handle_confirm_dismiss(self, e: ft.DismissibleDismissEvent):
        if e.direction == ft.DismissDirection.END_TO_START:  # right-to-left slide
            # save current dismissible to dialog's data, for confirmation in handle_dlg_action_clicked
            self.dlg.data = e.control
            self.page.open(self.dlg)
        else:  # left-to-right slide
            e.control.confirm_dismiss(True)
    
    def handle_dlg_action_clicked(self, e):
        self.page.close(self.dlg)
        self.dlg.data.confirm_dismiss(e.control.data)

    