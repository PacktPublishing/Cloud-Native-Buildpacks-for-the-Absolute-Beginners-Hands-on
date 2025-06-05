# models/category.py
class Category:
    @staticmethod
    def normalize(name):
        return name.strip().capitalize()
