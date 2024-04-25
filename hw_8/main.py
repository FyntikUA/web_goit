from search_functions import search_by_tag, search_by_author, search_by_tags

while True:
    command = input("Введіть команду (наприклад, name: Steve Martin, tag:life, tags:life,live, або exit для виходу): ")
    if command.startswith("name:"):
        name = command.split("name:")[1].strip()
        search_by_author(name)
    elif command.startswith("tag:"):
        tag = command.split("tag:")[1].strip()
        search_by_tag(tag)
    elif command.startswith("tags:"):
        tags = command.split("tags:")[1].strip()
        search_by_tags(tags)
    elif command == "exit":
        break
    else:
        print("Невідома команда. Спробуйте ще раз.")
