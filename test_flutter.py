import flet as ft

class Counter(ft.UserControl):   
    def minus_click(self, e):
        if int(self.txt_number.value) > 0:
            self.txt_number.value = str(int(self.txt_number.value) - 1)
            self.update()

    def plus_click(self, e):
        self.txt_number.value = str(int(self.txt_number.value) + 1)
        self.update()

    def build(self):
        self.txt_number = ft.TextField(value="0", text_align="right", width=100)
        return ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=self.minus_click),
                self.txt_number,
                ft.IconButton(ft.icons.ADD, on_click=self.plus_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

class Item(ft.UserControl):
    def __init__(self, item_name:str):
        super().__init__()
        self.item_name = item_name
    
    def build(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [ft.Icon(ft.icons.EMOJI_FOOD_BEVERAGE_ROUNDED), ft.Text(self.item_name)],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Row(
                            [Counter()],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ]
                ),
                width=250,
                padding=10,
            )
        )

class ProductCategorie(ft.UserControl):
    def __init__(self, categorie :str):
        super().__init__()
        self.categorie :str = categorie
    
    
    def build(self):
        return ft.Card(
            content=ft.Container(
                content=ft.ElevatedButton(self.categorie, on_click=self.show_items_with_tag()),
                width=250,
                padding=10,
            )
        )
    
    def show_items_with_tag(self):
        pass
    

def main(page):
    page.title = "Card Example"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(ProductCategorie("Drinks"))
    page.add(Item("Tee"))
    page.add(Item("Coffe"))
    page.update()

ft.app(target=main)