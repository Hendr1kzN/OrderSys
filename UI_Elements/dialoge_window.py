import flet as ft


class DialogeWindow(ft.UserControl):
    def __init__(self, item_name:str, info:list[str]):
        super().__init__()
        self.item_name = item_name
        self.info = info
        self.dlg = ft.AlertDialog(
            title=ft.Text(f'Info about {self.item_name}'),
            content=(ft.Text(str(self.info))),
        )
    
    def build(self):
        return ft.IconButton(ft.icons.INFO_OUTLINE_ROUNDED, on_click=self.open_dlg, on_focus=self.open_dlg)

    def open_dlg(self, e):
        self.page.dialog = self.dlg
        self.page.dialog.open = True
        self.page.update()