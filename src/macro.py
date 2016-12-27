BIENVENUE = 10
START = 11
QUELLE_CASE = 12
PLAY = 1

#Il est trop compliqué de coder en dur les messages côté serveur. Il vaut mieux
#n'envoyer qu'un seul type de variable et de traiter cas par cas.
#Ici, des int (toujours sous forme de bytes).
#Côté client, on a un cas pour chaque entier possible.
#Par exemple si il reçoit l'entier 10 (BIENVENUE), il fera juste un print "Bienvenue".
#Si il reçoit l'entier 1 (PLAY), alors il printera "Quelle case voulez-vous jouer"
#et demandera à l'utilisateur de rentrer une case à jouer, puis enverra la valeur au serveur.
