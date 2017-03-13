# Import des library 
library(rpart)				        # Popular decision tree algorithm
library(rpart.plot)				# Enhanced tree plots
library(plm)
# import des données
data <- read.csv2("/home/brehelin/Documents/Elections/Analyses/la_base.csv",sep=",")


data$taux_tgauche <- as.numeric(as.character(data[,4])) + as.numeric(as.character(data[,7])) + as.numeric(as.character(data[,9]))

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

