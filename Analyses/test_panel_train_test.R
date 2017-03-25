##############################################
#               OBJECTIF                     #
#     Comparer la performance MCO classique  #
#                   vs                       #
#       MCO avec effet individuel            #
#                                            #
#       Pour rappel mco : 0.8938             #
#                                            #
##############################################

library(plm)

# Import du train
train <- read.csv2("/home/brehelin/Documents/Elections/Analyses/base_train_gauche.csv",sep=",",dec=".")

# Import du test 
test <- read.csv2("/home/brehelin/Documents/Elections/Analyses/base_test_gauche.csv",sep=",",dec=".")


ptrain <- pdata.frame(train, index=c("département", "Année"), drop.index=TRUE, row.names=TRUE)


form <- as.formula(taux_gauche~ capacite.epargne.future.amélioration.moins.deterioration.+
                   taux_gauche_sup_moyenne+taux_vert_sup_moyenne
                   +taux_xgauche_sup_moyenne+pop_premier_ministre+pop_president+droite_au_pouvoir
                   +Dissident+persistance_gauche)

model_train <- plm(form, data=ptrain, model="random")
mae_model<- mean(abs(model_train$residuals))

test$predict <- model_train$coefficients[1] +
  model_train$coefficients[2]*test$capacite.epargne.future.amélioration.moins.deterioration. +
model_train$coefficients[3]*test$taux_gauche_sup_moyenne   +
model_train$coefficients[4]*test$taux_vert_sup_moyenne   +
model_train$coefficients[5]*test$taux_xgauche_sup_moyenne    +
model_train$coefficients[6]*test$pop_premier_ministre    +
model_train$coefficients[7]*test$pop_president    +
model_train$coefficients[8]*test$Dissident    +
model_train$coefficients[9]*test$persistance_gauche    

"""
MAE => 14.82 score très mauvais 
le  modèle de donnée de panel n'a pas de variable niveau dept => donnée de panel justifié?
le taux de chomage/ var chomage ne sont pas singificative sur ce modèle 
"""
