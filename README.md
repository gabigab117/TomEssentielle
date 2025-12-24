# TomEssentielle

1) Résumé initial
Tom Essentielle est un cabinet de naturopathie et d'hypnothérapie proposant des prestations, des programmes personnalisés et une boutique en ligne. Le projet vise à créer un site web interactif pour les clients et une application métier complète pour la gestion interne.

2) Objectifs
* Créer un site web comprenant :
    * Une boutique en ligne
    * Un système de réservation de rendez-vous en ligne
    * Un blog
* Créer une application métier comprenant:

3) Schéma rapide du parcours utilisateur public
VISITEUR PUBLIC
* Accueil
* Prestations
   * Liste des prestations
   * Détail des prestations
   * Réservations
      * Confirmation
* Boutique
   * Liste des produits
   * Détail des produits
   * Panier
      * Paiement
      * Confirmation
* Blog
   * Liste des articles
   * Détail des articles
      * Commentaires/like
* Collaborateurs
   * Liste des collaborateurs
   * Détail des collaborateurs

4) Priorisations des étapes
   Phase 1 : Site web fonctionnel
   * Partie utilisateur (accès sur toutes les pages)
       * Modèle utilisateur personnalisé hérité de AbstractBaseUser, pour formluaire, vues et templates, utilise django-allauth
   * Sécurité utilisateur
       * blocage compte au bout de 5 essaie infructueux
       * blocage IP si plus 20 tentatives de connexion par minute
       * Journal des connexions
       * (a complèter)
   * Partie boutique
      * Modèle catégorie, produit, panier, ligne du panier. Pour formulaire, vues et templates, utilise django-oscar
   * Partie blog
      * Modèle articles, utilisation de wagtail
   * Partie partenaires
      * Modèle partenaires, Vue (CRUD), Templates chaque partenaires peut modifier sa fiche
   Phase 2 : Applications métier (Gestion interne)
   * Fournisseur
      * Modèle fournisseur en lien avec le modèle produit-> en phase 3 scrapping pour actualisation des prix et comparaison
   * Produit :gestion des stocks, gestion des commandes étape (en préparation, expédié, en livraison, livré,...), alerte de stock bas
   * Comptabilité automatique : bon de commande, factures, devis, documents légaux (bilan, comptes de résultat, livres comptables,...) exportable en PDF pour impression et/ou envoie par mail
   * Tableau de bord : statistiques, rapport, graphiques (evolution CA, classement produit/prestations, marges, projections, ...) 
   Phase 3 : Evolutions et gestions ressources humaines
   * Employé : planning, gestion congés, suivi des heures, paie, dossiers employés
   * Chat bot et IA d'aide au choix d'achat
  
5) Composition de la page de base
   * Charte graphique
      * Couleurs : principale bleu #1e847f, secondaire beige #ecc19c, écriture principale blanc #ffffff, ecriture secondaire noir #000000
      * Police : principale Open Sans, secondaire : Kalam
   * Structure
      * header : logo centré, slogan "Votre Bien-être du Corps et de l'Esprit" (kalam, gras, blanc, 1,5rem), menu horizontal (Accueil, Prestations, Boutique, Blog, Collaborateurs)(Open sans, normal, blanc, 1rem)
      * Main :3 colonnes (20/60/20), gauche droite fond bleu, milieu fond beige. Sur colonne milieu bouton connexion/Inscription ou texte "Bonjour civlite non prenom"/déconnexion
      * Footer : Entreprise Tom Essentielle (kalam, gras, blanc, 1,2rem), Coordonées (Open sans, normal, blanc, 1rem), liens (mentions légales, CGVU,politique de confidentialité), barre copyright (fond blanc, blanc, normal, 1rem)
        
7) Etapes effectuées
 * Mise en place environnement
    * Dossier Tom Essentielle
    * Environnement virtuel : .venv
    * Installation :
       * django
       * django-environ
       * django-allauth
       * django-oscar
       * django-scheduler
       * django-livereload-server
       * wagtail
       * pytest
       * coverage
    * Freeze
    * Création projet : TomEssentielle
 * Réglage settings.py avec les documentations :
    * livereload
    * django-oscar
    * django-allauth
    * wagtail
 * Mise en place du .env avec django-environ: DJANGO_SECRET_KEY,DEBUG,ALLOWED_HOSTS,GOOGLE_ID,GOOGLE_SECRET
 * base.html
    * header : logo, slogan, menu
    * main : 3 colonnes
    * footer : entreprise, coordonnées, lien, copy
 * style.css
    * variables : bleu, beige, blanc, noir, rouge, polices
    * Initialisation HTML et body
    * .logo, .slogan, .entreprise, .adresse, .milieu, .copy, a
 *  responsive base.html
    * taille bootstrap sm
    * colonne de droite disparait
    * colonne de gauche se met entre colonne milieu et menu
    * menu hamburger
 * base.html
    * bouton connexion/inscription si utilisateur non connecté
    * texte/bouton déconnexion si utilisateur connecté
       * test affichage si utilisateur connecté
       * test affichage si utilisateur non connecté
 * style.css
    * btn
    * btn-custom
    * btn-danger
 * Création application utilisateur
    * settings.py ajout dans app
    * Ajout des fichiers/dossiers :
       * templates/utilisateur
       * forms.py
       * singals.py
       * urls.py
    * Ajout des urls dans urls.py du projet
 * planification modèle Utilisateur
    * ManagerUtilisateur(BaseUserManager)
       * méthodes :
          * create_user
          * create_superuser
             * Create_user
             * Is_staff :True
             * Is_admin: True
    * Utilisateur(AbstractBaseUser, PermissionMixin)
       * numéro : CharField -> ID-mmAAAA0000
       * email : EmailField
       * mot de passe : CharField -> min. 8 car, 1 maj, 1 min, 1 car spé
       * civilité : CharField -> choice
       * nom : CharField
       * prenom : CharField
       * slug : SlugField -> numéro client (slug auto)
       * adresse : CharField -> Numéro + rue
       * complément : CharField -> appartement, lieu-dit, étage, …
       * code postal : CharField -> 5 chiffres et que des chiffres
       * ville : CharField
       * téléphone : CharField -> 10 chiffres, commence par 0 et que des chiffres
       * date création : DateField
       * tentative : IntegerField (tentative de connexion)
       * date blocage : DateField
       * is_staff : BooleanField -> défaut False
       * is_active: BooleanField -> défaut True
       * is_admin : BooleanField -> defaut False
       * USERNAME_FIELD email
       * méthodes :
          * save()
          * clean()
    * Modèle Utilisateur
       * AUTH_USER_MODEL
       * paramètres django-allauth pour utilisateur personnalisé (à faire)
    * Migrations
    * Tests
       * Fixture utilisateur_cree
       * creation date
       * creation code utilisateur
       * creation slug
       * tel valide
       * tel – 10 chiffres
       * tel + 10 chiffres
       * tel pas que chiffres
       * tel vide
       * cp valide
       * cp – 5 chiffres
       * cp +5 chiffres
       * cp pas que chiffres
       * cp vide
       * email valide
       * email non valide
       * email vide
       * email en doublon
       * email mis en majuscule
       * email avec espace avant et après
       * civilité monsieur
       * civilité madame
       * civilité entreprise
       * civilité invalide
       * civilité vide
       * nom rempli
       * nom vide
       * prénom rempli
       * prénom vide
       * adresse rempli
       * adresse vide
       * complément rempli
       * complément vide
       * ville lettre uniquement
       * ville complexe
       * ville caractères spéciaux français
       * ville non-valide
       * ville vide
       * mdp valide
       * mdp pas enregistré en clair
       * mdp – 8 caractères
       * mdp sans lettre
       * mdp sans chiffre
       * mdp sans caractères spécial
       * mdp sans maj
       * mdp sans min
       * mdp vide
       * is_active, is_staff, is_superuser pour create user
       * is_active, is_staff, is_superuser pour create superuser
       * tentative et date blocage création du compte
 
9)  
