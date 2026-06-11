import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"


# Chargement des tâches 
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        print("⚠️  Fichier tasks.json corrompu. Réinitialisation.")
        return []

# Sauvegarde de tâches dans le fichier json
def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

# Identité de la prochaine tâche
def get_next_id(tasks):
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1

# Description de la tâche à accomplir
def create_task(description):
    now = datetime.now().isoformat()
    return {
        "id": get_next_id(load_tasks()),
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }      

# Implémentation des actions à effectuées 
# Ajouter une tâche
def add_task(description):
    tasks = load_tasks()
    new_task = create_task(description)
    new_task["id"] = get_next_id(tasks)  # Recalculer après chargement
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_task['id']})")

# MAJ d'une tâche de la base de données
def update_task(task_id, new_desc):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["description"] = new_desc
            t["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} updated successfully")
            return
    print(f"❌ Error: Task with ID {task_id} not found")

# Supprimer une tâche de la base de données
def delete_task(task_id):
    tasks = load_tasks()
    filtered = [t for t in tasks if t["id"] != task_id]
    if len(filtered) < len(tasks):
        save_tasks(filtered)
        print(f"Task {task_id} deleted successfully")
    else:
        print(f"❌ Error: Task with ID {task_id} not found")

# Status d'une tâche ( to do, done,...)
def mark_task(task_id, status):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["status"] = status
            t["updatedAt"] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {status}")
            return
    print(f"❌ Error: Task with ID {task_id} not found")

def list_tasks(filter_status=None):
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks found.")
        return

    filtered = tasks
    if filter_status:
        filtered = [t for t in tasks if t["status"] == filter_status]
        if not filtered:
            print(f"📭 No tasks with status '{filter_status}' found.")
            return

    # Affichage formaté
    print(f"{'ID':<4} {'Status':<12} {'Description':<30} {'Created At':<22} {'Updated At':<22}")
    print("-" * 95)
    for t in filtered:
        print(f"{t['id']:<4} {t['status']:<12} {t['description']:<30} {t['createdAt'][:19]:<22} {t['updatedAt'][:19]:<22}")

import sys

def print_usage():
    print("Usage:")
    print("  task-cli add \"<description>\"")
    print("  task-cli update <id> \"<new description>\"")
    print("  task-cli delete <id>")
    print("  task-cli mark-in-progress <id>")
    print("  task-cli mark-done <id>")
    print("  task-cli list [done|todo|in-progress]")

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == "add":
            if len(sys.argv) < 3:
                print("❌ Error: Missing task description")
                sys.exit(1)
            add_task(sys.argv[2])
        elif command == "update":
            if len(sys.argv) < 4:
                print("❌ Error: Missing task ID or new description")
                sys.exit(1)
            update_task(int(sys.argv[2]), sys.argv[3])
        elif command == "delete":
            if len(sys.argv) < 3:
                print("❌ Error: Missing task ID")
                sys.exit(1)
            delete_task(int(sys.argv[2]))
        elif command == "mark-in-progress":
            if len(sys.argv) < 3:
                print("❌ Error: Missing task ID")
                sys.exit(1)
            mark_task(int(sys.argv[2]), "in-progress")
        elif command == "mark-done":
            if len(sys.argv) < 3:
                print("❌ Error: Missing task ID")
                sys.exit(1)
            mark_task(int(sys.argv[2]), "done")
        elif command == "list":
            status = sys.argv[2] if len(sys.argv) > 2 else None
            if status and status not in ("done", "todo", "in-progress"):
                print("❌ Error: Invalid status. Use 'done', 'todo', or 'in-progress'")
                sys.exit(1)
            list_tasks(status)
        else:
            print(f"❌ Unknown command '{command}'")
            print_usage()
            sys.exit(1)
    except ValueError:
        print("❌ Error: Task ID must be an integer.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()        