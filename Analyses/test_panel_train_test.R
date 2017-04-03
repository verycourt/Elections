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
library(rpart)				  
library(rpart.plot)	
library(caret)

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
test_var <- train 
test_var$taux_sortie_sans_bloc<- NULL
test_var$taux_sortie_avec_bloc<- NULL
test_var$d.partement<- NULL                                                   
test_var$Ann.e<- NULL                                                          
test_var$taux_gauche<- NULL


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

# On veut tester la prédiction d'un modèle qui prédit le pourcentage de voix de la majorité sortante
# contrairement aux test précédent on utilise l'année 1981 pour nos prédictions

test_var <- train 
test_var$taux_bgauche<- NULL
test_var$taux_sortie_sans_bloc<- NULL
test_var$d.partement<- NULL                                                   
test_var$Ann.e<- NULL                                                          
test_var$taux_gauche<- NULL

tree_var_importance <- rpart(taux_sortie_avec_bloc~., test_var)


lm_var_importance <- step(lm(taux_sortie_avec_bloc~.,data=test_var),direction="both")

form <- as.formula(taux_sortie_avec_bloc~  
                     taux_sortie_avec_bloc ~ X20.39ans + X40.59ans + 
                     X60.74ans + Naissances.domicili.es.par.d.partement + Nombre.total.de.mariages.domicili.s + 
                     var_chomage_annee + taux_centre_sup_moyenne + taux_droite_sup_moyenne + 
                     taux_gauche_sup_moyenne + taux_xdroite_sup_moyenne + pop_droite + 
                     pop_xgauche + Dissident + Superficie + pres_xgauche
                      )

model_sortie_sans_bloc <- plm(form , data=ptrain, model="random")
summary(model_sortie_sans_bloc)

# ==> le score est meilleur sur le bloc de gauche sortie que sur la gauche partie socialiste 
# Score pas très satisfaisant
# TO DO : créer des features de sortie 

data_var<-subset(train, train$Ann.e > 1981)
ptrain <- pdata.frame(data_var, index=c("d.partement", "Ann.e"), drop.index=TRUE, row.names=TRUE)

form <- as.formula(taux_sortie_avec_bloc~var_chomage_annee+cohabitation+droite_au_pouvoir
                   +ecart_pop+pop_exec+taux_droite_sup_moyenne+taux_gauche_sup_moyenne+
                     taux_xgauche_sup_moyenne+taux_vert_sup_moyenne
)

model_sortie_avec_bloc <- plm(form , data=ptrain, model="random")

##############################################
#       Test sur xdroite                     #
#                                            #
##############################################
# Import du train
train <- read.csv2("/home/brehelin/Documents/Elections/Analyses/base_train_xdroite.csv",sep=",",dec=".")

# Import du test 
test <- read.csv2("/home/brehelin/Documents/Elections/Analyses/base_test_xdroite.csv",sep=",",dec=".")

train<-subset(train, train$Ann.e > 1981)

train_var <- train 
train_var$d.partement<- NULL                                                   
train_var$Ann.e<- NULL                                                          
test_var <- test
test_var$d.partement<- NULL                                                   
test_var$Ann.e<- NULL           

scale_train_var <- scale(train_var)
scale_train_var <-subset(scale_train_var ,select=-c(taux_xdroite))
scale_train_var <- as.data.frame(scale_train_var)
scale_train_var$taux_xdroite <- train$taux_xdroite

scale_test_var <- scale(test_var)
scale_test_var <-subset(scale_test_var ,select=-c(taux_xdroite))
scale_test_var <- as.data.frame(scale_test_var)
scale_test_var$taux_xdroite <- test$taux_xdroite

####################
##     TREE       ##
####################
tree_var_importance <- rpart(taux_xdroite~., train_var,method="anova")
tree_prune <- prune(tree_var_importance,cp=10e-5)
rpart.plot(tree_prune)
test$prune<-predict(tree_prune, test)
# R ne conserve pas les memes variables
# On normalise nos features pour être sur que R ne converse pas les mêmes variables
# Puis il faut tester la perf

tree_var_importance <- rpart(taux_xdroite~., scale_train_var ,method="anova")
tree_prune <- prune(tree_var_importance,cp=10e-5)
rpart.plot(tree_prune)
test$prune_scale<-predict(tree_prune, scale_test_var) 
# Meme scale les résultats sont différents....
# Remarque FN = > supprimer une Année ou ils ont à zero
# quand on scale les data on a la variables subventions qui devient pertinante
mean(abs(test$taux_xdroite - test$prune))
mean(abs(test$taux_xdroite - test$prune_scale))
# Perfomance meileurs sans scale...

####################
##       REG      ##
####################

lm_var_importance <- step(lm(taux_xdroite~.,data=train_var),direction="both")
test$lm<-predict(lm_var_importance, test) 


lm_var_importance <- step(lm(taux_xdroite~.,data=scale_train_var),direction="both")
test$scale_lm<-predict(lm_var_importance, scale_test_var) 
mean(abs(test$taux_xdroite - test$lm))
mean(abs(test$taux_xdroite - test$lm_scale))

lm_notebook <- lm(taux_xdroite~taux_xdroite_sup_moyenne+subventions+droite_au_pouvoir, train)
test$lm<-predict(lm_notebook, test) 
mean(abs(test$taux_xdroite - test$lm))

# La méthode step ne fonctionne pas bien car bcp de liaison entre nos variables
# on le vérifie juste avec la reg lm_notebook

###### Performance des arbres assez remarquable ici ########

################################
##     Modèle effet indiv     ##
################################

form <- as.formula(taux_xdroite~ subventions + capacit..epargne.actuelle..augmentation.moins.diminution.+
                     var_chomage_annee+X40.59ans+Naissances.domicili.es.par.d.partement+
                     Densit.)

model_train <- plm(form, data=train, model="within")
summary(model_train)
test$panel<-predict(model_train ,test) 