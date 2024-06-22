'''Here should the operations for the frontend be'''
from ast import Set
from data_model import Product
from db_actions import get_all_categorys, get_all_products, get_products_with_given_categories

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

    def sort_by_categorys(self):
        if len(self.categories) <= 0:
            query_result = get_all_products()
        else:
            query_result = get_products_with_given_categories(self.categories)
        return [element for element in query_result]
    
    def reset_categorys(self):
        self.categories = set()

class ItemsInOrder:
    def __init__(self) -> None:
        self._items = []
    
    def add_item(self, item: Product) -> int:
        self._items.append(item)
    
    def remove_item(self, item_id): #TODO: find a better solution to remove items
        self._items.pop(item_id)
    
    def return_items(self):
        return self._items

if __name__ == "__main__":
    filter = ItemFilter()
    filter.add_category_to_sort_by(1)
    filter.add_category_to_sort_by(2)
    print(filter.sort_by_categorys())
    filter.remove_category_from_search(2)
    print(filter.sort_by_categorys())
    filter.reset_categorys()
    print(filter.categories)