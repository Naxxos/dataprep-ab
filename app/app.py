
from sqlmodel import SQLModel,  Session
from backend.database import engine, create_db_and_tables
from backend.models import Collectivite, DocumentBudgetaire

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
    create_collectivites()

if __name__ == "__main__":
    main()

