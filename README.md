# 📋 Task Tracker CLI

Application en ligne de commande pour gérer vos tâches quotidiennes. Stockage local en JSON, sans dépendances externes.

## 🚀 Installation
1. Clonez ou téléchargez le script `task_CLI.py`
2. Assurez-vous d'avoir Python 3.6+ installé
3. Exécutez : `python task_CLI.py <commande>`

## 🛠️ Commandes disponibles
| Commande | Description |
|----------|-------------|
| `add "<description>"` | Ajoute une nouvelle tâche |
| `update <id> "<desc>"` | Met à jour la description |
| `delete <id>` | Supprime une tâche |
| `mark-in-progress <id>` | Marque comme en cours |
| `mark-done <id>` | Marque comme terminée |
| `list` | Liste toutes les tâches |
| `list todo` | Liste les tâches à faire |
| `list in-progress` | Liste les tâches en cours |
| `list done` | Liste les tâches terminées |

## 💾 Stockage
Les tâches sont sauvegardées dans `tasks.json` (créé automatiquement dans le dossier courant).

## 🐛 Gestion d'erreurs
- IDs invalides ou manquants → message clair
- Fichier JSON corrompu → réinitialisation sécurisée
- Commandes inconnues → affichage de l'aide
