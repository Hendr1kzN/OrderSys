'''Here should the operations for the frontend be'''
from db_actions import get_all_categorys, get_all_products

def order():
    pass # TODO: make it so you can send a order to an other device

def load_categorys_and_products():
    categorys = get_all_categorys()
    products = get_all_products()
    return categorys, products

def add_category_to_sort_by(category):
    pass

def remove_category_from_search(category):
    pass

def sort_by_category(category_name):
    pass # TODO: make it sort the elements by category

if __name__ == "__main__":
    c, p = load_categorys_and_products()
    print(e.name for e in c)
