# Nomenclature des tables 


## Table : base_caf_dgi.csv

Cette base contient pour chaque département toutes les informations disponibles provenant de la Caf et des Impots.

**Granularité** : Départements


| Variables       | Descriptions |
| ------------- |:-------------:| 
| code      | Numéro du département | 
| reg      | Numéro de région du département |   
| départements | Libellé du département     |
| alf*      | Pour l'année *, le nombre de foyers allocataires percevant l'allocation de logement familiale (AFL) | 
| af*    | Pour l'année *, le nombre de foyer bénéficiaires d'un droit payable aux allocations familiales (AF)    |   
| Tx_FonBat_an* | Pour l'année *, Taxe Foncière sur les Propriétés  Bâties (Taux d'imposition votés)     |
| TX_FonNonBat_an*     | Pour l'année *, Taxe Foncière sur les Propriétés  Non  Bâties (Taux d'imposition votés) | 
| Tx_Pro_an*  | Pour l'année *, Taxe Professionnelle (Taux d'imposition votés)      |   
| Tx_Hab_an* | Pour l'année *, Taxe Habitation (Taux d'imposition votés)      |


## Table : base_caf.csv

code : Numéro du département
reg : Numéro de région du département
alf* : Pour l'année *, à fin décembe, le nombre de foyers allocataires percevant l'allocation de logement familiale (AFL)
af* : Pour l'année *, à fin décembre, le nombre de foyer bénéficiaires d'un droit payable aux allocations familiales (AF)

## Table : base_impots.csv

code : Numéro du département
départements : Libellé du département
Tx_FonBat_an* : Pour l'année *, Taxe Foncière sur les Propriétés  Bâties (Taux d'imposition votés)
TX_FonNonBat_an* : Pour l'année *, Taxe Foncière sur les Propriétés  Non  Bâties (Taux d'imposition votés)
Tx_Pro_an* : Pour l'année *, Taxe Professionnelle (Taux d'imposition votés)
Tx_Hab_an* : Pour l'année *, Taxe Habitation (Taux d'imposition votés)