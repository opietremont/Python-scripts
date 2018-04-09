# Python-scripts
## revoke_sharedaccess.py
Ce script permet de révoquer les accès de partage d'un utilisateur à partir de son adresse mail. Il demande un fichier contenant une liste d'adresse mail et utilise l'outil gdrive https://github.com/prasmussen/gdrive afin de supprimer les accès.
  ### Prerequisites:
```
homebrew: https://brew.sh/index_fr
python: brew install python
gdrive: https://github.com/prasmussen/gdrive
```
  ### Initialisating (token Google API)
à partir d'un terminal
```
~:/gdrive list
suivez les instructions.
```
  ### Exécution
à partir d'un terminal
```
~:/./revoke_sharedaccess.py
Il demande le fichier texte contenant la liste d'adresse mail.
Il propose de créer un fichier contenant la liste des fichiers possédant comme utilisateur ayant des droits de partage,  l'adresse mail extraite.
Il propose de supprimer les droits de partage de l'adresse mail extraite sur l'ensemble des fichiers la possédant comme utilisateur ayant des droits de partage.
```

