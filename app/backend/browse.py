import os
from pathlib import Path

def liste_fichier_xml(chemin_donnees: Path):
    return os.listdir(chemin_donnees)

