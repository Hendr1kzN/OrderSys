'''Here should the operations for the frontend be'''
from ast import Set
from data_model import Product
from db_actions import get_all_categorys, get_all_products, get_products_with_given_categories, get_categorys_valid_with_current
from iddict import IDDict

def order():
    pass #TODO: make it so you can send a order to an other device and database

def load_categorys():
    return [category for category in get_all_categorys()]

def load_categorys_and_products():
    categorys = get_all_categorys()
    products = get_all_products()
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
            query_result = get_all_products()
        else:
            query_result = get_products_with_given_categories(self.categories)
        return [element for element in query_result]
    
    def return_valid_categories(self):
        if self.are_categories_emtpy():
            result = get_all_categorys()
        else:
            result = get_categorys_valid_with_current(self.categories)
        return [e for e in result]

    def are_categories_emtpy(self):
        return len(self.categories) <= 0

    def reset_categorys(self):
        self.categories = set()


class ItemsInOrder:
    def __init__(self) -> None:
        self._items = IDDict()
    
    def add_item(self, item: Product):
        return self._items.set(item)
    
    def remove_item(self, item_id):
        self._items.pop(item_id)
    
    def return_items(self):
        return self._items.items()

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
