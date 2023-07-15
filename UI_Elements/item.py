import flet as ft
from UI_Elements.dialoge_window import DialogeWindow


class Item(ft.UserControl):
    def __init__(self, count:int,item_name:str, tags:list[str]):
        super().__init__()
        self.item_name = item_name
        self.tags = tags
        self.txt_number = ft.Text(value=str(count), text_align="center", width=100)

    def minus_click(self, e):
        if int(self.txt_number.value) > 0:
            self.txt_number.value = str(int(self.txt_number.value) - 1)
            self.update()

    def plus_click(self, e):
        self.txt_number.value = str(int(self.txt_number.value) + 1)
        self.update()
    
    def build(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                [
                    ft.Container(
                        content=ft.Icon(ft.icons.REMOVE),
                        on_click=self.minus_click,
                        alignment=ft.alignment.center,
                        ink=True,
                        width=45
                    ),
                    ft.Column(
                        [
                            ft.Row(
                                [ft.Icon(ft.icons.EMOJI_FOOD_BEVERAGE_ROUNDED), ft.Text(self.item_name), DialogeWindow(self.item_name, self.tags)],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Row(
                                [self.txt_number],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                    ),
                    ft.Container(
                        content=ft.Icon(ft.icons.ADD),
                        on_click=self.plus_click,
                        alignment=ft.alignment.center,
                        ink=True,
                        width=45,
                        height=50
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER),
                width=250,
                padding=10,
            )
        )
    
    def get_current_amount(self):
        return self.counter.get_value()