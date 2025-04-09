import os


def replace_underscores_in_names(start_folder):
    # Parcours d'abord les fichiers (en partant du plus profond)
    for root, dirs, files in os.walk(start_folder, topdown=False):
        for name in files:
            if "_" in name:
                old_path = os.path.join(root, name)
                new_name = name.replace("_", " ")
                new_path = os.path.join(root, new_name)

                # Vérifie que l'ancien chemin existe encore
                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                    print(f"Fichier renommé: {name} -> {new_name}")

    # Ensuite, parcours des dossiers (toujours du plus profond)
    for root, dirs, files in os.walk(start_folder, topdown=False):
        for name in dirs:
            if "_" in name:
                old_path = os.path.join(root, name)
                new_name = name.replace("_", " ")
                new_path = os.path.join(root, new_name)

                # Vérifie que l'ancien chemin existe encore
                if os.path.exists(old_path):
                    os.rename(old_path, new_path)
                    print(f"Dossier renommé: {name} -> {new_name}")


if __name__ == "__main__":
    dossier_depart = "Hack The Box Academy Modules"
    replace_underscores_in_names(dossier_depart)
    print("\n✅ Renommage terminé avec succès.")
