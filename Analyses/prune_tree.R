library(rpart)				  
library(rpart.plot)	

data <- read.csv2("/home/brehelin/Documents/Elections/Analyses/base_train_gauche.csv",sep=",",dec=".")


form <- as.formula(data[,51]~ depart_frontalier+depart_CORSE+                                                   
   X0.19ans + X20.39ans                                                      
                   + X40.59ans                                                      
                   + X60.74ans                                                      
                   + X75.ans                                                        
                   + Naissances.domiciliées.par.département                         
                   + Nombre.total.de.mariages.domiciliés                            
                   + Décès.domiciliés.par.département                               
                   + var_chomage_annee                                              
                   + taux_chomage                                                   
                   + taux_centre_sup_moyenne                                        
                   + taux_droite_sup_moyenne                                        
                   + taux_gauche_sup_moyenne                                        
                   + taux_vert_sup_moyenne                                          
                   + taux_xdroite_sup_moyenne                                       
                   + taux_xgauche_sup_moyenne                                       
                   + taux_Abstention_sup_moyenne                                    
                   + taux_Blancs.et.nuls_sup_moyenne                                
                   + pop_centre                                                     
                   + pop_droite                                                     
                   + pop_gauche                                                     
                   + pop_xdroite                                                    
                   + pop_xgauche                                                    
                   + pop_premier_ministre                                           
                   + cohabitation                                                   
                   + pop_president                                                  
                   + droite_au_pouvoir                                              
                   + Dissident                                                      
                   + Superficie                                                     
                   + Densité                                                        
                   + persistance_gauche                                             
                   + persistance_droite                                             
                   + persistance.centre                                             
                   + persistance_centre_droite                                      
                   + pres_centre                                                    
                   + pres_droite                                                    
                   + pres_gauche                                                    
                   + pres_xgauche                                                   
                   + importations                                                   
                   + subventions                                                    
                   + conjoncture.travaux.publics.opinions.sur.le.carnet.de.commandes
                   + capacité.epargne.actuelle..augmentation.moins.diminution.      
                   + opportunite.epargner.favorable.moins.favorable.                
                   + capacite.epargne.future.amélioration.moins.deterioration.      
                   + densité_médecins                                               
                   + consommation.menages...electricite                             
                   + nombre.de.logement.vacant                                      
                   + Date)          

tree <- rpart(form,data=data)
tree_prune <- prune(tree,cp=10e-5)
rpart.plot(tree_prune)
