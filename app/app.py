
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
    #print(backend.browse.liste_fichier_xml(Path(backend.config.SOURCE_FILES)))
    dict_doc_budg = backend.parsing.create_dict_from_xml("./M71_2020/99_BU-033-200053759-20210727-CA_2020_BP_1-BF-1-1_1.XML")
    dict_infos_coll = backend.parsing.parsing_infos_collectivite(dict_doc_budg)
    dict_infos_etab = backend.parsing.parsing_infos_etablissement(dict_doc_budg)
    doc_budg1 = DocumentBudgetaire(**dict_infos_etab)
    coll1 = Collectivite(**dict_infos_coll)

    dict_annexes = backend.parsing.parsing_annexes(dict_doc_budg)
    coll1.documents_budgetaires.append(doc_budg1)
    with Session(engine) as session:
        session.add(coll1)
        session.add(doc_budg1)
        session.commit()
        list_Annexes = backend.parsing.create_list_Annexe(dict_annexes, doc_budg1.id)
        for annexe in list_Annexes:
            session.add(annexe)
            session.commit()

        
    #get_collectivite("20005375900011")


if __name__ == "__main__":
    main()

