import streamlit as st
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

# --- Fonctions de gestion des données (réutilisées du CLI) ---
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)

# --- Configuration de la page ---
st.set_page_config(page_title="Task Tracker", page_icon="✅", layout="wide")
st.title("✅ Gestionnaire de Tâches")
st.markdown("Organisez votre travail simplement et efficacement.")

# --- Barre latérale pour la navigation ---
st.sidebar.header("🛠️ Menu")
action = st.sidebar.radio("Que voulez-vous faire ?", ["📋 Voir les tâches", "➕ Ajouter une tâche"])

tasks = load_tasks()

# --- Page : Ajouter une tâche ---
if action == "➕ Ajouter une tâche":
    st.subheader("Nouvelle tâche")
    with st.form("add_task_form"):
        desc = st.text_input("Description de la tâche", placeholder="Ex: Acheter des courses...")
        submitted = st.form_submit_button("Ajouter la tâche")
        
        if submitted:
            if desc.strip():
                new_task = {
                    "id": max([t["id"] for t in tasks], default=0) + 1,
                    "description": desc.strip(),
                    "status": "todo",
                    "createdAt": datetime.now().isoformat(),
                    "updatedAt": datetime.now().isoformat()
                }
                tasks.append(new_task)
                save_tasks(tasks)
                st.success(f"✅ Tâche ajoutée avec succès (ID: {new_task['id']}) !")
                st.rerun()
            else:
                st.error("⚠️ La description ne peut pas être vide.")

# --- Page : Voir et gérer les tâches ---
else:
    st.subheader("📋 Liste des tâches")
    
    # Filtre
    filter_status = st.selectbox(
        "Filtrer par statut :", 
        ["Toutes", "🔴 À faire (todo)", "🟡 En cours (in-progress)", "🟢 Terminées (done)"]
    )
    
    status_map = {
        "Toutes": None, 
        "🔴 À faire (todo)": "todo", 
        "🟡 En cours (in-progress)": "in-progress", 
        "🟢 Terminées (done)": "done"
    }
    target_status = status_map[filter_status]

    filtered_tasks = [t for t in tasks if target_status is None or t["status"] == target_status]

    if not filtered_tasks:
        st.info("📭 Aucune tâche trouvée pour ce filtre.")
    else:
        # Affichage sous forme de cartes modernes
        for t in filtered_tasks:
            with st.container(border=True):
                col1, col2, col3 = st.columns([5, 2, 2])
                
                with col1:
                    st.markdown(f"**{t['description']}**")
                    st.caption(f"📅 Créé le: {t['createdAt'][:10]} | 🔄 Mis à jour le: {t['updatedAt'][:10]}")
                
                with col2:
                    status_badge = {
                        "todo": "🔴 À faire", 
                        "in-progress": "🟡 En cours", 
                        "done": "🟢 Terminée"
                    }
                    st.write(status_badge.get(t["status"], t["status"]))
                
                with col3:
                    # Boutons d'action
                    if t["status"] != "in-progress":
                        if st.button("▶️ En cours", key=f"prog_{t['id']}"):
                            t["status"] = "in-progress"
                            t["updatedAt"] = datetime.now().isoformat()
                            save_tasks(tasks)
                            st.rerun()
                    
                    if t["status"] != "done":
                        if st.button("✅ Terminé", key=f"done_{t['id']}"):
                            t["status"] = "done"
                            t["updatedAt"] = datetime.now().isoformat()
                            save_tasks(tasks)
                            st.rerun()
                    
                    if st.button("🗑️ Supprimer", key=f"del_{t['id']}", type="secondary"):
                        tasks = [task for task in tasks if task["id"] != t["id"]]
                        save_tasks(tasks)
                        st.rerun()