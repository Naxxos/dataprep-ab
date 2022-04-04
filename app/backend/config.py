
LIST_ANNEXES = "DATA_AMORTISSEMENT_METHODE, DATA_APCP, DATA_AUTRE_ENGAGEMENT, DATA_CHARGE, DATA_CONCOURS, DATA_CONSOLIDATION, DATA_CONTRAT_COUV, DATA_CONTRAT_COUV_REFERENCE, DATA_CREDIT_BAIL, DATA_DETTE, DATA_EMPRUNT, DATA_ETAB_SERVICE, DATA_FISCALITE, DATA_FOND_AIDES_ECO, DATA_FOND_COMM_HEBERGEMENT, DATA_FOND_EUROPEEN, DATA_FOND_EUROPEEN_PROGRAMMATION, DATA_FORMATION, DATA_FORMATION_PRO_JEUNES, DATA_MEMBRESASA, DATA_ORGANISME_ENG, DATA_ORGANISME_GROUP, DATA_PATRIMOINE, DATA_PERSONNEL, DATA_PERSONNEL_SOLDE, DATA_PPP, DATA_PRET, DATA_PROVISION, DATA_RECETTE_AFFECTEE, DATA_SERVICE_FERROVIAIRE_BUD, DATA_SERVICE_FERROVIAIRE_PATRIM, DATA_SERVICE_FERROVIAIRE_TER, DATA_SIGNATAIRE, DATA_SIGNATURE, DATA_SOMMAIRE, DATA_TIERS, DATA_TRESORERIE, DATA_VENTILATION, DATA_FLUX_CROISES".split(", ")

CHAMPS_LIGNE_BUDGET = ["SIRET", "Nature","LibCpte","Fonction","Operation","ContNat","ArtSpe","ContFon",
                 "ContOp","CodRD","MtBudgPrec","MtRARPrec","MtPropNouv","MtPrev","CredOuv",
                 "MtReal","MtRAR3112","OpBudg","TypOpBudg","OpeCpteTiers", "MtSup" , "CaracSup"]

CHAMPS_ANNEXE_DATA_EMPRUNT = "AnEncaisse, AnnuitNetDette, Champ_Editeur, CodArticle, CodNatEmpr, CodPeriodRemb, CodPeriodRembDtVote, CodPeriodRembReneg, CodProfilAmort, CodProfilAmortDtVote, CodProfilAmortReneg, CodTypEmpr, CodTypEmprGaranti, CodTypPreteur, CodTypTxCouv, CodTypTxReneg, CodTyptxDtVote, CodTyptxInit, CoutSortie, Couverture, Dt1RembInit, DtDebCouv, DtEmission, DtFinContr, DtFinCouv, DtPeriodeBonif, DtRegltCouv, DtReneg, DtSignInit, DureeAnn, DureeContratInit, DureeContratReneg, DureeRest, DureeRestInit, DureeRestReneg, IndSousJacent, IndSousJacentApresCouv, IndSousJacentAvantCouv, IndSousJacentDtVote, IndexTxVariDtVote, IndexTxVariInit, IndexTxVariReneg, IndiceCouv, IndiceEmpr, IndiceEmprDtVote, LibCpte, LibOrgCoContr, LibOrgaPreteur, MPrimeRecueCouv, MtCRDCouvert, MtCRDRefin, MtCapitalExer, MtCapitalReamenage, MtCapitalRestDu_01_01, MtCapitalRestDu_31_12, MtCharges, MtCommCouv, MtCouv, MtCouvert, MtEmprOrig, MtEmprReneg, MtICNE, MtInt778, MtIntExer, MtPrimePayeeCouv, MtProduits, MtSortie, NatCouv, NomBenefEmprGaranti, NumContrat, NumContratCouv, ObjEmpr, PartGarantie, ProfilAmort, ProfilAmortDtVote, ProvGarantiEmpr, RReelFon, Renegocie, RtAnticipe, Structure, StructureDtVote, StuctureApresCouv, StuctureAvantCouv, Tot1Annuite, TotGarEchoirExer, TxActua, TxActuaInit, TxActuaReneg, TxApresCouv, TxMargeInit, TxMaxi, TxMini, TxPaye, TxRecu, Txinit, TypCouv, TypeSortie".split(", ")
CHAMPS_ANNEXE_DATA_TRESORERIE = "Champ_Editeur, CodArticle, DtDec, IntManda, LibOrgaPret, MtMaxAutori, MtRemb, MtRembInt, MtRestDu, MtTirage, NumContrat".split(", ")
CHAMPS_ANNEXE_DATA_CHARGE = "Champ_Editeur, CodTypeCharge, DtDelib, DureeEtal, Exer, MtAmort, MtDepTransf, MtDotAmort, NatDepTransf".split(", ")
CHAMPS_ANNEXE_DATA_TIERS = "Champ_Editeur, CodChapitre, CodOper, CodOperR, CodRD, DtDelib, LibOper, MtCredOuv, MtCumulReal, MtRealCumulPrec, MtRealExer, NatTrav, RAR, TypOpDep".split(", ")
CHAMPS_ANNEXE_DATA_CREDIT_BAIL = "Champ_Editeur, CodTypContr, DureeContr, ExerContr, LibCredBail, MtCumulRest, MtRedevExer, MtRedevN_1, MtRedevN_2, MtRedevN_3, MtRedevN_4, MtRedevN_5, NatBienContr, NumContr".split(", ")
CHAMPS_ANNEXE_DATA_PPP = "AnnSignContr, Champ_Editeur, DtFinContr, DureeContr, LibContr, MtRemunCoContr, MtTotContr, NatPrestaContr, NomOrgaContr, PartInvest, PartNetteInvest".split(", ") 
CHAMPS_ANNEXE_DATA_AUTRE_ENGAGEMENT = "AnnOrig, Champ_Editeur, CodArticle, CodTypAutEng, CodTypPersoMorale, CodePeriod, DureeEng, MtAnnuit, MtDette, MtDetteOrig, NatEng, NomOrgaBenef".split(", ")
CHAMPS_ANNEXE_DATA_CONCOURS = "Champ_Editeur, CodArticle, CodInvFonc, CodNatJurBenefCA, DenomOuNumSubv, LibOrgaBenef, LibPrestaNat, MtSubv, ObjSubv, PopCommune, Siret".split(", ")
CHAMPS_ANNEXE_DATA_RECETTE_AFFECTEE = "Champ_Editeur, CodArticle, CodChapitre, CodRAffect, LibArticle, LibRAffect, MtD, MtR, MtRAE0101".split(", ")
CHAMPS_ANNEXE_DATA_FORMATION = "ActionFinanc, Champ_Editeur, NomElu".split(", ")
CHAMPS_ANNEXE_DATA_FISCALITE = "Champ_Editeur, CodSousTypContrib, CodTypContrib, CodTypeCarburant, LibTaxe, MtBaseNotif, MtProdVote, Origine, TxApplicConsMunic, TxVariBase, TxVariProd, TxVariTx, Unite".split(", ")
CHAMPS_ANNEXE_DATA_CONSOLIDATION = "Champ_Editeur, CodBudAnnex, CodInvFonc, CodRD, CodTypBudAgreg, LibBudAnnex, MtCredOuv, MtRealMandatTitre, RAR, SiretBudAnnexe".split(", ")
CHAMPS_ANNEXE_DATA_ORGANISME_ENG = "Champ_Editeur, CodNatEng, DtEng, MtOrgEng, NatEng, NatJurOrgEng, NomOrgEng, RSOrgEng".split(", ")
CHAMPS_ANNEXE_DATA_ORGANISME_GROUP = "Champ_Editeur, CodModFinanc, CodNatOrgGroup, DtAdhGroup, MtFinancOrgGroup, NomOrgGroup".split(", ")
CHAMPS_ANNEXE_DATA_PATRIMOINE = "Champ_Editeur, CodEntreeSorti, CodModalAcqui, CodModalSorti, CodTypImmo, CodTypTitre, CodVariPatrim, DtAcquiBien, DtCessBienSorti, DtDelib, DureeAmortBien, LibBien, LibObserv, LibOrgPrisePartic, MtAmortExer, MtCumulAmortBien, MtPrixCessBienSorti, MtVNCBien0101, MtVNCBien3112, MtVNCBienSorti, MtValAcquiBien, NumInventaire".split(", ")
CHAMPS_ANNEXE_DATA_PERSONNEL = "Champ_Editeur, CodCatAgent, CodMotifContrAgent, CodSectAgentNonTitulaire, CodSectAgentTitulaire, CodTypAgent, EffectifBud, EffectifPourvu, EffectifTNC, EmploiGradeAgent, IndiceAgent, LibMotifContrAgent, LibelleNatureContrat, MtPrev6215, NatureContrat, Permanent, RemunAgent, TempsComplet".split(", ")
CHAMPS_ANNEXE_DATA_PERSONNEL_SOLDE = "Champ_Editeur, NbrCreatEmploi, NbrSupprEmploi".split(", ")
CHAMPS_ANNEXE_DATA_DETTE = "Champ_Editeur, LibTypDette, MtDExerDette, MtInitDette, MtRestDette".split(", ")
CHAMPS_ANNEXE_DATA_VENTILATION = "Champ_Editeur, CodArticle, CodChapitre, CodInvFonc, CodRD, CodRegroup, CodTypVentil, LibCpte, MtVentil, NomService, TypOpBudg".split(", ")
CHAMPS_ANNEXE_DATA_CONTRAT_COUV = "CapitalRestDu, Champ_Editeur, CodPeriodRemb, CodTypRisqFinanc, CodTypTx, DtDebContr, DtFinContrEmpr, DtFinCouv, DtReglt, DureeContr, IndSousJacentApresCouv, IndSousJacentAvantCouv, IndexTxPaye, IndexTxRecu, LibEmprCouv, LibOrgCoContr, MtChaOrig, MtChaOrigPrimeAss, MtChaOrigPrimeCommi, MtCommDiv, MtEmprCouv, MtMaxAutoriEmprEnc_N, MtMaxAutori_N, MtPert, MtPertProf, MtPrimePayee, MtPrimeRecue, MtProdOrig, MtProf, NatContrCouv, NbEmpruntCouv, NumContratCouv, StuctureApresCouv, StuctureAvantCouv, TxTxPaye, TxTxRecu, TypCouv".split(", ")
CHAMPS_ANNEXE_DATA_AMORTISSEMENT_METHODE = "Champ_Editeur, DtDelib, DureeBienAmort, LibBienAmort, ProcAmort".split(", ")
CHAMPS_ANNEXE_DATA_PROVISION = "Champ_Editeur, CodNatProv, CodSTypProv, CodTypProv, CodTypTabProv, DtConstitProv, DureeEtal, LibNatProv, LibObjProv, MtProvConstit_01_01_N, MtProvExer, MtProvRepr, MtTotalProvAConstit".split(", ")
CHAMPS_ANNEXE_DATA_APCP = "Champ_Editeur, Chapitre, CodSTypAutori, CodTypAutori, LibAutori, MtAutoriAffectee, MtAutoriAffecteeAnnulee, MtAutoriDispoAffectation, MtAutoriNonCouvParCP_01_01_N, MtAutoriPrec, MtAutoriPropose, MtAutoriVote, MtAutori_NMoins1, MtCPAnt, MtCPOuv, MtCPReal, MtCredAFinanc_NPlus1, MtCredAFinanc_Sup_N, MtCredAFinanc_Sup_NPlus1, NumAutori, RatioCouvAutoriAffect_N, RatioCouvAutoriAffect_NMoins1, RatioCouvAutoriAffect_NMoins2, RatioCouvAutoriAffect_NMoins3, TypeChapitre".split(", ")
CHAMPS_ANNEXE_DATA_SIGNATURE = "Champ_Editeur, DtConvoc, DtDelib, DtPresent, DtPub, DtTransmPrefect, DtfFin, LibDelibLieu, LibDelibPar, LibFin, LibPresentLieu, LibPresentPar, LibReuniSession, NbrMembExer, NbrMembPresent, NbrSuffExprime, NbrVoteAbstention, NbrVoteContre, NbrVotePour".split(", ")
CHAMPS_ANNEXE_DATA_SIGNATAIRE = ["Signataire"]
CHAMPS_ANNEXE_DATA_ETAB_SERVICE = "Champ_Editeur, CodNatEtab, DtCreatEtab, DtDelibEtab, IndicTVAEtab, LibCatEtab, LibEtab, LibNatActivEtab, NumDelibEtab, SiretEtab".split(", ")
CHAMPS_ANNEXE_DATA_PRET = "Champ_Editeur, CodTypPret, DtDelib, MtCapitalExer, MtCapitalRestDu_01_01, MtCapitalRestDu_31_12, MtICNE, MtIntExer, NomBenefPret".split(", ")
CHAMPS_ANNEXE_DATA_CONTRAT_COUV_REFERENCE = "Champ_Editeur, CodProfilAmort, CodTyptxInit, DtDebEcheance, DureeAnn, IndexTxVariInit, LibObserv, MtCapitalExer, MtCapitalRestDu_01_01, MtCapitalRestDu_31_12, MtEmprOrig, MtIntExer, NumContr, NumContratEmprunt, TxActuaInit".split(", ")
CHAMPS_ANNEXE_DATA_SERVICE_FERROVIAIRE_BUD = "Champ_Editeur, CodChapitre, CodInvFonc, CodRD, CodRegroupBudFerrov, MtVentil".split(", ")
CHAMPS_ANNEXE_DATA_SERVICE_FERROVIAIRE_PATRIM = "Champ_Editeur, DtFinPot, DtMiseService, LibModeFinanc, LibProprietaire, LibRame, Matricule, MtAmort, MtVNC, MtValOrig".split(", ")
CHAMPS_ANNEXE_DATA_SERVICE_FERROVIAIRE_TER = "Champ_Editeur, CodCptTER, MtCptTER".split(", ")
CHAMPS_ANNEXE_DATA_FOND_COMM_HEBERGEMENT = "Champ_Editeur, CodOper, CodRD, LibEtabHeberg, LibFondHeberg, LibObjFond, MtFond".split(", ")
CHAMPS_ANNEXE_DATA_FOND_EUROPEEN = "Champ_Editeur, CodArticle, CodDestFonds, CodRDDJust, DtAcquit, LibBenef, LibEmetteurs, LibFondsEuropeen, LibMesure, LibOper, MtFond".split(", ")
CHAMPS_ANNEXE_DATA_FOND_EUROPEEN_PROGRAMMATION = "Avances, CodRD, MontantN, MontantN_X, Programmation, RappelTotal, RegulN, TypeFonds, TypeGestion".split(", ")
CHAMPS_ANNEXE_DATA_FOND_AIDES_ECO = "Champ_Editeur, CodArticle, CodInvFon, CodRD, DtConvent, DtVers, LibAide, LibBenef, LibFormeAide, LibOrgConvent, MtDExer, MtDExerAnt, MtReliquatCPAnt, MtTotAide, MtVersExer".split(", ")
CHAMPS_ANNEXE_DATA_FORMATION_PRO_JEUNES = "Champ_Editeur, CodApprent, CodRDTot, CodRessExt, MtFormN, MtFormN_1".split(", ")
CHAMPS_ANNEXE_DATA_MEMBRESASA = "Commune, Proprietaire, Superficie".split(", ")
CHAMPS_ANNEXE_DATA_FLUX_CROISES = "CodInvFonc, CodRD, CodTypFlux, MtCredOuv, MtRAR, MtReal".split(", ")
CHAMPS_ANNEXE_DATA_SOMMAIRE = "Champ_Editeur, CodeAnnexe, Present".split(", ")









