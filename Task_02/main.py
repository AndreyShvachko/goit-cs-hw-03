from pymongo import MongoClient
from bson.objectid import ObjectId

# Підключення до MongoDB
def connect_to_db():
    try:
        client = MongoClient("mongodb+srv://andrey_s:1122334455@cats.yjmzc.mongodb.net/?retryWrites=true&w=majority&appName=Cats")  # Замініть на ваш MongoDB URI, якщо використовуєте Atlas
        db = client["cats_database"]
        return db
    except Exception as e:
        print(f"Помилка: {e}")
        return None

# CREATE: Додавання нового кота
def create_cat(db, name, age, features):
    try:
        collection = db["test"]
        new_cat = {"name": name, "age": age, "features": features}
        result = collection.insert_one(new_cat)
        print(f"Додано кота з _id: {result.inserted_id}")
    except Exception as e:
        print(f"Помилка при додаванні кота: {e}")


# READ: Отримання всіх котів
def read_all_cats(db):
    try:
        collection = db["test"]
        cats = collection.find()
        print("Усі коти:")
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f"Помилка при читанні котів: {e}")


# READ: Отримання кота за ім'ям
def read_cat_by_name(db, name):
    try:
        collection = db["test"]
        cat = collection.find_one({"name": name})
        if cat:
            print(f"Кіт із ім'ям {name}: {cat}")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка при пошуку кота: {e}")


# UPDATE: Оновлення віку кота за ім'ям
def update_cat_age(db, name, new_age):
    try:
        collection = db["test"]
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count > 0:
            print(f"Вік кота {name} оновлено до {new_age} років.")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка при оновленні віку кота: {e}")


# UPDATE: Додавання нової характеристики коту
def add_cat_feature(db, name, new_feature):
    try:
        collection = db["test"]
        result = collection.update_one({"name": name}, {"$push": {"features": new_feature}})
        if result.matched_count > 0:
            print(f"До кота {name} додано характеристику: {new_feature}.")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка при додаванні характеристики: {e}")


# DELETE: Видалення кота за ім'ям
def delete_cat_by_name(db, name):
    try:
        collection = db["test"]
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Кіт із ім'ям {name} видалений.")
        else:
            print(f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(f"Помилка при видаленні кота: {e}")


# DELETE: Видалення всіх котів
def delete_all_cats(db):
    try:
        collection = db["test"]
        result = collection.delete_many({})
        print(f"Видалено {result.deleted_count} котів із бази даних.")
    except Exception as e:
        print(f"Помилка при видаленні всіх котів: {e}")


# Головна функція
def main():
    collection = connect_to_db()
    if collection is not None:  # Виправлена перевірка
        while True:
            print("\nОберіть операцію:")
            print("1. Додати кота")
            print("2. Вивести всі записи")
            print("3. Знайти кота за ім'ям")
            print("4. Оновити вік кота")
            print("5. Додати характеристику коту")
            print("6. Видалити кота за ім'ям")
            print("7. Видалити всі записи")
            print("0. Вихід")

            choice = input("Ваш вибір: ")
            
            if choice == "1":
                name = input("Введіть ім'я кота: ")
                age = int(input("Введіть вік кота: "))
                features = input("Введіть характеристики (через кому): ").split(", ")
                add_cat(collection, name, age, features)
            elif choice == "2":
                read_all_cats(collection)
            elif choice == "3":
                name = input("Введіть ім'я кота: ")
                find_cat_by_name(collection, name)
            elif choice == "4":
                name = input("Введіть ім'я кота: ")
                new_age = int(input("Введіть новий вік: "))
                update_cat_age(collection, name, new_age)
            elif choice == "5":
                name = input("Введіть ім'я кота: ")
                feature = input("Введіть нову характеристику: ")
                add_feature_to_cat(collection, name, feature)
            elif choice == "6":
                name = input("Введіть ім'я кота: ")
                delete_cat_by_name(collection, name)
            elif choice == "7":
                confirm = input("Ви впевнені? Введіть 'так', щоб підтвердити: ")
                if confirm.lower() == "так":
                    delete_all_cats(collection)
            elif choice == "0":
                print("Програма завершена.")
                break
            else:
                print("Неправильний вибір, спробуйте ще раз.")
    else:
        print("Не вдалося підключитися до бази даних.")


if __name__ == "__main__":
    main()