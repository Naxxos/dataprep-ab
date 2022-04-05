
from sqlmodel import SQLModel,  Session
from backend.database import engine, create_db_and_tables
from backend.models import Collectivite, DocumentBudgetaire, Annexe
import backend.parsing, backend.config, backend.browse
from pathlib import Path



def create_collectivites():
    coll1 = Collectivite(id="20005372600028", libelle_collectivite="REGION BOURGOGNE-FRANCHE-COMTE", nature_collectivite="ADM-Etat")
    coll2 = Collectivite(id="20005332600028", libelle_collectivite="Haut de france", nature_collectivite="ADM-Etat")
    coll3 = Collectivite(id="20004332600028", libelle_collectivite="PACA", nature_collectivite="ADM-Etat")

    with Session(engine) as session:
        session.add(coll1)
        session.add(coll2)
        session.add(coll3)

        session.commit()


def main():
    create_db_and_tables()
    #create_collectivites()
    #print(backend.browse.liste_fichier_xml(Path(backend.config.SOURCE_FILES)))
    dict_doc_budg = backend.parsing.create_dict_from_xml("./M71_2020/99_BU-033-200053759-20210727-CA_2020_BP_1-BF-1-1_1.XML")
    dict_infos_coll = backend.parsing.parsing_infos_collectivite(dict_doc_budg)
    #coll1 = Collectivite(**dict_infos_coll)
    #with Session(engine) as session:
    #    session.add(coll1)
    #    session.commit()


if __name__ == "__main__":
    main()

