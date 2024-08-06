import flet as ft
from publisher import Publisher

class DayRevenue(ft.Card, Publisher):
    def __init__(self, product: str, total: str):
        super().__init__(content=ft.Container(
                content=ft.Row(controls=[ft.Text(product), ft.Text(total)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                alignment=ft.alignment.center,
                
                padding=10,
                ink=True,
            ),
            width=250,
            height=70
        )

            