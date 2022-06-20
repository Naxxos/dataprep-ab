
from sqlmodel import SQLModel,  Session, select
from backend.database import engine, drop_and_create_db_and_tables
from backend.models import Collectivite, DocumentBudgetaire, Annexe
from backend.parsing import Parsing
import backend.config, backend.browse
from pathlib import Path
import gzip
import xmltodict

from backend.timer import logger

def insert_annexes(list_Annexes, doc_budg_id):
    with Session(engine) as session:
        for annexe in list_Annexes:
            #doc_budg.annexes.append(annexe)
            session.add(annexe)
            session.commit()

def main():
    drop_and_create_db_and_tables()
    chemin_fichiers_xml = backend.browse.get_liste_fichiers_xml(Path(backend.config.SOURCE_FILES))
    n = 0

    parsing = Parsing()
    for file in chemin_fichiers_xml:
        with gzip.open(file) as f:
            logger.debug(f"\"{file}\" opened, fichier n°{n}")
            dict_doc_budg = xmltodict.parse(f.read(), encoding="latin-1", dict_constructor=dict)
            
            #dict_doc_budg = parsing.create_dict_from_xml(f.read())
        try:
            dict_infos_coll = parsing.parsing_infos_collectivite(dict_doc_budg)
            dict_infos_etab = parsing.parsing_infos_etablissement(dict_doc_budg)
            
            collectivite = Collectivite(**dict_infos_coll)
            collectivite.insert_collectivite()

            doc_budg = DocumentBudgetaire(**dict_infos_etab)
            doc_budg_id = doc_budg.insert_docbudg()
            
            #collectivite.documents_budgetaires.append(doc_budg)

            dict_annexes = parsing.parsing_annexes(dict_doc_budg)
            list_Annexes = parsing.create_list_Annexe(dict_annexes, doc_budg_id)
            insert_annexes(list_Annexes, doc_budg_id)
            n += 1
            if (n % 100) == 0:
                logger.debug(f"Fichier n°{n}")
        except KeyError:
            logger.error(f"Missing mandatory fields")


        
    #get_collectivite("20005375900011")


if __name__ == "__main__":
    main()

