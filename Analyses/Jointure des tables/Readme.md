# Nomenclature des tables 


## Table : base_caf_dgi.csv

Cette base contient pour chaque département toutes les informations disponibles provenant de la Caf et des Impots.

**Granularité** : Départements  




| Variables       | Descriptions | Années Disponibles |
| ------------- |:-------------:| -----:|
| code      | Numéro du département |	|
| département | Libellé du département     |	| 
| reg      | Numéro de région du département |  |
| année      | année d'observation |	1993 - 2015 |
| alf      | le nombre de foyers allocataires percevant l'allocation de logement familiale (AFL) | 1993-2015	| 
| af    | le nombre de foyer bénéficiaires d'un droit payable aux allocations familiales (AF)    | 1993-2015	|
| apl    | le nombre de foyer bénéficiaires d'un droit payable aux allocations familiales (AF)    | 1993-2015	|
| TxFonBat | Taxe Foncière sur les Propriétés  Bâties (Taux d'imposition votés)     | 2000-2015|
| TXFonNonBat     | Taxe Foncière sur les Propriétés  Non  Bâties (Taux d'imposition votés) | 2000-2010|
| TxPro  | Taxe Professionnelle (Taux d'imposition votés)      | 2000-2010 |  
| TxHab | Taxe Habitation (Taux d'imposition votés)      | 2000-2010 |



## Table : base_caf.csv

code : Numéro du département  
reg : Numéro de région du département  
alf(N) : Pour l'année N, à fin décembe, le nombre de foyers allocataires percevant l'allocation de logement familiale (AFL)  
af(N) : Pour l'année N, à fin décembre, le nombre de foyers bénéficiaires d'un droit payable aux allocations familiales (AF)  
apl(N) : Pour l'année N, à fin décembre, le nombre de foyers allocataires percevant l'aide personnalisée au logement (APL)

## Table : base_impots.csv

code : Numéro du département  
départements : Libellé du département  
TxFonBat_an(N): Pour l'année N, Taxe Foncière sur les Propriétés  Bâties (Taux d'imposition votés)  
TXFonNonBat_an(N) : Pour l'année N, Taxe Foncière sur les Propriétés  Non  Bâties (Taux d'imposition votés)  
TxPro_an(N) : Pour l'année N, Taxe Professionnelle (Taux d'imposition votés)  
TxHab_an(N) : Pour l'année N, Taxe Habitation (Taux d'imposition votés)  