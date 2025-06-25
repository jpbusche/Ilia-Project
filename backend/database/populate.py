from hashlib import md5
import random

from models.product import Products


def populate_database():
    f = open("database/database_populate.csv", "r")
    for line in f.readlines():
        line = line.replace("\n", "").split(",")
        try:
            product = Products(
                product_id = md5(f"{line[2]} ({line[1]})".encode()).hexdigest(),
                name = line[2],
                price = float(line[5]),
                quantity = random.randint(0, 100),
                rarity = line[-1].replace("\n", ""),
                collection = "Amigos de Jornada",
                image_link = line[4]
            )
            product.save()
        except Exception:
            pass