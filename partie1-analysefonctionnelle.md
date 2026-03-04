# Partie 1 – Analyse fonctionnelle

## Cas métier : Application de calcul automatisé pour la broderie

---

# 1. Approche globale

## Compréhension du besoin métier

L’objectif de l’application est d’aider un atelier de broderie à transformer une image en données exploitables pour la production.

Concrètement, le système doit :

- Identifier les couleurs présentes dans l’image
- Calculer la surface associée à chaque couleur
- Estimer la quantité de fil nécessaire
- Estimer le temps ou le coût de production

L’enjeu principal est donc de relier une analyse technique d’image à des estimations métier utiles pour l’atelier.

---

## Découpage du traitement

Pour structurer la solution, je propose de découper le traitement en étapes successives.

### 1. Réception et stockage de l’image

La première étape consiste à récupérer l’image fournie par l’utilisateur et à vérifier qu’elle est exploitable.

- Upload d’un fichier (PNG, JPEG,...)
- Vérification du format et de la taille
- Extraction de métadonnées (dimensions en pixels, éventuellement DPI)
- Stockage de l’image et création d’un projet associé

---

### 2. Prétraitement de l’image

Avant l’analyse, un prétraitement peut améliorer la qualité et les performances.

- Redimensionnement si l’image est trop grande (pour optimiser le traitement)
- Conversion dans un espace colorimétrique standard (RVB par exemple)
- Réduction éventuelle du bruit ou amélioration du contraste

Cette étape permet d’obtenir une image plus stable pour la détection des couleurs.

---

### 3. Analyse et regroupement des couleurs

L’étape suivante consiste à analyser les pixels de l’image afin d’identifier les couleurs dominantes.

- Lecture des pixels
- Regroupement des couleurs proches (via un clustering simple, par exemple k-means, ou une tolérance sur les valeurs RGB)
- Comptage du nombre de pixels par couleur

À ce stade, on obtient pour chaque couleur :

- Le nombre de pixels
- Le pourcentage de surface par rapport à l’image totale

---

### 4. Conversion en surface réelle

Pour que les résultats soient exploitables en production, il est nécessaire de convertir les pixels en surface réelle.

Deux cas sont possibles :

- Soit l’image contient une information de résolution (DPI)
- Soit l’utilisateur fournit une dimension réelle (ex : largeur en cm)

À partir de ces données, on peut :

- Convertir les pixels en cm²
- Appliquer une densité de broderie (points par cm²)
- Estimer le nombre total de points par couleur

---

### 5. Estimation des consommables et du temps

À partir du nombre de points calculé, il est possible d’effectuer des estimations métier.

- Calcul de la longueur de fil nécessaire (selon consommation par point)
- Estimation du temps de broderie (points par minute de la machine)
- Calcul éventuel d’un coût total (fil + temps machine)

Ces paramètres doivent rester configurables pour s’adapter à différents types de fil ou machines.

---

### 6. Restitution des résultats

Enfin, les résultats doivent être présentés de manière claire et compréhensible.

- Tableau récapitulatif par couleur
- Surface (pixels et cm²)
- Longueur de fil estimée
- Temps estimé
- Coût éventuel

Un export (PDF ou CSV) peut être envisagé pour un usage professionnel.

---

## Architecture fonctionnelle globale

On peut identifier les briques principales suivantes :

- Interface utilisateur (upload, paramétrage)
- Module de traitement d’image
- Module de calcul métier
- Base de données (projets, couleurs, configurations)
- Module de restitution (affichage, export)

Cette séparation permet de distinguer clairement la logique technique (analyse d’image) de la logique métier (estimation de fil et de coût).

---

# 2. Modèle de données

Pour structurer les informations, je propose les entités suivantes.

---

## Entité `ProjetBroderie`

Représente une commande ou un projet.

| Champ             | Type     | Rôle                   | Règles           |
| ------------------| -------- | ---------------------- | ---------------- |
| id                | int      | Identifiant unique     | Clé primaire     |
| nom               | string   | Nom du projet          | Requis, non vide |
| date_creation     | datetime | Date de création       | Requis           |
| Image_path        | string   | Chemin vers l’image    | Requis           |
| resolution        | float    | Résolution de l’image  | > 0 si renseigné |
| largeur_reelle_cm | float    | Largeur réelle fournie | > 0 si renseigné |
| densite_points    | float    | Points par cm²         | > 0              |

---

## Entité `Couleur`

Représente une couleur détectée dans l’image.

| Champ                | Type   | Rôle                   | Règles        |
| ---------------------| ------ | ---------------------- | ------------- |
| id                   | int    | Identifiant            | Clé primaire  |
| projet_id            | int    | Référence au projet    | Clé étrangère |
| code_col             | string | Code couleur (#RRGGBB) | Format valide |
| surface_pixels       | int    | Nombre de pixels       | ≥ 0           |
| surface_cm2          | float  | Surface réelle         | ≥ 0           |
| nombre_point         | int    | Points estimés         | ≥ 0           |
| longueur_fil_metres  | float  | Fil estimé             | ≥ 0           |
| temps_estime_minutes | float  | Temps estimé           | ≥ 0           |

---

## Relations

- Un `ProjetBroderie` possède plusieurs `Couleur` (relation one-to-many).
- Une `Couleur` appartient à un seul projet.

---

## Règles métier importantes

- La somme des surfaces en pixels des couleurs ne doit pas dépasser la surface totale de l’image.
- Les estimations (fil, temps) sont calculées automatiquement mais peuvent être ajustables.
- Les paramètres métier (densité, consommation par point) doivent être configurables.

---

# 3. Obstacles potentiels et risques

Plusieurs difficultés peuvent apparaître dans un tel système.

---

## 3.1. Qualité ou résolution des images

Images floues ou fortement compressées peuvent fausser la détection des couleurs.

**Pistes de résolution :**

- Recommander une résolution minimale
- Appliquer un prétraitement simple
- Informer l’utilisateur si l’image est jugée trop dégradée

---

## 3.2. Couleurs très proches ou dégradés

Les dégradés peuvent générer un grand nombre de teintes proches.

**Pistes de résolution :**

- Regrouper les couleurs avec une tolérance configurable
- Limiter le nombre maximal de couleurs principales
- Permettre une validation ou fusion manuelle après analyse

---

## 3.3. Performances sur images volumineuses

Le traitement pixel par pixel peut être coûteux.

**Pistes de résolution :**

- Redimensionnement avant analyse
- Utilisation de bibliothèques optimisées
- Traitement asynchrone avec indicateur de progression

---

## 3.4. Précision des estimations

La conversion pixels → surface réelle dépend d’informations parfois absentes.

**Pistes de résolution :**

- Demander explicitement une dimension réelle
- Utiliser une valeur par défaut avec avertissement
- Afficher le caractère estimatif des résultats

---
