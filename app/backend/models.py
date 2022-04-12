from typing import List, Optional, Dict
from sqlmodel import Field, SQLModel, Relationship, JSON, ARRAY, Column, String
from sqlmodel import Session, select
from backend.database import engine
from .timer import timed, logger



class Collectivite(SQLModel, table=True):
    siret_coll: str = Field(sa_column=Column(String(14), primary_key=True))
    libelle_collectivite: str
    nature_collectivite: str
    departement: Optional[str]

    documents_budgetaires: List["DocumentBudgetaire"] = Relationship(
        back_populates="collectivite")

    @timed
    def insert_collectivite(self):
        if self.get_collectivite(self.siret_coll):
            logger.debug(f"\"{self.libelle_collectivite}\" already in database")
        else:
            with Session(engine) as session:
                session.add(self)
                session.commit()
    
    def get_collectivite(self, siret):
        with Session(engine) as session:
            statement = select(Collectivite).where(Collectivite.siret_coll == siret)
            results = session.exec(statement)
            return results.first()

class DocumentBudgetaire(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    siret_etablissement: str = Field(sa_column=Column(String(14)), index=True)
    libelle: str
    code_insee: Optional[str]
    nomenclature: str
    exercice: int = Field(index=True)
    nature_dec: str  # Enum à l'avenir
    num_dec: Optional[int]
    nature_vote: str  # Enum
    type_budget: str  # Enum
    id_etabl_princ: Optional[str]

    json_budget: Optional[str]# = Field(sa_column=Column(JSON))
    list_annexes: Optional[list] = Field(sa_column=Column(ARRAY(String)))


    fk_siret_collectivite: str = Field(foreign_key="collectivite.siret_coll")
    collectivite: Collectivite = Relationship(
        back_populates="documents_budgetaires")
    annexes: List["Annexe"] = Relationship(
        back_populates="document_budgetaire")

    @timed
    def insert_docbudg(self):
        with Session(engine) as session:
            session.add(self)
            session.commit()
            return self.id




class Annexe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    type_annexe: Optional[str] = Field(index=True)
    json_annexe: Optional[str] #= Field(sa_column=Column(JSON))

    fk_id_document_budgetaire: int = Field(foreign_key="documentbudgetaire.id")
    document_budgetaire: DocumentBudgetaire = Relationship(
        back_populates="annexes")
    


"""
Champ de référence 	Balise XML

### EnTeteDocBudgetaire
SIRET Colloc 	IdColl ----- id Collectivite
libellé Colloc 	LibelleColl  ---- libelle_collectivite
type de collectivité 	NatCEPL ---- nature_collectivite
département 	Departement ---- departement

### EnTeteBudget
libellé budget 	LibelleEtab --- libelle
SIRET budget 	IdEtab --- siret_etablissement
Code INSEE 	CodInseeColl --- code_insee
nomenclature 	Nomenclature --- nomenclature


### BlocBudget
exercice 	Exer --- exercice
type de document budgétaire 	NatDec ----
numéro de DM  	NumDec  -----
nature de vote 	NatFonc ----
budget principal/annexe 	CodTypBud ----
SIRET BP 	IdEtabPal ---

"""
