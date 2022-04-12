import os
from pathlib import Path

def get_liste_fichiers_xml(chemin_donnees: Path):
    return chemin_donnees.glob('**/*')

def get_liste_chemin_fichiers(chemin_donnees: Path):
    list_fichier = get_liste_fichiers_xml(chemin_donnees)
    liste_chemin = []
    for nom_fichier in list_fichier:
        liste_chemin.append(Path.joinpath(chemin_donnees, nom_fichier))

    return liste_chemin