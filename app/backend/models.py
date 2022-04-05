from typing import List, Optional, Dict
from sqlmodel import Field, SQLModel, Relationship, JSON, Column


class Collectivite(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    siret_coll: str 
    libelle_collectivite: str
    nature_collectivite: str
    departement: Optional[str]

    documentsBudgetaires: List["DocumentBudgetaire"] = Relationship(back_populates="collectivite")


class DocumentBudgetaire(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    siret_etablissement: str
    libelle: str
    code_insee: Optional[str]
    nomenclature: str
    exercice: int
    nature_dec: str #Enum à l'avenir
    num_dec: Optional[int]
    nature_vote: str #Enum
    type_budget: str #Enum
    id_etabl_princ: Optional[str]

    fk_id_collectivite: str = Field(foreign_key="collectivite.id") 
    json_budget: Optional[dict] = Field(sa_column=Column(JSON))
    json_annexes: Optional[dict] = Field(sa_column=Column(JSON))

    collectivite: Collectivite = Relationship(back_populates="documentsBudgetaires")
    annexes: List["Annexe"] = Relationship(back_populates="documentsBudgetaires")


class Annexe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fk_id_document_budgetaire: int = Field(foreign_key="documentbudgetaire.id")
    type_annexe: Optional[str]
    json_annexe: Optional[dict] = Field(sa_column=Column(JSON))
    
    document_budgetaire: DocumentBudgetaire = Relationship(back_populates="annexe")



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


class Annexe(Base):
    __tablename__ = "annexes"

    id_annexe = Column(String, primary_key=True, nullable = False)
    libelle = Column(String, nullable = False)
    liste_champs = Column(String, nullable = False)
    nom_fichier = Column(String, nullable = False)
    chemin_xml = Column(String, nullable = False)
    element_type = Column(String, nullable = False)


class Champ(Base):
    __tablename__ = "champs"

    id_champ = Column(String, primary_key=True, nullable = False)
    libelle = Column(String, nullable = False)
    libelle_long = Column(String, nullable = False)
    value_dict = Column(String, primary_key=True, nullable = False)



- # annexes
- idannexe (primary key)
- codeChamp (primary key)
- nom_fichier_xsd
- nom_racine (surement deux éléments DATA_CONCOURS(1)/CONCOURS(*))
- libChamp
- descChamp

content = Column(String, nullable = False)
    is_published = Column(Boolean, server_default='True', nullable = True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, 
        server_default=text('now()'))
- # Code champ annexe
- codeChamp (primary key)
- value (primary key)
- libellé
- libellé long (libellé + description)
"""