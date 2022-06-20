import copy
import app.backend.config
import xmltodict
import json
import glob
import os

from pathlib import Path
from datetime import datetime

import logging
import time

from typing import List, Optional, Dict
from sqlmodel import Field, SQLModel, Relationship, JSON, ARRAY, Column, String
from sqlmodel import Session, select
from app.backend.database import engine

from functools import wraps

from sqlmodel import SQLModel
from sqlmodel import create_engine
import os


CHAMPS_LIGNE_BUDGET = ["SIRET", "Nature","LibCpte","Fonction","Operation","ContNat","ArtSpe","ContFon",
                 "ContOp","CodRD","MtBudgPrec","MtRARPrec","MtPropNouv","MtPrev","CredOuv",
                 "MtReal","MtRAR3112","OpBudg","TypOpBudg","OpeCpteTiers", "MtSup" , "CaracSup"]

CHAMPS_ANNEXES = {
  'DATA_PRES_CROISEE': ["RefFonc",
  "ChapitreNature",
  "Section",
  "InfoOpe",
  "CodRD",
  "OpBudg",
  "MtBudgPrec",
  "MtRARPrec",
  "MtPropNouv",
  "MtPrev",
  "CredOuv",
  "MtReal",
  "MtRAR3112",
  "MtCumul",
  "MtCumulCA",
  "MtMdtTitreEmis",
  "MtSup"],
'DATA_EMPRUNT': ['AnEncaisse',
  'AnnuitNetDette',
  'Champ_Editeur',
  'CodArticle',
  'CodNatEmpr',
  'CodPeriodRemb',
  'CodPeriodRembDtVote',
  'CodPeriodRembReneg',
  'CodProfilAmort',
  'CodProfilAmortDtVote',
  'CodProfilAmortReneg',
  'CodTypEmpr',
  'CodTypEmprGaranti',
  'CodTypPreteur',
  'CodTypTxCouv',
  'CodTypTxReneg',
  'CodTyptxDtVote',
  'CodTyptxInit',
  'CoutSortie',
  'Couverture',
  'Dt1RembInit',
  'DtDebCouv',
  'DtEmission',
  'DtFinContr',
  'DtFinCouv',
  'DtPeriodeBonif',
  'DtRegltCouv',
  'DtReneg',
  'DtSignInit',
  'DureeAnn',
  'DureeContratInit',
  'DureeContratReneg',
  'DureeRest',
  'DureeRestInit',
  'DureeRestReneg',
  'IndSousJacent',
  'IndSousJacentApresCouv',
  'IndSousJacentAvantCouv',
  'IndSousJacentDtVote',
  'IndexTxVariDtVote',
  'IndexTxVariInit',
  'IndexTxVariReneg',
  'IndiceCouv',
  'IndiceEmpr',
  'IndiceEmprDtVote',
  'LibCpte',
  'LibOrgCoContr',
  'LibOrgaPreteur',
  'MPrimeRecueCouv',
  'MtCRDCouvert',
  'MtCRDRefin',
  'MtCapitalExer',
  'MtCapitalReamenage',
  'MtCapitalRestDu_01_01',
  'MtCapitalRestDu_31_12',
  'MtCharges',
  'MtCommCouv',
  'MtCouv',
  'MtCouvert',
  'MtEmprOrig',
  'MtEmprReneg',
  'MtICNE',
  'MtInt778',
  'MtIntExer',
  'MtPrimePayeeCouv',
  'MtProduits',
  'MtSortie',
  'NatCouv',
  'NomBenefEmprGaranti',
  'NumContrat',
  'NumContratCouv',
  'ObjEmpr',
  'PartGarantie',
  'ProfilAmort',
  'ProfilAmortDtVote',
  'ProvGarantiEmpr',
  'RReelFon',
  'Renegocie',
  'RtAnticipe',
  'Structure',
  'StructureDtVote',
  'StuctureApresCouv',
  'StuctureAvantCouv',
  'Tot1Annuite',
  'TotGarEchoirExer',
  'TxActua',
  'TxActuaInit',
  'TxActuaReneg',
  'TxApresCouv',
  'TxMargeInit',
  'TxMaxi',
  'TxMini',
  'TxPaye',
  'TxRecu',
  'Txinit',
  'TypCouv',
  'TypeSortie'],
 'DATA_TRESORERIE': ['Champ_Editeur',
  'CodArticle',
  'DtDec',
  'IntManda',
  'LibOrgaPret',
  'MtMaxAutori',
  'MtRemb',
  'MtRembInt',
  'MtRestDu',
  'MtTirage',
  'NumContrat'],
 'DATA_CHARGE': ['Champ_Editeur',
  'CodTypeCharge',
  'DtDelib',
  'DureeEtal',
  'Exer',
  'MtAmort',
  'MtDepTransf',
  'MtDotAmort',
  'NatDepTransf'],
 'DATA_TIERS': ['Champ_Editeur',
  'CodChapitre',
  'CodOper',
  'CodOperR',
  'CodRD',
  'DtDelib',
  'LibOper',
  'MtCredOuv',
  'MtCumulReal',
  'MtRealCumulPrec',
  'MtRealExer',
  'NatTrav',
  'RAR',
  'TypOpDep'],
 'DATA_CREDIT_BAIL': ['Champ_Editeur',
  'CodTypContr',
  'DureeContr',
  'ExerContr',
  'LibCredBail',
  'MtCumulRest',
  'MtRedevExer',
  'MtRedevN_1',
  'MtRedevN_2',
  'MtRedevN_3',
  'MtRedevN_4',
  'MtRedevN_5',
  'NatBienContr',
  'NumContr'],
 'DATA_PPP': ['AnnSignContr',
  'Champ_Editeur',
  'DtFinContr',
  'DureeContr',
  'LibContr',
  'MtRemunCoContr',
  'MtTotContr',
  'NatPrestaContr',
  'NomOrgaContr',
  'PartInvest',
  'PartNetteInvest'],
 'DATA_AUTRE_ENGAGEMENT': ['AnnOrig',
  'Champ_Editeur',
  'CodArticle',
  'CodTypAutEng',
  'CodTypPersoMorale',
  'CodePeriod',
  'DureeEng',
  'MtAnnuit',
  'MtDette',
  'MtDetteOrig',
  'NatEng',
  'NomOrgaBenef'],
 'DATA_CONCOURS': ['Champ_Editeur',
  'CodArticle',
  'CodInvFonc',
  'CodNatJurBenefCA',
  'DenomOuNumSubv',
  'LibOrgaBenef',
  'LibPrestaNat',
  'MtSubv',
  'ObjSubv',
  'PopCommune',
  'Siret'],
 'DATA_RECETTE_AFFECTEE': ['Champ_Editeur',
  'CodArticle',
  'CodChapitre',
  'CodRAffect',
  'LibArticle',
  'LibRAffect',
  'MtD',
  'MtR',
  'MtRAE0101'],
 'DATA_FORMATION': ['ActionFinanc', 'Champ_Editeur', 'NomElu'],
 'DATA_FISCALITE': ['Champ_Editeur',
  'CodSousTypContrib',
  'CodTypContrib',
  'CodTypeCarburant',
  'LibTaxe',
  'MtBaseNotif',
  'MtProdVote',
  'Origine',
  'TxApplicConsMunic',
  'TxVariBase',
  'TxVariProd',
  'TxVariTx',
  'Unite'],
 'DATA_CONSOLIDATION': ['Champ_Editeur',
  'CodBudAnnex',
  'CodInvFonc',
  'CodRD',
  'CodTypBudAgreg',
  'LibBudAnnex',
  'MtCredOuv',
  'MtRealMandatTitre',
  'RAR',
  'SiretBudAnnexe'],
 'DATA_ORGANISME_ENG': ['Champ_Editeur',
  'CodNatEng',
  'DtEng',
  'MtOrgEng',
  'NatEng',
  'NatJurOrgEng',
  'NomOrgEng',
  'RSOrgEng'],
 'DATA_ORGANISME_GROUP': ['Champ_Editeur',
  'CodModFinanc',
  'CodNatOrgGroup',
  'DtAdhGroup',
  'MtFinancOrgGroup',
  'NomOrgGroup'],
 'DATA_PATRIMOINE': ['Champ_Editeur',
  'CodEntreeSorti',
  'CodModalAcqui',
  'CodModalSorti',
  'CodTypImmo',
  'CodTypTitre',
  'CodVariPatrim',
  'DtAcquiBien',
  'DtCessBienSorti',
  'DtDelib',
  'DureeAmortBien',
  'LibBien',
  'LibObserv',
  'LibOrgPrisePartic',
  'MtAmortExer',
  'MtCumulAmortBien',
  'MtPrixCessBienSorti',
  'MtVNCBien0101',
  'MtVNCBien3112',
  'MtVNCBienSorti',
  'MtValAcquiBien',
  'NumInventaire'],
 'DATA_PERSONNEL': ['Champ_Editeur',
  'CodCatAgent',
  'CodMotifContrAgent',
  'CodSectAgentNonTitulaire',
  'CodSectAgentTitulaire',
  'CodTypAgent',
  'EffectifBud',
  'EffectifPourvu',
  'EffectifTNC',
  'EmploiGradeAgent',
  'IndiceAgent',
  'LibMotifContrAgent',
  'LibelleNatureContrat',
  'MtPrev6215',
  'NatureContrat',
  'Permanent',
  'RemunAgent',
  'TempsComplet'],
 'DATA_PERSONNEL_SOLDE': ['Champ_Editeur',
  'NbrCreatEmploi',
  'NbrSupprEmploi'],
 'DATA_DETTE': ['Champ_Editeur',
  'LibTypDette',
  'MtDExerDette',
  'MtInitDette',
  'MtRestDette'],
 'DATA_VENTILATION': ['Champ_Editeur',
  'CodArticle',
  'CodChapitre',
  'CodInvFonc',
  'CodRD',
  'CodRegroup',
  'CodTypVentil',
  'LibCpte',
  'MtVentil',
  'NomService',
  'TypOpBudg'],
 'DATA_CONTRAT_COUV': ['CapitalRestDu',
  'Champ_Editeur',
  'CodPeriodRemb',
  'CodTypRisqFinanc',
  'CodTypTx',
  'DtDebContr',
  'DtFinContrEmpr',
  'DtFinCouv',
  'DtReglt',
  'DureeContr',
  'IndSousJacentApresCouv',
  'IndSousJacentAvantCouv',
  'IndexTxPaye',
  'IndexTxRecu',
  'LibEmprCouv',
  'LibOrgCoContr',
  'MtChaOrig',
  'MtChaOrigPrimeAss',
  'MtChaOrigPrimeCommi',
  'MtCommDiv',
  'MtEmprCouv',
  'MtMaxAutoriEmprEnc_N',
  'MtMaxAutori_N',
  'MtPert',
  'MtPertProf',
  'MtPrimePayee',
  'MtPrimeRecue',
  'MtProdOrig',
  'MtProf',
  'NatContrCouv',
  'NbEmpruntCouv',
  'NumContratCouv',
  'StuctureApresCouv',
  'StuctureAvantCouv',
  'TxTxPaye',
  'TxTxRecu',
  'TypCouv'],
 'DATA_AMORTISSEMENT_METHODE': ['Champ_Editeur',
  'DtDelib',
  'DureeBienAmort',
  'LibBienAmort',
  'ProcAmort'],
 'DATA_PROVISION': ['Champ_Editeur',
  'CodNatProv',
  'CodSTypProv',
  'CodTypProv',
  'CodTypTabProv',
  'DtConstitProv',
  'DureeEtal',
  'LibNatProv',
  'LibObjProv',
  'MtProvConstit_01_01_N',
  'MtProvExer',
  'MtProvRepr',
  'MtTotalProvAConstit'],
 'DATA_APCP': ['Champ_Editeur',
  'Chapitre',
  'CodSTypAutori',
  'CodTypAutori',
  'LibAutori',
  'MtAutoriAffectee',
  'MtAutoriAffecteeAnnulee',
  'MtAutoriDispoAffectation',
  'MtAutoriNonCouvParCP_01_01_N',
  'MtAutoriPrec',
  'MtAutoriPropose',
  'MtAutoriVote',
  'MtAutori_NMoins1',
  'MtCPAnt',
  'MtCPOuv',
  'MtCPReal',
  'MtCredAFinanc_NPlus1',
  'MtCredAFinanc_Sup_N',
  'MtCredAFinanc_Sup_NPlus1',
  'NumAutori',
  'RatioCouvAutoriAffect_N',
  'RatioCouvAutoriAffect_NMoins1',
  'RatioCouvAutoriAffect_NMoins2',
  'RatioCouvAutoriAffect_NMoins3',
  'TypeChapitre'],
 'DATA_SIGNATURE': ['Champ_Editeur',
  'DtConvoc',
  'DtDelib',
  'DtPresent',
  'DtPub',
  'DtTransmPrefect',
  'DtfFin',
  'LibDelibLieu',
  'LibDelibPar',
  'LibFin',
  'LibPresentLieu',
  'LibPresentPar',
  'LibReuniSession',
  'NbrMembExer',
  'NbrMembPresent',
  'NbrSuffExprime',
  'NbrVoteAbstention',
  'NbrVoteContre',
  'NbrVotePour'],
 'DATA_SIGNATAIRE': ['Signataire'],
 'DATA_ETAB_SERVICE': ['Champ_Editeur',
  'CodNatEtab',
  'DtCreatEtab',
  'DtDelibEtab',
  'IndicTVAEtab',
  'LibCatEtab',
  'LibEtab',
  'LibNatActivEtab',
  'NumDelibEtab',
  'SiretEtab'],
 'DATA_PRET': ['Champ_Editeur',
  'CodTypPret',
  'DtDelib',
  'MtCapitalExer',
  'MtCapitalRestDu_01_01',
  'MtCapitalRestDu_31_12',
  'MtICNE',
  'MtIntExer',
  'NomBenefPret'],
 'DATA_CONTRAT_COUV_REFERENCE': ['Champ_Editeur',
  'CodProfilAmort',
  'CodTyptxInit',
  'DtDebEcheance',
  'DureeAnn',
  'IndexTxVariInit',
  'LibObserv',
  'MtCapitalExer',
  'MtCapitalRestDu_01_01',
  'MtCapitalRestDu_31_12',
  'MtEmprOrig',
  'MtIntExer',
  'NumContr',
  'NumContratEmprunt',
  'TxActuaInit'],
 'DATA_SERVICE_FERROVIAIRE_BUD': ['Champ_Editeur',
  'CodChapitre',
  'CodInvFonc',
  'CodRD',
  'CodRegroupBudFerrov',
  'MtVentil'],
 'DATA_SERVICE_FERROVIAIRE_PATRIM': ['Champ_Editeur',
  'DtFinPot',
  'DtMiseService',
  'LibModeFinanc',
  'LibProprietaire',
  'LibRame',
  'Matricule',
  'MtAmort',
  'MtVNC',
  'MtValOrig'],
 'DATA_SERVICE_FERROVIAIRE_TER': ['Champ_Editeur',
  'CodCptTER',
  'MtCptTER'],
 'DATA_FOND_COMM_HEBERGEMENT': ['Champ_Editeur',
  'CodOper',
  'CodRD',
  'LibEtabHeberg',
  'LibFondHeberg',
  'LibObjFond',
  'MtFond'],
 'DATA_FOND_EUROPEEN': ['Champ_Editeur',
  'CodArticle',
  'CodDestFonds',
  'CodRDDJust',
  'DtAcquit',
  'LibBenef',
  'LibEmetteurs',
  'LibFondsEuropeen',
  'LibMesure',
  'LibOper',
  'MtFond'],
 'DATA_FOND_EUROPEEN_PROGRAMMATION': ['Avances',
  'CodRD',
  'MontantN',
  'MontantN_X',
  'Programmation',
  'RappelTotal',
  'RegulN',
  'TypeFonds',
  'TypeGestion'],
 'DATA_FOND_AIDES_ECO': ['Champ_Editeur',
  'CodArticle',
  'CodInvFon',
  'CodRD',
  'DtConvent',
  'DtVers',
  'LibAide',
  'LibBenef',
  'LibFormeAide',
  'LibOrgConvent',
  'MtDExer',
  'MtDExerAnt',
  'MtReliquatCPAnt',
  'MtTotAide',
  'MtVersExer'],
 'DATA_FORMATION_PRO_JEUNES': ['Champ_Editeur',
  'CodApprent',
  'CodRDTot',
  'CodRessExt',
  'MtFormN',
  'MtFormN_1'],
 'DATA_MEMBRESASA': ['Commune', 'Proprietaire', 'Superficie'],
 'DATA_FLUX_CROISES': ['CodInvFonc',
  'CodRD',
  'CodTypFlux',
  'MtCredOuv',
  'MtRAR',
  'MtReal'],
 'DATA_SOMMAIRE': ['Champ_Editeur', 'CodeAnnexe', 'Present'],
}

import gzip

logger = logging.getLogger(__name__)


# Misc logger setup so a debug log statement gets printed on stdout.
logger.setLevel("DEBUG")
handler = logging.StreamHandler()
log_format = "%(asctime)s %(levelname)s -- %(message)s"
formatter = logging.Formatter(log_format)
handler.setFormatter(formatter)
logger.addHandler(handler)

db_password = os.environ["PG_ROOT_PASSWORD"]

DATABASE_URL = "postgresql://postgres:{}@localhost/actes_budgetaire".format(db_password)

engine = create_engine(DATABASE_URL)

class Collectivite(SQLModel, table=True):
    siret_coll: str = Field(sa_column=Column(String(14), primary_key=True))
    libelle_collectivite: str
    nature_collectivite: str
    departement: Optional[str]

    documents_budgetaires: List["DocumentBudgetaire"] = Relationship(
        back_populates="collectivite")

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
    
class Parsing():
    def create_dict_from_xml(self, chemin_fichier: Path):
        with open(chemin_fichier, encoding='latin-1') as fd:
            doc = xmltodict.parse(fd.read(), dict_constructor=dict)
            logger.debug(chemin_fichier)
        return doc


    def parsing_infos_collectivite(self, dict_from_xml: dict):
        
        infos_dict = dict()
        dict_entete_doc = dict_from_xml["DocumentBudgetaire"]["EnTeteDocBudgetaire"]
        infos_dict["siret_coll"] = dict_entete_doc["IdColl"]["@V"]
        infos_dict["libelle_collectivite"] = dict_entete_doc["LibelleColl"]["@V"]
        infos_dict["nature_collectivite"] = dict_entete_doc["NatCEPL"]["@V"]
        infos_dict["departement"] = dict_entete_doc.get(
            "Departement", {}).get("@V", None)

        return infos_dict


    def parsing_infos_etablissement(self, dict_from_xml: dict):
        infos_dict = dict()
        dict_entete_budget = dict_from_xml["DocumentBudgetaire"]["Budget"]["EnTeteBudget"]
        dict_bloc_budget = dict_from_xml["DocumentBudgetaire"]["Budget"]["BlocBudget"]

        infos_dict["siret_etablissement"] = dict_entete_budget["IdEtab"]["@V"]
        infos_dict["libelle"] = dict_entete_budget["LibelleEtab"]["@V"]
        infos_dict["code_insee"] = dict_entete_budget.get(
            "CodInseeColl", {}).get("@V", None)
        infos_dict["nomenclature"] = dict_entete_budget["Nomenclature"]["@V"]

        infos_dict["exercice"] = int(dict_bloc_budget["Exer"]["@V"])
        infos_dict["nature_dec"] = dict_bloc_budget["NatDec"]["@V"]
        infos_dict["NumDec"] = int(dict_bloc_budget.get(
            "NumDec", {}).get("@V", None) or 0)
        infos_dict["nature_vote"] = dict_bloc_budget["NatFonc"]["@V"]
        infos_dict["type_budget"] = dict_bloc_budget["CodTypBud"]["@V"]
        infos_dict["id_etabl_princ"] = dict_bloc_budget.get(
            "IdEtabPal", {}).get("@V", None)

        infos_dict["json_budget"] = self.generate_dict_budget(dict_from_xml)
        if dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"]:
            infos_dict["list_annexes"] = list(dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"].keys())
        
        infos_dict["fk_siret_collectivite"] = dict_from_xml["DocumentBudgetaire"]["EnTeteDocBudgetaire"]["IdColl"]["@V"]

        return infos_dict


    def generate_dict_all_annexes(self, dict_from_xml: dict) -> dict:
        return dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"]

    def generate_dict_budget(self, dict_from_xml: dict) -> dict:
        budget_dict = copy.deepcopy(
            dict_from_xml["DocumentBudgetaire"]["Budget"]["LigneBudget"])
        
        if isinstance(budget_dict, dict):
            for field in CHAMPS_LIGNE_BUDGET:
                if field in budget_dict:
                    if "@V" in budget_dict[field]:
                        budget_dict[field] = budget_dict[field]['@V']
            return json.dumps([budget_dict])
        for idx, row in enumerate(budget_dict):
            for field in CHAMPS_LIGNE_BUDGET:
                if field in row:
                    if "@V" in row[field]:
                        budget_dict[idx][field] = row[field]['@V']
        #erreur s'il y a qu'une seule ligne de budget
        return json.dumps(budget_dict)

    def generate_dict_annexe(self, dict_from_xml: dict, nom_annexe: str, liste_champs_annexe: list) -> dict:
        annexe_dict = copy.deepcopy(dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"]
                                    [nom_annexe][nom_annexe.split("_", 1)[1]])
        annexe_dict = [annexe_dict] if isinstance(
            annexe_dict, dict) else annexe_dict
        if annexe_dict:
            for idx, row in enumerate(annexe_dict):
                for field in liste_champs_annexe:
                    if row:
                        if field in row:
                            if "@V" in row[field]:
                                annexe_dict[idx][field] = row[field]['@V']
        return annexe_dict

    def parsing_annexes(self, dict_from_xml: dict) -> dict:
        dict_annexes = dict()
        if dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"]:
            liste_annexe = list(dict_from_xml["DocumentBudgetaire"]["Budget"]["Annexes"].keys())
            if "FLUX_CROISES" in liste_annexe: liste_annexe.remove("FLUX_CROISES")

            if "DATA_MEMBRESASA" in liste_annexe: 
                liste_annexe.remove("DATA_MEMBRESASA")
                logger.warning(f"\"DATA_MEMBRESASA\" in annexe ")
            
            if liste_annexe:
                for annexe in liste_annexe:
                    dict_annexes[annexe] = self.generate_dict_annexe(dict_from_xml, annexe, CHAMPS_ANNEXES[annexe])

        return dict_annexes

    def create_list_Annexe(self, dict_annexe: dict, id_doc: int):
        annexes = []
        infos_dict = dict()
        dict_temp = copy.deepcopy(dict_annexe)
        infos_dict["json_annexe"] = {}
        for annexe in  dict_annexe.keys():
            infos_dict["type_annexe"] = annexe
            infos_dict["json_annexe"] = json.dumps(dict_temp[annexe])
            infos_dict["fk_id_document_budgetaire"] = id_doc
            annexes.append(Annexe(**infos_dict))
        
        return annexes

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)

def drop_and_create_db_and_tables():
    drop_db_and_tables()
    create_db_and_tables()
    
def timed(func):
    """This decorator prints the execution time for the decorated function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.debug("{} ran in {}s".format(func.__name__, round(end - start, 2)))
        return result

    return wrapper

def insert_annexes(list_Annexes, doc_budg_id):
    with Session(engine) as session:
        for annexe in list_Annexes:
            #doc_budg.annexes.append(annexe)
            
            session.add(annexe)
            session.commit()

def main():
    #drop_and_create_db_and_tables()
    #chemin_fichiers_xml = backend.browse.get_liste_fichiers_xml(Path(backend.config.SOURCE_FILES))
    n = 0
    liste_fichiers = glob.glob("./import_data/2021*/*")
    parsing = Parsing()
    for file in liste_fichiers:
        with gzip.open(file) as f:
            logger.debug(f"\"{file}\" opened, fichier n°{n}")
            dict_doc_budg = xmltodict.parse(f.read(), dict_constructor=dict)
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
        n +=1

if __name__ == "__main__":
    main()