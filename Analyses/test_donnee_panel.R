# Import des library 
library(rpart)				        # Popular decision tree algorithm
library(rpart.plot)				# Enhanced tree plots
library(plm)
library(plyr)
# import des données
data <- read.csv2("/home/brehelin/Documents/Elections/Analyses/la_base.csv",sep=",",dec=".")


data$taux_tgauche <- data[,4] + data[,7] + data[,9]

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