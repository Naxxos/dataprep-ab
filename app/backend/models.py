from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship


class Collectivite(SQLModel, table=True):
    id: str = Field(primary_key=True)
    libelle_collectivite: str
    nature_collectivite: str
    departement: Optional[str]

    documentsBudgetaires: List["DocumentBudgetaire"] = Relationship(back_populates="collectivite")


class DocumentBudgetaire(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_etablissement: int
    fk_id_collectivite: str = Field(foreign_key="collectivite.id")
    collectivite: Collectivite = Relationship(back_populates="documentsBudgetaires")


"""
Champ de référence 	Balise XML

### EnTeteDocBudgetaire
SIRET Colloc 	IdColl ----- id Collectivite
libellé Colloc 	LibelleColl  ---- libelle_collectivite
type de collectivité 	NatCEPL ---- nature_collectivite
département 	Departement ---- departement


### EnTeteBudget
libellé budget 	LibelleEtab
SIRET budget 	IdEtab
Code INSEE 	CodInseeColl
nomenclature 	Nomenclature



### BlocBudget
exercice 	Exer
type de document budgétaire 	NatDec
numéro de DM  	NumDec
nature de vote 	NatFonc
budget principal/annexe 	CodTypBud
SIRET BP 	IdEtabPal


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