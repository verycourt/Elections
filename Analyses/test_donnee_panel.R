# Import des library 
library(rpart)				        # Popular decision tree algorithm
library(rpart.plot)				# Enhanced tree plots
library(plm)
library(plyr)
# import des données
data <- read.csv2("/home/brehelin/Documents/Elections/Analyses/la_base.csv",sep=",",dec=".")


data$taux_tgauche <- data[,"taux_xgauche"] + data[,"taux_gauche"] + data[,"taux_vert"]

# On va utiliser un decision tree pour regarder quels variales sont discriminante de manière naives

form <- as.formula(taux_tgauche~depart_frontalier+depart_OM+depart_CORSE+X0.19ans+X20.39ans+X40.59ans+
                X60.74ans+X75.ans+Total+Naissances.domicili.es.par.d.partement+Nombre.total.de.mariages.domicili.s+
                 D.c.s.domicili.s.par.d.partement+Q3_rate)

tree <- rpart(form,data=data)

summary(tree)
# On va tester les données de panel sur ces données déja
#Naissances.domicili.es.par.d.partement    
#Nombre.total.de.mariages.domicili.s       
#D.c.s.domicili.s.par.d.partement 
#X40.59ans                              
#X60.74ans                               
#X0.19ans 
#Q3_rate


# On va tester l'homogeneite global
predict_formula <- as.formula(taux_tgauche~
                                Naissances.domicili.es.par.d.partement+Nombre.total.de.mariages.domicili.s+
                                D.c.s.domicili.s.par.d.partement+Q3_rate)

# Transformer les données en donnée de panel

E <- pdata.frame(data, index=c("d.partement", "Ann.e"), drop.index=TRUE, row.names=TRUE)
E$code <- NULL

# Premier test d'homogeneite global
# Pvcm errur pas suffisament de donnée...
znp <- pvcm(predict_formula, data=E, model="within")
zplm <- plm(predict_formula, data=E, model="within")
pooltest(zplm,znp)

pooltest(predict_formula, data=E, model="within")

# On tente le test d'homogeneite de alpha
# Me renvoi une p-value NA
pplm <- plm(predict_formula, data=E, model="pooling")
plm <- plm(predict_formula, data=E, model="within")
pooltest(pplm, plm)


# On tente les test uniquement sur les années où toute les données sont disponible
#### TEST #### 
#data$Ann.e <- as.numeric(as.character(data[,3]))
#data$var_chomage_annee <- as.numeric(as.character(data$var_chomage_annee))
#data$depart_frontalier <- as.numeric(as.character(data$depart_frontalier))
#data$depart_CORSE <- as.numeric(as.character(data$depart_CORSE))
#data$Naissances.domicili.es.par.d.partement <- as.numeric(as.character(data$Naissances.domicili.es.par.d.partement))
#subset(data, data$Ann.e > 1990)
data_var<-subset(data, data$Ann.e > 1990)
data_var$code <- NULL
formula_var <- as.formula(taux_tgauche~depart_frontalier+depart_CORSE+var_chomage_annee)

E_var <- pdata.frame(data_var, index=c("d.partement", "Ann.e"), drop.index=TRUE, row.names=TRUE)
E_var$code <- NULL

#plm <- plm(taux_tgauche ~ Naissances.domicili.es.par.d.partement+var_chomage_annee+depart_frontalier+depart_CORSE, data=data_var, model="random")
znp <- pvcm(taux_tgauche ~ var_chomage_annee + D.c.s.domicili.s.par.d.partement, data=data_var, model="within")
zplm <- plm(taux_tgauche ~ var_chomage_annee + D.c.s.domicili.s.par.d.partement, data=data_var, model="within")
pooltest(zplm,znp)

test_data_ain <- subset(data_var, data_var$d.partement=="AIN")

# Le test d'homogeneite ne fonctionner pas car dans le premier pvcm
# on tente autant de regression que de département mais on ne peut avoir
# p > n donc avec n = 4 cela causé des pb
# Question : peut on pratiquer les test pour avoir un avis puis changer l'équation??

# Test hypothèse sur la variable de chomage et de décès domicilié par département
znp <- pvcm(taux_tgauche ~ var_chomage_annee + D.c.s.domicili.s.par.d.partement, data=data_var, model="within")
zplm <- plm(taux_tgauche ~ var_chomage_annee + D.c.s.domicili.s.par.d.partement, data=data_var, model="pooling")
pooltest(zplm,znp)
# On rejette l'hypothèse d'homogeneité global 
znp <- pvcm(taux_tgauche ~ var_chomage_annee + D.c.s.domicili.s.par.d.partement, data=data_var, model="within")
zplm <- plm(taux_tgauche ~ var_chomage_annee + D.c.s.domicili.s.par.d.partement, data=data_var, model="within")
pooltest(zplm,znp)
# on ne rejtte pas l'hypothèse null sur le test d'homogeneite de beta 
# La structure de panel est deja justifié 
znp <- plm(taux_tgauche ~ var_chomage_annee + D.c.s.domicili.s.par.d.partement, data=data_var, model="pooling")
zplm <- plm(taux_tgauche ~ var_chomage_annee + D.c.s.domicili.s.par.d.partement, data=data_var, model="within")
pooltest(znp,zplm)
# On rejette H0 => modele à effet aléatoire il reste à savoir
# si on est en dans un modèle à effet fixe ou aléatoire
# test de haussman
znp <- plm(taux_tgauche ~ var_chomage_annee + D.c.s.domicili.s.par.d.partement, data=data_var, model="within")
zplm <- plm(taux_tgauche ~ var_chomage_annee + D.c.s.domicili.s.par.d.partement, data=data_var, model="random")
phtest(znp,zplm)
# On ne eejette H0, on peut donc specifié notre modèle avec des effets individuelles aléatoires


# On va tester un modèle entrainer sur les années supérieur à 81
data_train<-subset(data, data$Ann.e > 1981)
data_train$code <- NULL
# On teste un premier modèle relativement simple
# On étudie la corrélation entre y et X des pop pour savoir quel pop supprimer
cor(data_train[,c("taux_tgauche","X0.19ans","X20.39ans","X40.59ans","X60.74ans","X75.ans")])
# On supprime la pop la moins corrélé à la cible (de manière générale la corrélation est faible)


cor(data_train[,c("taux_tgauche","taux_centre_sup_moyenne"
                  ,"taux_droite_sup_moyenne",                "taux_gauche_sup_moyenne"
                  ,"taux_vert_sup_moyenne" ,                 "taux_xdroite_sup_moyenne"
                  ,"taux_xgauche_sup_moyenne",               "taux_Abstention_sup_moyenne"
                  ,"taux_Blancs.et.nuls_sup_moyenne" )])

data_train$taux_tgauche_sup_moyenne <- data_train[,"taux_gauche_sup_moyenne"] + 
  data_train[,"taux_vert_sup_moyenne"] + data_train[,"taux_xgauche_sup_moyenne"]

# mise à 0 des NA sur la popularité des verts 
data_train[is.na(data_train[,"pop_verts"]),"pop_verts"]<-0
data_train$pop_tgauche <- data_train[,"pop_gauche"] + 
  data_train[,"pop_verts"] + data_train[,"pop_xgauche"]

cor(data_train[,c("taux_tgauche","taux_centre_sup_moyenne"
                  ,"taux_droite_sup_moyenne", "taux_tgauche_sup_moyenne"
                  ,"taux_xdroite_sup_moyenne"
                )])

formula_var1 <- as.formula(taux_tgauche~depart_frontalier+depart_CORSE+var_chomage_annee+
                            X0.19ans+X20.39ans+X40.59ans+X75.ans+Naissances.domicili.es.par.d.partement+
                           taux_Abstention_sup_moyenne+taux_centre_sup_moyenne+
                           taux_droite_sup_moyenne + taux_tgauche_sup_moyenne+
                          taux_xdroite_sup_moyenne+pop_tgauche )

data_train_panel <- pdata.frame(data_train, index=c("d.partement", "Ann.e"), drop.index=TRUE, row.names=TRUE)

model_test1 <- plm(formula_var1, data=data_train_panel, model="random")


formula_var2 <- as.formula(taux_tgauche~var_chomage_annee+
                            X20.39ans+X40.59ans+X75.ans+Naissances.domicili.es.par.d.partement+
                             taux_centre_sup_moyenne+
                             taux_droite_sup_moyenne + taux_tgauche_sup_moyenne+
                             taux_xdroite_sup_moyenne + pop_tgauche)
model_test2 <- plm(formula_var2, data=data_train_panel, model="random")

# On observe des signes de coeficients très suspect, relation positive entre chomage et gauche?
mse_model_test2 <- mean(model_test2$residuals^2)
mae_mode_test_2 <- mean(abs(model_test2$residuals))

# Next step :
# - modifier les indicateurs de pop_tgauche/ taux_tgauche
# - refaire un arbre pour utiliser les variables les plus discriminantes

data_train$taux_tmean_gauche_sup_moyenne <- data_train$taux_tgauche_sup_moyenne/ 3

data_train$pop_tmean_gauche <- 0  

data_train[data_train$Ann.e==1988, "pop_tmean_gauche"]<-data_train[data_train$Ann.e==1988, "pop_tgauche"]/ 2
data_train[data_train$Ann.e!=1988, "pop_tmean_gauche"]<-data_train[data_train$Ann.e!=1988, "pop_tgauche"]/ 3


# Faire un decision tree et garder variable les plus discriminante

                                
form <- as.formula(taux_tgauche~depart_frontalier+depart_OM+depart_CORSE+X0.19ans+X20.39ans+X40.59ans+
                     X60.74ans+X75.ans+Naissances.domicili.es.par.d.partement+Nombre.total.de.mariages.domicili.s+
                     D.c.s.domicili.s.par.d.partement+var_chomage_annee+taux_centre_sup_moyenne+taux_droite_sup_moyenne
                  + taux_xdroite_sup_moyenne + taux_Abstention_sup_moyenne+taux_Blancs.et.nuls_sup_moyenne
                  +pop_droite + pop_centre + pop_xdroite + taux_tmean_gauche_sup_moyenne +
                    taux_tgauche_sup_moyenne + pop_tgauche + pop_tmean_gauche)

tree <- rpart(form,data=data_train)

data_train_panel <- pdata.frame(data_train, index=c("d.partement", "Ann.e"), drop.index=TRUE, row.names=TRUE)

formula_var3 <- as.formula(taux_tgauche~var_chomage_annee+ X0.19ans + 
                             X20.39ans+X40.59ans+X75.ans+Naissances.domicili.es.par.d.partement+
                             taux_centre_sup_moyenne+taux_Blancs.et.nuls_sup_moyenne+
                             taux_droite_sup_moyenne + taux_tmean_gauche_sup_moyenne+ taux_centre_sup_moyenne + 
                             taux_xdroite_sup_moyenne + pop_tmean_gauche + pop_droite + pop_centre 
                           + pop_xdroite )

model_test3 <- plm(formula_var3, data=data_train_panel, model="random")

# On observe des signes de coeficients très suspect, relation positive entre chomage et gauche?
mse_model_test3 <- mean(model_test3$residuals^2)
mae_mode_test_3 <- mean(abs(model_test3$residuals))

formula_var4 <- as.formula(taux_tgauche~var_chomage_annee+ taux_centre_sup_moyenne 
                           + taux_tmean_gauche_sup_moyenne+ taux_centre_sup_moyenne + 
                             taux_xdroite_sup_moyenne + pop_tmean_gauche + pop_droite + pop_centre 
                           + pop_xdroite )

model_test4 <- plm(formula_var4, data=data_train_panel, model="random")

# On observe des signes de coeficients très suspect, relation positive entre chomage et gauche?
mse_model_test4 <- mean(model_test4$residuals^2)
mae_mode_test_4 <- mean(abs(model_test4$residuals))

## ECART DE POPULARITE ENTRE PREMIER MINISTRE ET PRESIDENT
## VOIX OBTENU AU SCRUTE PRECEDENT
