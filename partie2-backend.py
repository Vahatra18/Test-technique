# partie2-backend.py

class Task:
    """Représente une tâche dans un projet."""
    def __init__(self, name, project, priority, is_blocked=False, block_reason=None):
        self.name = name
        self.project = project
        self.priority = priority  # 1 = haute, 3 = basse
        self.is_blocked = is_blocked
        self.block_reason = block_reason
        
    # Méthode spéciale qui définit la représentation "officielle" d'un objet.
    def __repr__(self):
        return f"Task(name={self.name}, project={self.project}, priority={self.priority}, blocked={self.is_blocked})"


def get_blocked_tasks_sorted(tasks):
    """
    Retourne la liste des tâches bloquées triées par priorité croissante,
    puis par nom alphabétique.
    """
    # On filtre les tâches bloquées
    blocked_tasks = [task for task in tasks if task.is_blocked]
    # Tri : d'abord priorité, ensuite nom
    blocked_tasks.sort(key=lambda t: (t.priority, t.name))
    return blocked_tasks


def update_task_blocked(task, is_blocked, block_reason=None):
    """
    Met à jour l'état bloqué d'une tâche avec validation.
    
    Gestion de la validation :
    - Si is_blocked est True, block_reason doit être une chaîne non vide (après suppression des espaces).
    - Si la validation échoue, on lève une exception ValueError pour signaler l'erreur de manière explicite.
    - Si is_blocked est False, on efface la raison (block_reason = None) sans validation.
    
    Ce choix est simple et permet à l'appelant de capturer l'erreur si nécessaire.
    """
    if is_blocked:
        # Vérification que block_reason est une chaîne et non vide après strip
        if not isinstance(block_reason, str) or block_reason.strip() == "":
            raise ValueError("block_reason doit être une chaîne non vide lorsque is_blocked est True.")
        task.is_blocked = True
        task.block_reason = block_reason.strip()  # On nettoie les espaces inutiles, on utilise le fonction strip()
    else:
        task.is_blocked = False
        task.block_reason = None


# --- Exemples d'utilisation ---
if __name__ == "__main__":
    # Création d'une liste de tâches
    tasks = [
        Task("Déployer le serveur", "Client A", 1, is_blocked=True, block_reason="En attente firewall"),
        Task("Configurer DNS", "Client A", 1, is_blocked=False),
        Task("Rédiger la documentation", "Interne", 3, is_blocked=True, block_reason="Manque d'informations"),
        Task("Tester l'API", "Client B", 2, is_blocked=True, block_reason="Bug à corriger"),
        Task("Mettre à jour le README", "Interne", 3, is_blocked=False),
        Task("Installer le certificat", "Client B", 2, is_blocked=True, block_reason="En attente du fournisseur"),
    ]

    # 1. Filtrer et trier les tâches bloquées, on appelle la méthode get_blocked_tasks_sorted()
    bloquees_triees = get_blocked_tasks_sorted(tasks)
    print("\nLes tâches bloquées triées :")
    for t in bloquees_triees:
        print(f"  {t.name} - {t.project} - {t.priority} - {t.is_blocked} - {t.block_reason}")

    # 2. Tests de mise à jour avec validation, on appelle la méthode update_task_blocked()
    print("\n--- Test de la fonction update_task_blocked ---")

    # Cas valide : bloquer une tâche avec une raison correcte
    tache = tasks[1]  # Configurer DNS (non bloquée)
    print(f"Avant mise à jour : {tache}")
    update_task_blocked(tache, True, "Problème de licence")
    print(f"Après mise à jour valide : {tache}")

    # Cas invalide : bloquer avec une raison vide (espaces)
    try:
        update_task_blocked(tasks[4], True, "   ")
    except ValueError as e:
        print(f"Erreur attendue (raison vide) : {e}")

    # Cas invalide : bloquer avec raison None
    try:
        update_task_blocked(tasks[4], True, None)
    except ValueError as e:
        print(f"Erreur attendue (raison None) : {e}")

    # Cas de déblocage (pas de validation)
    tache_bloquee = tasks[0]
    print(f"\nAvant déblocage : {tache_bloquee}")
    update_task_blocked(tache_bloquee, False)
    print(f"Après déblocage : {tache_bloquee}")