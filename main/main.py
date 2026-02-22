'''
Generate and maintain a ToDo List using the CLI
'''

import json


# =========================
# CONFIG
# =========================

TO_DO_FILE = "todo_list.json"
ADD_TASK = "Add Task"
REMOVE_TASK = "Remove Task"
VIEW_TASKS = "View Tasks"
EDIT_TASK_STATUS = "Edit Status of Task"
EXIT = "Exit"
TASK_NUMBER = "Task Number"
NAME = "Name"
STATUS = "Status"
COMPLETE = "Complete"
INCOMPLETE = "Incomplete"
IN_PROGRESS = "In Progress"
REJECTED = "Rejected"
YES = "Yes"
NO = "No"
Y_N_CHOICES = {1: YES, 2: NO}
CHOICES = {1: ADD_TASK, 2: REMOVE_TASK, 3: VIEW_TASKS, 4: EDIT_TASK_STATUS, 5: EXIT}
STATUSES = {1: COMPLETE, 2: INCOMPLETE, 3: IN_PROGRESS}


# =========================
# UTILITY
# =========================

def get_key_number_choice_from_dict(prompt: str, target_dict: dict) -> int:
    dict_range = [i for i in range(1, len(target_dict) + 1)]
    min_choice = min(dict_range)
    max_choice = max(dict_range)
    invalid_prompt = f"Invalid choice. Choice must be a numerical value between {min_choice} - {max_choice}"

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
    header = "\nOPTIONS:"
    display_options_from_dict(header, CHOICES)

    prompt = "What would you like to do?: "
    choice = get_key_number_choice_from_dict(prompt, CHOICES)
    
    return choice


def route_choice(todo_dict: dict[int, dict[str, str]], choice: int) -> bool:
    list_length = len(todo_dict)
    current_choice = CHOICES[choice]
    if current_choice == ADD_TASK:
        add_item(todo_dict)
        view_items(todo_dict)
        return True
    elif current_choice == REMOVE_TASK and list_length > 0:
        remove_item(todo_dict)
        view_items(todo_dict)
        return True
    elif current_choice == VIEW_TASKS:
        view_items(todo_dict)
        return True
    elif current_choice == EDIT_TASK_STATUS and list_length > 0:
        edit_item_status(todo_dict)
        view_items(todo_dict)
        return True
    elif current_choice == EXIT:
        return False
    else:
        print("\nInvalid choice. To-Do List is currently Empty")
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
    discard_item(todo_dict, task_number)


def discard_item(todo_dict: dict[int, dict[str, str]], task_number: int) -> None:
    todo_dict.pop(task_number)
    new_dict = {i + 1: v for i, v in enumerate(todo_dict.values())}
    todo_dict.clear()
    todo_dict.update(new_dict)


def view_items(todo_dict: dict[int, dict[str, str]]) -> None:
    list_length = len(todo_dict)

    if 1 <= list_length:
        print("\nLIST:")
        for k in todo_dict:
            task = todo_dict[k][NAME]
            status = todo_dict[k][STATUS]
            print(f"    {k}. {task} -- Status: {status}")
    else:
        print("\nLIST:\n    EMPTY")


def edit_item_status(todo_dict: dict[int, dict[str, str]]) -> None:
    task_prompt = "\nWhich task would you like to edit the status of?: "
    task_number = get_key_number_choice_from_dict(task_prompt, todo_dict)
    
    header = "\nSTATUS TYPES:"
    display_options_from_dict(header, STATUSES)

    status_prompt = "What would you like the status to be?: "
    status_number = get_key_number_choice_from_dict(status_prompt, STATUSES)
    todo_dict[task_number][STATUS] = STATUSES[status_number]

    status = STATUSES[status_number]
    if status == COMPLETE:
        header = "\nY/N:"
        display_options_from_dict(header, Y_N_CHOICES)

        deletion_prompt = "Status marked as complete. Would you like to delete?:"
        deletion_number = get_key_number_choice_from_dict(deletion_prompt, Y_N_CHOICES)

        if Y_N_CHOICES[deletion_number] == YES:
            discard_item(todo_dict, task_number)
        

# =========================
# FILE I/O
# =========================

def load_todo_dict() -> dict:
    try:
        with open(TO_DO_FILE, "r") as f:
            loaded_dict = json.load(f)
        todo_dict = {int(k): v for k, v in loaded_dict.items()}
    except FileNotFoundError:
        todo_dict = {}
    
    return todo_dict

def save_todo_dict(todo_dict: dict[int, dict[str, str]]) -> None:
    with open(TO_DO_FILE, "w") as f:
        json.dump(todo_dict, f)


# =========================
# MAIN LOOP
# =========================

def main():
    todo_dict = load_todo_dict()
    view_items(todo_dict)
    running = True
    while running:
        choice = get_user_choice()
        running = route_choice(todo_dict, choice)
        save_todo_dict(todo_dict)


if __name__ == "__main__":
    main()
