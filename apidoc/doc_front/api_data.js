define({ "api": [
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./doc_front/main.js",
    "group": "/Users/noah/MesDocuments/TAL/TAL_M2_INALCO/Semestre_2/technique_web/projet_groupe/front/doc_front/main.js",
    "groupTitle": "/Users/noah/MesDocuments/TAL/TAL_M2_INALCO/Semestre_2/technique_web/projet_groupe/front/doc_front/main.js",
    "name": ""
  },
  {
    "type": "Get",
    "url": "/Date/get",
    "title": "fonction \"get\"",
    "name": "DataGet",
    "group": "ClassData",
    "description": "<p>On vérifié que le client est bien connecté grâce à la présence du token dans le cookie, Sinon on redirige vers une page d'erreur</p>",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "html",
            "optional": false,
            "field": "resp",
            "description": "<p>renvoie la page html https://ceptyconsultant.localhost/data et afficher tous les données si public_id non saisi et contrib_name non saisi, tous les données avec le contrib_name requis si public_id non saisi, seulement l'unité de donnée correspond aux contrib_name et public_id requis.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "login_error",
            "description": "<p>connection échoué.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "donn",
            "description": "<p>ée_non_trouvées aucune donnée a été trouvée</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./api_front.py",
    "groupTitle": "ClassData"
  },
  {
    "type": "Post",
    "url": "/Date/post",
    "title": "fonction \"post\"",
    "name": "DataPost",
    "group": "ClassData",
    "description": "<p>Gère l'ajout, la modification et la suppression des données</p>",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "html",
            "optional": false,
            "field": "resp1",
            "description": "<p>Si une suppresion est demandée on récupère l'article_id dans les données du formulaire puis et on supprime l'élément associé par la requête 'delete', et renvoie une page html contenant un message 'suppression avec succès'</p>"
          },
          {
            "group": "Success 200",
            "type": "html",
            "optional": false,
            "field": "resp2",
            "description": "<p>Si une modification est demandée on récupère les données à modifier et l'article_id envoyés par le formulaire puis on effectue la modification avec la méthode 'post', et renvoie une page html contenant un message 'modification avec succès'</p>"
          },
          {
            "group": "Success 200",
            "type": "html",
            "optional": false,
            "field": "resp3",
            "description": "<p>Si un ajout est demandé, on recupère les données envoyées par le formulaires et on créé le nouvel élément grâce à la méthode 'put', et renvoie une page html contenant un message 'ajout avec succès'</p>"
          },
          {
            "group": "Success 200",
            "type": "html",
            "optional": false,
            "field": "resp4",
            "description": "<p>Si une recherche est demandée on redirige vers la méthode get de data avec une url personnalisée en fonction des données recherchées, et renvoie une page html contenant les données recherchées.</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "login_error",
            "description": "<p>connection échoué.</p>"
          },
          {
            "group": "Error 4xx",
            "optional": false,
            "field": "data_error",
            "description": "<p>article_id existe déjà.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./api_front.py",
    "groupTitle": "ClassData"
  },
  {
    "type": "Get",
    "url": "Licence/get",
    "title": "Get licence",
    "name": "LicenseGet",
    "group": "ClassLicense",
    "description": "<p>On vérifié que le client est bien connecté grâce à la présence du token dans le cookie, sinon on redirige vers une page d'erreur</p>",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "html",
            "optional": false,
            "field": "resp",
            "description": "<p>renvoie la page https://ceptyconsultant/license</p>"
          }
        ]
      }
    },
    "error": {
      "fields": {
        "Error 4xx": [
          {
            "group": "Error 4xx",
            "type": "html",
            "optional": false,
            "field": "_login_error",
            "description": "<p>redirige vers la page d'erreur https://ceptyconsultant/login_error avec un bouton qui dirige vers la connection, si le bouton est appuyé, la page de login apparaît.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./api_front.py",
    "groupTitle": "ClassLicense"
  },
  {
    "type": "Get",
    "url": "Login/get",
    "title": "fonction \"get\" dans la class Login",
    "name": "LoginGet",
    "group": "ClassLogin",
    "description": "<p>Envoie le formulaire à remplir pour se connecter. Si il y a un token dans le cookie alors il est supprimée. Ceci permet de gérer la déconnexion automatique lorsqu'on recharge la page de login ou lorsque qu'une redirection est effectuée</p>",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "html",
            "optional": false,
            "field": "resp",
            "description": "<p>redirige vers la page de login, cette méthode est un lien avec le lien avec la méthode post.</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./api_front.py",
    "groupTitle": "ClassLogin"
  },
  {
    "type": "Post",
    "url": "Login/post",
    "title": "fonction \"post\" dans la classe Login",
    "name": "post",
    "group": "ClassLogin",
    "description": "<p>Récupére les informations du formulaire de login et envoie une requête post au backend qui renvoie le token, le stock dans un cookie puis redirige vers les données. Si les identifiants sont incorrects alors une page de message d'erreur est renvoyée</p>",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "html",
            "optional": false,
            "field": "resp",
            "description": "<p>retourne la page https://ceptyconsultant.localhost/data</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./api_front.py",
    "groupTitle": "ClassLogin"
  },
  {
    "type": "Get",
    "url": "/_check_cookie_auth",
    "title": "Check cookie",
    "name": "checkCookie",
    "group": "Main",
    "description": "<p>Vérifie qu'il y a bien un cookie nommé token dans le navigateur</p>",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "resp",
            "description": "<p>retourne le token récupéré depuis le navigateur</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./api_front.py",
    "groupTitle": "Main"
  },
  {
    "type": "Get",
    "url": "/_login_error",
    "title": "login error",
    "name": "loginError",
    "group": "Main",
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "HTML",
            "optional": false,
            "field": "resp",
            "description": "<p>retourne la page login_error.html</p>"
          }
        ]
      }
    },
    "version": "0.0.0",
    "filename": "./api_front.py",
    "groupTitle": "Main"
  }
] });
