import os

# === Декоратор ===

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "⚠️ Contact not found."
        except ValueError:
            return "❌ Please provide correct name and phone."
        except IndexError:
            return "❌ Not enough arguments."
    return inner

# === Парсер команди ===

def parse_input(user_input):
    cmd, *args = user_input.strip().split()
    return cmd.lower(), args

# === Handler-функції ===

@input_error
def add_contact(args, contacts):
    name, phone = args

    if not phone.isdigit():
        return "❌ Phone number must contain digits only."

    if name in contacts:
        if phone in contacts[name]:
            return f"⚠️ This phone number already exists for '{name}'."
        else:
            contacts[name].append(phone)
            return f"➕ New phone added to '{name}': {phone}"
    else:
        contacts[name] = [phone]
        return f"✅ Contact '{name}' added with phone '{phone}'."

@input_error
def change_contact(args, contacts):
    name, phone = args

    if not phone.isdigit():
        return "❌ Phone number must contain digits only."

    if name in contacts:
        contacts[name] = [phone]  # замінюємо всі телефони на новий
        return f"🔁 Contact '{name}' updated with new phone '{phone}'."
    else:
        raise KeyError

@input_error
def delete_contact(args, contacts):
    name = args[0]
    del contacts[name]
    return f"🗑️ Contact '{name}' deleted."

@input_error
def show_phone(args, contacts):
    name = args[0]
    phones = ', '.join(contacts[name])
    return f"📞 {name}'s phone number(s): {phones}"

@input_error
def search_contact(args, contacts):
    query = args[0].lower()
    results = []
    for name, phones in contacts.items():
        if query in name.lower():
            results.append(f"- {name}: {', '.join(phones)}")
    if results:
        return "🔎 Search results:\n" + "\n".join(results)
    else:
        return "❌ No matches found."

@input_error
def show_all(contacts):
    if not contacts:
        return "📭 No contacts found."
    result = "📒 Contact list:\n"
    for name, phones in contacts.items():
        result += f"- {name}: {', '.join(phones)}\n"
    return result.strip()

def export_contacts(contacts):
    if not contacts:
        return "📭 No contacts to export."
    with open("contacts.txt", "w") as file:
        for name, phones in contacts.items():
            line = name + ',' + '|'.join(phones) + '\n'
            file.write(line)
    return "✅ Contacts exported to contacts.txt"

def import_contacts(contacts):
    if not os.path.exists("contacts.txt"):
        return "❌ File contacts.txt not found."
    with open("contacts.txt", "r") as file:
        for line in file:
            name, phones_str = line.strip().split(",", 1)
            phones = phones_str.split('|')
            contacts[name] = phones
    return "✅ Contacts imported from contacts.txt"

def show_help():
    return """📖 Available commands:
- add <name> <phone>        Add new contact or new phone to existing
- change <name> <phone>     Replace all phones for a contact
- delete <name>             Delete contact
- phone <name>              Show contact phone(s)
- search <query>            Search contacts by name
- all                       Show all contacts
- import                    Import contacts from contacts.txt
- export                    Export contacts to contacts.txt
- help                      Show this help
- exit / close              Exit bot (auto export)
"""

# === Головний цикл ===

def main():
    contacts = {}
    print("👋 Welcome to the assistant bot!")

    # Автоімпорт якщо файл існує
    if os.path.exists("contacts.txt"):
        import_contacts(contacts)
        print("📂 Contacts loaded from contacts.txt")

    while True:
        user_input = input("📝 Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print(export_contacts(contacts))  # автозбереження
            print("👋 Good bye!")
            break

        elif command == "hello":
            print("🤖 How can I help you?")

        elif command == "add":
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "delete":
            print(delete_contact(args, contacts))

        elif command == "phone":
            print(show_phone(args, contacts))

        elif command == "search":
            print(search_contact(args, contacts))

        elif command == "all":
            print(show_all(contacts))

        elif command == "export":
            print(export_contacts(contacts))

        elif command == "import":
            print(import_contacts(contacts))

        elif command in ["help", "?"]:
            print(show_help())

        else:
            print("❗ Invalid command. Type 'help' to see available commands.")


if __name__ == "__main__":
    main()
