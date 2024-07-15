'''Here should the operations for the frontend be'''
from ast import Set
from data_model import OrderedProduct, Product
import db_actions
from iddict import IDDict
    

def load_categorys():
    return [category for category in db_actions.get_all_categorys()]

def load_categorys_and_products():
    categorys = db_actions.get_all_categorys()
    products = db_actions.get_all_products()
    return categorys, products

class ItemFilter:
    def __init__(self) -> None:
        self.categories : Set[int] = set()

    def add_category_to_sort_by(self, category_id: int):
        self.categories.add(category_id)

    def remove_category_from_search(self, category_id: int):
        self.categories.discard(category_id)

    def sort_by_categories(self):
        if len(self.categories) <= 0:
            query_result = db_actions.get_all_products()
        else:
            query_result = db_actions.get_products_with_given_categories(self.categories)
        return [element for element in query_result]
    
    def return_valid_categories(self):
        if self.are_categories_emtpy():
            result = db_actions.get_all_categorys()
        else:
            result = db_actions.get_categorys_valid_with_current(self.categories)
        return [e for e in result]

    def are_categories_emtpy(self):
        return len(self.categories) <= 0

    def reset_categorys(self):
        self.categories = set()

class ProductItem:
    def __init__(self, size, addon_text: str | None = "") -> None:
        self.size = size
        self.addon_text = addon_text
    
    def get_product(self):
        return self.size.product
    
    def set_addon_text(self, text):
        self.addon_text = text
    
    def create_ordered_product(self, order):
        return OrderedProduct(self.size, order, self.addon_text)
    
    def __str__(self) -> str:
        return f"{self.size, self.addon_text}"

class ItemsInOrder:
    def __init__(self) -> None:
        self._items = IDDict()
    
    def add_item(self, item: ProductItem):
        return self._items.set(item)
    
    def remove_item(self, item_id):
        self._items.pop(item_id)
    
    def return_items(self):
        return self._items.items()

    def return_values(self):
        return self._items.values()

    def finish_order(self, table_number):
        db_actions.create_order(table_number, list(self.return_values()))

if __name__ == "__main__":
    order = ItemsInOrder()
    print(order._items.counter)
    order.add_item("123")
    print(order._items.counter)
    print(order.return_items())
    print(order.add_item("456"))
    print(order.return_items())
    for key, item in order.return_items():
        print(key, item)
