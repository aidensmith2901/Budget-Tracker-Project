import categoryDim

def categoryCLI(conn):
    while True:
        print("\n=== Category Manager ===")
        print("1. View Parent Categories")
        print("2. View Child Categories")
        print("3. Add Category")
        print("4. Edit Category")
        print("5. Delete Category")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            viewParents(conn)
        elif choice == "2":
            viewChildren(conn)
        elif choice == "3":
            cliAddCategory(conn)
        elif choice == "4":
            cliEditCategory(conn)
        elif choice == "5":
            cliDeleteCategory(conn)
        elif choice == "6":
            break
        else:
            print("Invalid choice.")

def viewParents(conn):
    parents = categoryDim.getParentCategories(conn)
    print("\n--- Parent Categories ---")
    for catID, catName in parents:
        print(f"{catID}: {catName}")

def viewChildren(conn):
    parentID = input("Enter parent category ID: ")
    children = categoryDim.getChildCategories(conn, parentID)

    print("\n--- Child Categories ---")
    for catID, catName in children:
        print(f"{catID}: {catName}")

def cliAddCategory(conn):
    print("\nAdd Category")
    name = input("Category name: ")

    print("Is this a parent category? (y/n)")
    isParent = input("> ").lower()

    if isParent == "y":
        parentCat = None
    else:
        parentCat = input("Enter parent category ID: ")

    success = categoryDim.addCategory(conn, name, parentCat)

    if success:
        print("Category added.")
    else:
        print("Category name already exists.")

def cliEditCategory(conn):
    print("\nEdit Category")
    catID = input("Enter category ID: ")

    newName = input("New name (leave blank to skip): ")
    newName = newName if newName.strip() != "" else None

    newParent = input("New parent ID (blank for no change): ")
    newParent = newParent if newParent.strip() != "" else None

    active = input("Active? (1=active, 0=inactive, blank=skip): ")
    active = int(active) if active.strip() != "" else None

    categoryDim.editCategory(conn, catID, newName, newParent, active)
    print("Category updated.")

def cliDeleteCategory(conn):
    print("\nDelete Category")
    catID = input("Enter category ID: ")
    categoryDim.deleteCategory(conn, catID)
    print("Category deleted (soft delete).")