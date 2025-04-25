# Code by Ethan Ray

todo = {}
todo2 = {}
todo3 = {}
todo4 = {}

def display_list():
    list_opt = int(input("Which list? 1-4 : "))
    if list_opt == 1:
        print(todo)
    elif list_opt == 2:
        print(todo2)
    elif list_opt == 3:
        print(todo3)
    elif list_opt == 4:
        print(todo4)
    else:
        print("That's not an option.")
        try_again = input("Try again? y/n: ")
        if try_again == "y":
            display_list()

def display_opt():
    print("Please choose an option: ")
    print("1. Add item to a list")
    print("2. Remove item from a list")
    print("3. Mark item as completed")
    print("4. Mark item as not completed")
    print("5. Display a list")
    print("6. Name a list")

def delete_obj():
    list_opt = int(input("Which list? 1-4 : "))
    if list_opt == 1:
        print(todo)
        obj_to_del = input("Delete which object? (case sensitive): ")

        try:
            del todo[obj_to_del]
            print(f"Deleted item '{obj_to_del}' successfully.")
        except KeyError:
            print(f"Item '{obj_to_del}' not found. Cannot delete.")
            try_again = input("Try again? y/n: ")
            if try_again == "y":
                delete_obj()

    elif list_opt == 2:
        print(todo2)
        obj_to_del = input("Delete which object? (case sensitive): ")

        try:
            del todo2[obj_to_del]
            print(f"Deleted item '{obj_to_del}' successfully.")
        except KeyError:
            print(f"Item '{obj_to_del}' not found. Cannot delete.")
            try_again = input("Try again? y/n: ")
            if try_again == "y":
                delete_obj()

    elif list_opt == 3:
        print(todo3)
        obj_to_del = input("Delete which object? (case sensitive): ")

        try:
            del todo3[obj_to_del]
            print(f"Deleted item '{obj_to_del}' successfully.")
        except KeyError:
            print(f"Item '{obj_to_del}' not found. Cannot delete.")
            try_again = input("Try again? y/n: ")
            if try_again == "y":
                delete_obj()

    elif list_opt == 4:
        print(todo4)
        obj_to_del = input("Delete which object? (case sensitive): ")

        try:
            del todo4[obj_to_del]
            print(f"Deleted item '{obj_to_del}' successfully.")
        except KeyError:
            print(f"Item '{obj_to_del}' not found. Cannot delete.")
            try_again = input("Try again? y/n: ")
            if try_again == "y":
                delete_obj()
    else:
        print("That's not an option.")
        try_again = input("Try again? y/n: ")
        if try_again == "y":
            delete_obj()

def mark_obj_as_completed():
    list_opt = int(input("Which list? 1-4 : "))

    if list_opt == 1:
        print(todo)
        obj_to_complete = input("Complete which item? (case sensitive): ")

        try:
            todo[obj_to_complete] = "✓"
            print(f"{obj_to_complete} completed!")
        except KeyError:
            print(f"Item '{obj_to_complete}' not found. Cannot complete.")
            try_again = input("Try again? y/n: ")
            if try_again == "y":
                mark_obj_as_completed()

    elif list_opt == 2:
        print(todo2)
        obj_to_complete = input("Complete which item? (case sensitive): ")

        try:
            todo2[obj_to_complete] = "✓"
            print(f"{obj_to_complete} completed!")
        except KeyError:
            print(f"Item '{obj_to_complete}' not found. Cannot complete.")
            try_again = input("Try again? y/n: ")
            if try_again == "y":
                mark_obj_as_completed()

    elif list_opt == 3:
        print(todo3)
        obj_to_complete = input("Complete which item? (case sensitive): ")

        try:
            todo3[obj_to_complete] = "✓"
            print(f"{obj_to_complete} completed!")
        except KeyError:
            print(f"Item '{obj_to_complete}' not found. Cannot complete.")
            try_again = input("Try again? y/n: ")
            if try_again == "y":
                mark_obj_as_completed()

    elif list_opt == 4:
        print(todo4)
        obj_to_complete = input("Complete which item? (case sensitive): ")

        try:
            todo4[obj_to_complete] = "✓"
            print(f"{obj_to_complete} completed!")
        except KeyError:
            print(f"Item '{obj_to_complete}' not found. Cannot complete.")
            try_again = input("Try again? y/n: ")
            if try_again == "y":
                mark_obj_as_completed()

    else:
        print("That's not an option.")
        try_again = input("Try again? y/n: ")
        if try_again == "y":
            mark_obj_as_completed()

def mark_obj_as_incomplete():
    list_opt = int(input("Which list? 1-4 : "))

    if list_opt == 1:
        print(todo)
        obj_to_incomplete = input("Make which item incomplete? (case sensitive): ")

        try:
            todo[obj_to_incomplete] = "X"
            print(f"{obj_to_incomplete} made incomplete!")
        except KeyError:
            print(f"Item '{obj_to_incomplete}' not found. Cannot make incomplete.")
            try_again = input("Try again? y/n: ")
            if try_again == "y":
                mark_obj_as_incomplete()

    elif list_opt == 2:
        print(todo2)
        obj_to_incomplete = input("Make which item incomplete? (case sensitive): ")

        try:
            todo2[obj_to_incomplete] = "X"
            print(f"{obj_to_incomplete} made incomplete!")
        except KeyError:
            print(f"Item '{obj_to_incomplete}' not found. Cannot make incomplete.")
            try_again = input("Try again? y/n: ")
            if try_again == "y":
                mark_obj_as_incomplete()

    elif list_opt == 3:
        print(todo3)
        obj_to_incomplete = input("Make which item incomplete? (case sensitive): ")

        try:
            todo3[obj_to_incomplete] = "X"
            print(f"{obj_to_incomplete} made incomplete!")
        except KeyError:
            print(f"Item '{obj_to_incomplete}' not found. Cannot make incomplete.")
            try_again = input("Try again? y/n: ")
            if try_again == "y":
                mark_obj_as_incomplete()

    elif list_opt == 4:
        print(todo4)
        obj_to_incomplete = input("Make which item incomplete? (case sensitive): ")

        try:
            todo4[obj_to_incomplete] = "X"
            print(f"{obj_to_incomplete} made incomplete!")
        except KeyError:
            print(f"Item '{obj_to_incomplete}' not found. Cannot make incomplete.")
            try_again = input("Try again? y/n: ")
            if try_again == "y":
                mark_obj_as_incomplete()
    else:
        print("That's not an option.")
        try_again = input("Try again? y/n: ")
        if try_again == "y":
            mark_obj_as_incomplete()

def add_obj():
    list_opt = int(input("Which list? 1-4 : "))

    if list_opt == 1:
        item_name = input("Name of item: ")
        is_completed = "X"

        todo.update({item_name: is_completed})

        print(f"Updated list: {todo}")

    elif list_opt == 2:
        item_name = input("Name of item: ")
        is_completed = "X"

        todo2.update({item_name: is_completed})

        print(f"Updated list: {todo2}")

    elif list_opt == 3:
        item_name = input("Name of item: ")
        is_completed = "X"

        todo3.update({item_name: is_completed})

        print(f"Updated list: {todo3}")

    elif list_opt == 4:
        item_name = input("Name of item: ")
        is_completed = "X"

        todo4.update({item_name: is_completed})

        print(f"Updated list: {todo4}")

    else:
        print("That's not an option.")
        try_again = input("Try again? y/n: ")
        if try_again == "y":
            add_obj()

def main():
    while True:
        display_opt()
        opt = int(input("Option: "))

        if opt == 1:
            add_obj()
            input("Press ENTER to continue")

        if opt == 2:
            delete_obj()
            input("Press ENTER to continue")

        if opt == 3:
            mark_obj_as_completed()
            input("Press ENTER to continue")

        if opt == 4:
            mark_obj_as_incomplete()
            input("Press ENTER to continue")

        if opt == 5:
            display_list()
            input("Press ENTER to continue")

if __name__ == '__main__':
    main()