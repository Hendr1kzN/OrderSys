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

class DialogeWindow(ft.UserControl):
    def __init__(self, item_name:str, tags:list[str]):
        super().__init__()
        self.item_name = item_name
        self.tags = tags
        self.dlg = ft.AlertDialog(
            title=ft.Text(f'Info about {self.item_name}'),
            content=(ft.Text(str(", ".join(self.tags)))),
        )
    
    def build(self):
        return ft.IconButton(ft.icons.INFO_OUTLINE_ROUNDED, on_click=self.open_dlg, on_focus=self.open_dlg)

    def open_dlg(self, e):
        self.page.dialog = self.dlg
        self.page.dialog.open = True
        self.page.update()


class Item(ft.UserControl):
    def __init__(self, item_name:str, tags:list[str]):
        super().__init__()
        self.item_name = item_name
        self.tags = tags
    
    def build(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [ft.Icon(ft.icons.EMOJI_FOOD_BEVERAGE_ROUNDED), ft.Text(self.item_name), DialogeWindow(self.item_name, self.tags)],
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
        self.button = ft.ElevatedButton(self.categorie, on_click=self.show_items_with_tag())
    
    def build(self):
        return ft.Card(
            content=ft.Container(
                content=self.button,
                width=250,
                padding=10,
            )
        )
    
    def show_items_with_tag(self): # needs to filter out all products that doesn't have those tags and all tags that aren't in any product with this tag
        pass


def main(page):
    page.title = "App Example"
    page.window_width = 256
    page.window_height = 512
    page.window_resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.RESTAURANT_MENU_ROUNDED, label="Menu"),
            ft.NavigationDestination(icon=ft.icons.TABLE_RESTAURANT_ROUNDED, label="Tables"),
        ],
    )
    def change_view(route):
        page.views.clear()
        if page.navigation_bar.selected_index == 0 or page.navigation_bar.selected_index == None:
            page.views.append(
                ft.View(
                    "/menue",
                    [
                        ft.AppBar(title=ft.Text("Menue Items"), bgcolor=ft.colors.SURFACE_VARIANT, automatically_imply_leading=False),
                        ProductCategorie("Drinks"),
                        Item("Tee", ['Drink', 'Warm', 'Nonalkoholic']),
                        Item("Coffe", ['Drink', 'Warm', 'Nonalkoholic', 'Coffenated']),
                        page.navigation_bar,
                    ],
                    
                )
            )
        if page.navigation_bar.selected_index == 1:
            page.views.append(
                ft.View(
                    "/order",
                    [
                        ft.AppBar(title=ft.Text("Tables"), bgcolor=ft.colors.SURFACE_VARIANT, automatically_imply_leading=False),
                        Item("Tee", ['Drink', 'Warm', 'Nonalkoholic']),
                        Item("Coffe", ['Drink', 'Warm', 'Nonalkoholic', 'Coffenated']),
                        page.navigation_bar,
                    ],
                )
            )
        page.update()
    
    page.navigation_bar.on_change = change_view
    page.on_route_change = change_view
    page.update()

ft.app(target=main,) #view=ft.WEB_BROWSER)