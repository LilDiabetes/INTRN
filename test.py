class Car:

    def __init__(self, id, brand, model, production_date, price, quantity, *args):
        self.id = int(id)
        self.brand = brand
        self.model = model
        self.production_date = str(production_date)
        self.price = float(price)
        self.quantity = int(quantity)

    def __str__(self):
        return f"{self.id} - {self.brand} - {self.model} - {self.production_date} - $ {self.price}  {self.quantity} left"

    def check_quantity(self, chosen_quantity):
        while str(chosen_quantity) > str(self.quantity):
            chosen_quantity = input("too much bro")
        else:
            print(f"chosen quantity - {chosen_quantity} ")
            return chosen_quantity

    def decrease_quantity(self, var1):
        self.quantity = self.quantity - int(var1)
        print(f'New quantity - {self.quantity}')
        return self.quantity

    def sell_car(self):
        chosen_quantity = input("how much? ")
        while chosen_quantity.isdigit() is False:
            chosen_quantity = input("make sure to ask numbers not words ")
        else:
            var1 = self.check_quantity(chosen_quantity)
            var2 = self.decrease_quantity(var1)
            return var1, var2


class Store:

    def __init__(self, name, address, *args):
        self.name = name
        self.address = address
        self.product_list = []

    def get_car_by_id(self):
        choice = input(" please choose the product by ID ")
        e = self.product_list
        while choice.isdigit() is False:
            choice = input("make sure to ask numbers not words ")
        while choice > str(len(e)):
            self.get_product_list()
            choice = input("try again ")
        else:
            for i in e:
                if choice in str(i.id):
                    var3 = i.sell_car()
                    return i, var3[0]

    def add_car(self, list_items):
        self.product_list.append(list_items)

    def get_product_list(self):
        print(*car_shop.product_list, sep="\n")

    def remove_car(self):
        e = self.product_list
        for i in e:
            if i.quantity <= 0:
                self.product_list.remove(i)
                return e

    def buy_car(self):
        chosen_car = self.get_car_by_id()
        price = chosen_car[0].price
        quantity = chosen_car[1]
        total_price = float(price) * float(quantity)
        print(total_price)
        return total_price


item_list = [
    {
        "id": 1,
        "brand": "Toyota",
        "model": "Prius",
        "production_date": "2015/03/17",
        "price": 13212.95,
        "quantity": 7
    },
    {
        "id": 2,
        "brand": "BMW",
        "model": "e46 m3",
        "production_date": "1997/12/15",
        "price": 14212.95,
        "quantity": 3
    },
    {
        "id": 3,
        "brand": "Mazda",
        "model": "ahura",
        "production_date": "2016/03/17",
        "price": 5000,
        "quantity": 2
    }
]

car_shop = Store("boo", "goo")
mbb = [car_shop.add_car(Car(**e)) for e in item_list]
car_shop.get_product_list()
car_shop.buy_car()
car_shop.remove_car()
