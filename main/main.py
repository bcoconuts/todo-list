'''
Generate and maintain a ToDo List using the CLI
'''


# =========================
# CONFIG
# =========================

ADD_TASK = "Add Task"
REMOVE_TASK = "Remove Task"
VIEW_TASKS = "View Tasks"
EXIT = "Exit"
TASK_NUMBER = "Task Number"
NAME = "Name"
STATUS = "Status"
COMPLETE = "Complete"
INCOMPLETE = "Incomplete"
IN_PROGRESS = "In Progress"
REJECTED = "Rejected"
CHOICES = {1: ADD_TASK, 2: REMOVE_TASK, 3: VIEW_TASKS, 4: EXIT}


# =========================
# UTILITY
# =========================

def get_key_number_choice_from_dict(prompt: str, target_dict: dict) -> int:
    dict_range = [i for i in range(1, len(target_dict) + 1)]
    min_choice = min(dict_range)
    max_choice = max(dict_range)
    invalid_prompt = f"Invalid choice. Choise must be a numerical value between {min_choice} - {max_choice}"

    while True:
        try:
            choice = int(input(prompt).strip())
            if min_choice <= choice <= max_choice:
                break
            else:
                print(invalid_prompt)
        except ValueError:
            print(invalid_prompt)

    return choice


def display_options_from_dict(header: str, target_dict: dict[int, str]) -> None:
    '''
    Display options to user for a dict formatted {Option Number: Option Name}.
    
    :param header: Header to be displayed prior to options list being displayed.
    :type header: str
    :param target_dict: Dict from which options will be derived.
    :type target_dict: dict[int, str]
    '''
    print(header)
    for k, v in target_dict.items():
        print(f"    {k}. {v}")


# =========================
# LOGIC
# =========================

def get_user_choice() -> int:
    display_options_from_dict("\nOPTIONS:", CHOICES)

    prompt = "What would you like to do?: "
    choice = get_key_number_choice_from_dict(prompt, CHOICES)

    return choice


def route_choice(todo_dict: dict[int, dict[str, str]], choice: int) -> None | bool:
    current_choice = CHOICES[choice]
    if current_choice == ADD_TASK:
        add_item(todo_dict)
        view_items(todo_dict)
    elif current_choice == REMOVE_TASK:
        remove_item(todo_dict)
        view_items(todo_dict)
    elif current_choice == VIEW_TASKS:
        view_items(todo_dict)
    else:
        return True


def add_item(todo_dict: dict[int, dict[str, str]]) -> None:
    new_task_number = len(todo_dict) + 1
    new_task = input("\nName the task you would like to add: ").strip()

    todo_dict[new_task_number] = {}
    todo_dict[new_task_number][NAME] = new_task
    todo_dict[new_task_number][STATUS] = INCOMPLETE

    
def remove_item(todo_dict: dict[int, dict[str, str]]) -> None:
    prompt = "\nWhich task would you like to remove?: "
    task_number = get_key_number_choice_from_dict(prompt, todo_dict)

    todo_dict.pop(task_number)
    new_dict = {i + 1: v for i, v in enumerate(todo_dict.values())}
    todo_dict.clear()
    todo_dict.update(new_dict)


def view_items(todo_dict: dict[int, dict[str, str]]) -> None:
    print("\nLIST:")
    for k in todo_dict:
        task = todo_dict[k][NAME]
        status = todo_dict[k][STATUS]
        print(f"    {k}. {task} -- Status: {status}")


# =========================
# MAIN LOOP
# =========================

def main():
    todo_dict = sample_dict
    exited = False
    while not exited:
        choice = get_user_choice()
        exited = route_choice(todo_dict, choice)


# =========================
# TESTING
# =========================

sample_dict = {
    1: {NAME: "Laundry", STATUS: INCOMPLETE},
    2: {NAME: "Bills", STATUS: COMPLETE},
    3: {NAME: "Coding", STATUS: IN_PROGRESS},
}

if __name__ == "__main__":
    main()
