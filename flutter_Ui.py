import flet as ft

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


class ProductCategorie(ft.UserControl):
    def __init__(self, categorie :str):
        super().__init__()
        self.categorie :str = categorie
        self.is_active = False
        self.button = ft.ElevatedButton(self.categorie, on_click=self.show_items_with_tag,)# highlite the button when it is pressed or make it a good checkbox
    
    def build(self):
        return ft.Card(
            content=ft.Container(
                content=self.button,
                width=250,
                padding=10,
            )
        )
    
    def show_items_with_tag(self, button): # needs to filter out all products that doesn't have those tags and all tags that aren't in any product with this tag
        self.is_active = not self.is_active
        if self.is_active:
            print("active")

def main(page):
    page.session.set("current_table", None)
    page.title = "App Example"
    page.window_width = 256
    page.window_height = 512
    page.window_resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationDestination(icon=ft.icons.RESTAURANT_MENU_ROUNDED, label="Menu"),
            ft.NavigationDestination(icon=ft.icons.TABLE_RESTAURANT_ROUNDED, label="Tables"),
        ],
    )
    def set_table_number(e):
        page.session.remove("current_table")
        page.session.set("current_table", 1)
        change_view("/")

    def change_view(route):
        page.views.clear()
        if page.session.get("current_table") == None:
            page.views.append(
                ft.View(
                    "/settable",
                    [
                        ft.AppBar(title=ft.Text("Select Table"), bgcolor=ft.colors.SURFACE_VARIANT, automatically_imply_leading=False),
                        ft.TextField(label="table number"),
                        ft.TextButton(text="Submit", on_click=set_table_number),
                        page.navigation_bar,
                    ],
                )
            )
        elif page.navigation_bar.selected_index == 0 or page.navigation_bar.selected_index == None:
            page.views.append(
                ft.View(
                    "/menue",
                    [
                        ft.AppBar(title=ft.Text("Menue Items"), bgcolor=ft.colors.SURFACE_VARIANT, automatically_imply_leading=False),
                        ProductCategorie("Drinks"),
                        Item(0, "Tee", ['Drink', 'Warm', 'Nonalkoholic']),
                        Item(0, "Coffe", ['Drink', 'Warm', 'Nonalkoholic', 'Coffenated']),
                        page.navigation_bar,
                    ],
                    
                )
            )
        elif page.navigation_bar.selected_index == 1:
                page.views.append(
                    ft.View(
                        "/order",
                        [
                            ft.AppBar(title=ft.Text("Tables"), actions=[ft.TextButton("Send order")], bgcolor=ft.colors.SURFACE_VARIANT, automatically_imply_leading=False),
                            Item(0, "Tee", ['Drink', 'Warm', 'Nonalkoholic']),
                            Item(0, "Coffe", ['Drink', 'Warm', 'Nonalkoholic', 'Coffenated']),
                            page.navigation_bar,
                        ],
                    )
                )
        page.update()
    
    page.on_route_change = change_view
    page.navigation_bar.on_change = change_view
    page.update()

    change_view("/")

ft.app(target=main)#, view=ft.WEB_BROWSER)