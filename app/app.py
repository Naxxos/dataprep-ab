
from sqlmodel import SQLModel,  Session, select
from backend.database import engine, drop_and_create_db_and_tables
from backend.models import Collectivite, DocumentBudgetaire, Annexe
import backend.parsing, backend.config, backend.browse
from pathlib import Path

def get_collectivite(siret):
    with Session(engine) as session:
        statement = select(Collectivite).where(Collectivite.siret_coll == siret)
        results = session.exec(statement)
        return results.first()

def insert_collectivite(dict_coll):
    coll = Collectivite(**dict_coll)
    if get_collectivite(coll.siret_coll):
        print(f"\"{coll.libelle_collectivite}\" already in database")
    else:
        with Session(engine) as session:
            session.add(coll)
            session.commit()

def insert_docbudg(dict_etablissement):
    doc_budg = DocumentBudgetaire(**dict_etablissement)
    with Session(engine) as session:
            session.add(doc_budg)
            session.commit()
            return doc_budg.id

def insert_annexe(list_Annexes: list[Annexe], doc_budg_id):
    with Session(engine) as session:
        for annexe in list_Annexes:
            #doc_budg.annexes.append(annexe)
            session.add(annexe)
            session.commit()


def insert_in_db(object_to_insert):
    with Session(engine) as session:
        session.add(object_to_insert)
        session.commit()

def insert_bulk_in_db(objects):
    with Session(engine) as session:
        session.bulk_save_objects(objects)
        session.commit()


def main():
    drop_and_create_db_and_tables()
    chemin_fichiers_xml = backend.browse.get_liste_fichiers_xml(Path(backend.config.SOURCE_FILES))
    
    for file in chemin_fichiers_xml:
        dict_doc_budg = backend.parsing.create_dict_from_xml(file)
        dict_infos_coll = backend.parsing.parsing_infos_collectivite(dict_doc_budg)
        dict_infos_etab = backend.parsing.parsing_infos_etablissement(dict_doc_budg)
        
        insert_collectivite(dict_infos_coll)
        doc_budg_id = insert_docbudg(dict_infos_etab)

        dict_annexes = backend.parsing.parsing_annexes(dict_doc_budg)
        list_Annexes = backend.parsing.create_list_Annexe(dict_annexes, doc_budg_id)
        #coll.documents_budgetaires.append(doc_budg)
        insert_annexe(list_Annexes, doc_budg_id)

        
    #get_collectivite("20005375900011")


if __name__ == "__main__":
    main()

