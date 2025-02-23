'''Here should the operations for the frontend be'''
from ast import Set
from data_model import Category
import db_actions
from iddict import IDDict

class ItemFilter:
    def __init__(self) -> None:
        self.categories : Set[Category] = set()

    def add_category_to_sort_by(self, category: Category):
        self.categories.add(category)

    def remove_category_from_search(self, category: Category):
        self.categories.discard(category)

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
        self.product = db_actions.get_product_of_size(self.size)
    
    def get_product(self):
        return self.product
    
    def set_addon_text(self, text):
        self.addon_text = text

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
    
    def _return_values_as_list(self):
        return list(self._items.values())

    def finish_order(self, table_number):
        return db_actions.create_order(table_number, self._return_values_as_list())

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