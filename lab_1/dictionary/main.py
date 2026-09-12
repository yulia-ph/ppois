"""Console interface for the Dictionary."""

import json
from dictionary import Dictionary

def show_menu():
    """Print the main menu."""
    print("-------------MENU-------------")
    print("1. Show dictionary")
    print("2. Add/edit translation")
    print("3. Find translation")
    print("4. Delete translation")
    print("5. Show the size of dictionary")
    print("6. Save dictionary to file")
    print("7. Load dictionary from file")
    print("0. Exit")
    print("------------------------------")


def main():
    d = Dictionary()
    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        match choice:
            case "1":
                print("----------DICTIONARY----------")
                for k, v in d.pack_dictionary().items():
                    print(f"{k} : {v}")
            case "2":
                k = input("Enter word in english: ")
                v = input("Enter translation: ")
                if d.add_node(k, v):
                    print("Translation added")
                else:
                    print("Translation edited")
            case "3":
                k = input("Enter word in english: ")
                try:
                    print(f"Translation: {d.find_node(k)}")
                except KeyError as e:
                    print(e)
            case "4":
                k = input("Enter word in english: ")
                if d.delete_node(k):
                    print("Translation deleted")
                else:
                    print("Translation not found")
            case "5":
                print(f"Size of dictionary: {len(d)}")
            case "6":
                file_name = input("Enter file name: ")
                try:
                    d.save_dictionary(file_name)
                    print(f"Dictionary saved to the file {file_name}")
                except OSError as e:
                    print(f"Could not save: {e}")
            case "7":
                file_name = input("Enter file name: ")
                try:
                    d.load_dictionary(file_name)
                    print(f"Dictionary loaded from file {file_name}")
                except FileNotFoundError:
                    print("File not found")
                except json.JSONDecodeError:
                    print("File is not valid JSON")
                except TypeError as e:
                    print(f"Wrong data in file: {e}")
            case "0":
                print("Exiting...")
                break
            case _:
                print("Input error")

if __name__ == "__main__":
    main()
