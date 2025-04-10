# CosmiSort: Nébuleuse du Tri

![CosmiSort Logo](https://raw.githubusercontent.com/username/sorting-algorithms/main/logo.png) <!-- Vous pourrez ajouter une capture d'écran ou un logo plus tard -->

## 📝 Description

CosmiSort est un visualiseur futuriste d'algorithmes de tri qui transforme les données brutes en une expérience visuelle cosmique. Inspiré par l'idée d'aider Héron d'Alexandrie à organiser les papyrus du savoir humain, ce projet fusionne l'élégance algorithmique avec une interface graphique captivante.

## 🌌 Caractéristiques

- **7 algorithmes de tri** implémentés avec une précision mathématique:
  - Tri par sélection (O(n²))
  - Tri à bulles (O(n²))
  - Tri par insertion (O(n²))
  - Tri fusion (O(n log n))
  - Tri rapide (O(n log n))
  - Tri par tas (O(n log n))
  - Tri à peigne (O(n log n))

- **Visualisation hypnotique**
  - Particules énergétiques pour représenter les données
  - Traînées lumineuses lors des déplacements
  - Halos lumineux pour mettre en évidence les opérations
  - Champ d'étoiles pulsant en arrière-plan

- **Analyse des performances**
  - Mesure précise du temps d'exécution pour chaque algorithme
  - Comptage des étapes pour comparer l'efficacité algorithmique
  - Affichage en temps réel des statistiques

## 🚀 Installation

1. Clonez ce dépôt:
```bash
git clone https://github.com/username/sorting-algorithms.git
cd sorting-algorithms
```

2. Installez les dépendances:
```bash
pip install pygame
```

3. Lancez l'application:
```bash
python main.py
```

## 🎮 Utilisation

- Appuyez sur les touches **1-7** pour lancer les différents algorithmes de tri:
  - **1**: Tri par sélection
  - **2**: Tri à bulles
  - **3**: Tri par insertion
  - **4**: Tri fusion
  - **5**: Tri rapide
  - **6**: Tri par tas
  - **7**: Tri à peigne
- Appuyez sur **R** pour générer un nouveau jeu de données
- Appuyez sur **Échap** pour quitter

## 🧠 Architecture du code

### `sorting.py`
Contient les implémentations pures des 7 algorithmes de tri, ainsi que leurs versions "visuelles" qui sont des générateurs Python (utilisant `yield`) pour communiquer chaque étape du processus de tri.

### `main.py`
- Initialise l'environnement Pygame
- Gère les particules et leurs animations
- Interprète les états générés par les algorithmes et les transforme en représentations visuelles
- Mesure et affiche les performances

## 🔬 Choix d'implémentation remarquables

1. **Visualisation par générateurs**
   - L'utilisation de générateurs Python (`yield`) permet de suspendre l'exécution des algorithmes à chaque étape clé, offrant un contrôle précis sur l'animation sans modifier la logique fondamentale des algorithmes.

2. **Objets Particle avec micro-particules**
   - Chaque élément possède ses propres particules d'énergie orbitantes, créant une esthétique riche sans surcharger les performances.

3. **Traînées dynamiques**
   - La classe `Particle` maintient une liste de positions précédentes qui s'estompe progressivement, créant un effet de traînée lumineuse élégant lors des déplacements.

4. **Étoiles pulsantes**
   - L'arrière-plan n'est pas statique; chaque étoile pulse indépendamment, créant une ambiance cosmique vivante.

5. **Architecture de données par état**
   - Les algorithmes communiquent via des dictionnaires d'état riches (`{'data': [...], 'compare': [i,j], ...}`) qui permettent une interprétation flexible des opérations.

## 📊 Comparaison des performances

| Algorithme | Complexité | Forces | Faiblesses |
|------------|------------|--------|------------|
| Sélection | O(n²) | Simple, stable | Lent sur grandes listes |
| Bulles | O(n²) | Détecte les listes déjà triées | Très inefficace sur grandes listes |
| Insertion | O(n²) | Excellent sur petites listes ou presque triées | Ralentit avec la taille |
| Fusion | O(n log n) | Stable, diviser pour régner | Utilise plus de mémoire |
| Rapide | O(n log n) | Très rapide en pratique | Pire cas O(n²) si mal pivoté |
| Tas | O(n log n) | Garanti O(n log n), utilise structure de tas | Complexe, non-stable |
| Peigne | O(n log n) | Amélioration du tri à bulles | Moins connu, implémentations variables |

## 📜 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🧙‍♂️ Auteur

Créé par [Votre Nom] comme projet pour démontrer la beauté des algorithmes de tri.

---

*"Mettre de l'ordre dans le chaos n'a jamais été aussi beau."*