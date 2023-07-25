"# EpicEvents_CRM" 


# <h1 align="center">EpicEvents_CRM</h1>
</br>
<p align="center">
    <img src="https://user.oc-static.com/upload/2020/09/22/16007804386673_P10.png" 
            alt="le logo de d'Epic Events" 
            width="250" 
            height="200"
            style="filter: invert(1)"/>
</p>


EpicEvents_CRM est un logiciel de gestion de la relation client (CRM) sécurisé interne à l'entreprise, qui effectue le suivi de tous les clients et événements.

# Installation :

1. Placez-vous dans le répertoire qui contiendra le projet 
  
2. Récupérer le code venant de GitHub (faire un clone) :  
    ```
    git clone https://github.com/glgstyle/EpicEvents_CRM.git
    cd EpicEvents_CRM
    ```
3. Créer un environnement virtuel : 

    ```python -m venv env```

4. Activer l'environnement :  

    ```source env/bin/activate ```

5. Installer les packages :

    ```pip install -r requirements.txt```  
    ```pip freeze``` (pour vérifier que les packages se sont bien installés)

6. Se placer dans le répertoire epic_crm:

    ```cd epic_crm```

# Utilisation

    Pour plus d'informations concernant les requêtes de l'API veuillez consulter la documentation ci dessous :
    https://documenter.getpostman.com/view/23089101/2s8YzXterj

- Pour utiliser le site:

1. Démarrer le serveur avec la commande suivante:

    ```python manage.py runserver```  

2. Rendez vous à l'adresse suivante dans votre navigateur internet:

    http://127.0.0.1:8000/  


- Pour gérer l'interface d'aministration:

1. Créer un super user avec la commande suivante:

    ```python manage.py createsuperuser```

2. Saisir le nom d’utilisateur souhaité et appuyez sur entrée exemple:

    ```Username: admin```

3. Saisir l’adresse mail souhaitée exemple:

    ```Email address: admin@example.com```

4. L’étape finale est de saisir le mot de passe. On vous demande de le saisir deux fois, la seconde fois étant une confirmation de la première:

    ```Password: **********```

    ```Password (again): *********```
    
    ```Superuser created successfully.```

5. À présent, ouvrez un navigateur Web et allez à l’URL « /admin/ » de votre domaine local – par exemple, http://127.0.0.1:8000/admin/.
   Vous devriez voir l’écran de connexion à l’interface d’administration.


# Tests

Pour tester le code un répertoire de tests à été crée contenant des tests unitaires, de performance et d'intégration. Nous avons utitlisé pytest. 

Pour lancer les tests tapper la commande suivante (pytest + le nom du répertoire): 

````pytest -s tests``

Pour mesurer le pourcentage de couverture des tests sur le project:

```pytest --cov=.```

# Conventions

Afin de respecter les conventions de code nommée PEP8 nous avons utilisé Flake8. Pour générer un rapport avec Flake8 tapper la commande suivante:

```flake8 --format=html --htmldir=flake-report```

# Technologies
    - Python v3.x+
    - Django Rest 
    - Postman
    - PostgreSQL

# Contribuer au project

    Soft Desk n'est pas un projet open source. Veuillez nous contacter pour contribuer avec vos propres fonctionnalités.

# Auteur

    Gwénaëlle