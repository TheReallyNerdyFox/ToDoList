# Code by Ethan Ray

todo = {}
lists = []

def display_opt():
    print("Please choose an option: ")
    print("1. Add a list")
    print("2. Remove a list")
    print("3. Add item to list")
    print("4. Remove item from list")
    print("5. Mark item as completed")
    print("6. Mark item as not completed")
    print("0. Display list")

def display_lists():
    print("Display which list?")
    print(lists)
    listLookup = input("List: ")
    try:
        print(todo[listLookup])
    except KeyError:
        print(f"{listLookup} does not exist.")
        tryAgain = input("Try again? y/n: ")
        if tryAgain == "y":
            display_lists()

def add_list():
    new_todo = {}
    listname = input("Name the list: ")
    todo[listname] = new_todo
    lists.append(listname)
    print(f"A new list has been created with the name {listname}")

def del_list():
    print(lists)
    listLookup = input("Delete which list: ")
    try:
        print(todo[listLookup])
        confirm = input("Delete this list? y/n: ")
        if confirm == "y":
            del todo[listLookup]
            lists.remove(listLookup)
            print(f"{listLookup} deleted.")
        else:
            print(f"{listLookup} NOT deleted.")
    except KeyError:
        print(f"{listLookup} does not exist.")
        tryAgain = input("Try again? y/n: ")
        if tryAgain == "y":
            del_list()


def add_to_list():
    print(lists)
    listLookup = input("Add task to which list: ")
    item_name = input("Name of task: ")
    is_completed = "X"

    try:
        todo[listLookup].update({item_name: is_completed})
        print(f"Updated list: {todo[listLookup]}")
    except KeyError:
        print(f"{listLookup} does not exist.")
        tryAgain = input("Try again? y/n: ")
        if tryAgain == "y":
            add_to_list()


def del_from_list():
    print(lists)
    listLookup = input("Delete a task from which list: ")
    try:
        print(todo[listLookup])
        item_name = input("Which task to delete: ")
        try:
            del todo[listLookup][item_name]
            print(f"Deleted {item_name} from {listLookup}")
        except KeyError:
            print(f"{listLookup} does not exist.")
            tryAgain = input("Try again? y/n: ")
            if tryAgain == "y":
                add_to_list()
    except KeyError:
        print(f"{listLookup} does not exist.")
        tryAgain = input("Try again? y/n: ")
        if tryAgain == "y":
            add_to_list()

def mark_task_as_complete():
    print(lists)
    listLookup = input("Complete task from which list: ")
    try:
        print(todo[listLookup])
        item_name = input("Complete which task: ")
        try:
            todo[listLookup][item_name] = "✓"
            print("Updated list: ", todo[listLookup])
        except KeyError:
            print(f"Could not complete {item_name}.")
            tryAgain = input("Try again? y/n: ")
            if tryAgain == "y":
                mark_task_as_complete()
    except KeyError:
        print(f"{listLookup} does not exist.")
        tryAgain = input("Try again? y/n: ")
        if tryAgain == "y":
            mark_task_as_complete()

def mark_task_as_incomplete():
    print(lists)
    listLookup = input("Incomplete task from which list: ")
    try:
        print(todo[listLookup])
        item_name = input("Incomplete which task: ")
        try:
            todo[listLookup][item_name] = "X"
            print("Updated list: ", todo[listLookup])
        except KeyError:
            print(f"Could not incomplete {item_name}.")
            tryAgain = input("Try again? y/n: ")
            if tryAgain == "y":
                mark_task_as_incomplete()
    except KeyError:
        print(f"{listLookup} does not exist.")
        tryAgain = input("Try again? y/n: ")
        if tryAgain == "y":
            mark_task_as_incomplete()



def main():
    while True:
        display_opt()
        opt = int(input("Option: "))

        if opt.isdigit():
            if opt == 1:
                add_list()
                input("Press ENTER to continue")

            if opt == 2:
                del_list()
                input("Press ENTER to continue")

            if opt == 3:
                add_to_list()
                input("Press ENTER to continue")

            if opt == 4:
                del_from_list()
                input("Press ENTER to continue")

            if opt == 5:
                mark_task_as_complete()
                input("Press ENTER to continue")

            if opt == 6:
                mark_task_as_incomplete()
                input("Press ENTER to continue")

            if opt == 0:
                display_lists()
                input("Press ENTER to continue")
        else:
            print("That is not a valid option. Use the numbers 1-6, and 0 to make a choice.")
            input("Press ENTER to continue")

if __name__ == '__main__':
    main()