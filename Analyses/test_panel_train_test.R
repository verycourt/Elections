##############################################
#               OBJECTIF                     #
#     Comparer la performance MCO classique  #
#                   vs                       #
#       MCO avec effet individuel            #
#                                            #
#       Pour rappel mco : 0.8938             #
#                                            #
##############################################
# Remarque on n'utilise pas l'année 1981 pour le train 

library(plm)

# Import du train
train <- read.csv2("/home/brehelin/Documents/Elections/Analyses/base_train_gauche.csv",sep=",",dec=".")

# Import du test 
test <- read.csv2("/home/brehelin/Documents/Elections/Analyses/base_test_gauche.csv",sep=",",dec=".")


ptrain <- pdata.frame(train, index=c("d.partement", "Ann.e"), drop.index=TRUE, row.names=TRUE)


form <- as.formula(taux_gauche~ capacite.epargne.future.am.lioration.moins.deterioration.+
                   taux_gauche_sup_moyenne+taux_vert_sup_moyenne
                   +taux_xgauche_sup_moyenne+pop_premier_ministre+pop_president+droite_au_pouvoir
                   +Dissident+persistance_gauche)

model_train <- plm(form, data=ptrain, model="random")
mae_model<- mean(abs(model_train$residuals))

test$predict <- model_train$coefficients[1] +
  model_train$coefficients[2]*test$capacite.epargne.future.am.lioration.moins.deterioration. +
model_train$coefficients[3]*test$taux_gauche_sup_moyenne   +
model_train$coefficients[4]*test$taux_vert_sup_moyenne   +
model_train$coefficients[5]*test$taux_xgauche_sup_moyenne    +
model_train$coefficients[6]*test$pop_premier_ministre    +
model_train$coefficients[7]*test$pop_president    +
model_train$coefficients[8]*test$Dissident    +
model_train$coefficients[9]*test$persistance_gauche    

mean(abs(test$taux_gauche - test$predict))
"""
MAE => 14.82 score très mauvais 
le  modèle de donnée de panel n'a pas de variable niveau dept => donnée de panel justifié?
le taux de chomage/ var chomage ne sont pas singificative sur ce modèle 
"""

# Test avec bloc de gauche 
#data <- read.csv2("/home/brehelin/Documents/Elections/Analyses/la_base.csv",sep=",",dec=".")
#data$taux_tgauche <- data[,"taux_xgauche"] + data[,"taux_gauche"] + data[,"taux_vert"]


#test <- merge(train, data[,c("Ann.e","d.partement","taux_tgauche")],
#              by.x=c("Année","département"), by.y = c("Ann.e","d.partement"), all.x=TRUE)

form <- as.formula(taux_bgauche~ capacite.epargne.future.am.lioration.moins.deterioration.+
                     taux_gauche_sup_moyenne+taux_vert_sup_moyenne
                   +taux_xgauche_sup_moyenne+pop_premier_ministre+pop_president
                   +Dissident+persistance_gauche+var_chomage_annee)

model_bloc_gauche <- plm(form, data=ptrain, model="random")
summary(model_bloc_gauche)
mae_model_bloc_gauche<- mean(abs(model_bloc_gauche$residuals))

# Au premier abord le MAE est déja plus faible
# R2 est plus important est nos variable sont bcp plus significative 

test$predict_bgauche <- model_bloc_gauche$coefficients[1] +
  model_bloc_gauche$coefficients[2]*test$capacite.epargne.future.am.lioration.moins.deterioration. +
  model_bloc_gauche$coefficients[3]*test$taux_gauche_sup_moyenne   +
  model_bloc_gauche$coefficients[4]*test$taux_vert_sup_moyenne   +
  model_bloc_gauche$coefficients[5]*test$taux_xgauche_sup_moyenne    +
  model_bloc_gauche$coefficients[6]*test$pop_premier_ministre    +
  model_bloc_gauche$coefficients[7]*test$pop_president    +
  model_bloc_gauche$coefficients[8]*test$Dissident    +
  model_bloc_gauche$coefficients[9]*test$persistance_gauche   +
  model_bloc_gauche$coefficients[10]*test$var_chomage_annee 

mean(abs(test$taux_bgauche - test$predict_bgauche))

"""
Constat les prédictions du bloc de gauche sont déja plus proche que lorsqu'on tente de prédire seulement la gauche
l'érreur est tout de même très importantes avec 7 pts en moyenne 
"""