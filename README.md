# 🌌 COSMOS SORT - Visualisateur Quantique d'Algorithmes de Tri

## 🚀 Introduction

COSMOS SORT est un visualisateur d'algorithmes de tri révolutionnaire qui transforme la compréhension des algorithmes en une expérience visuelle immersive. Inspiré par Héron d'Alexandrie et sa quête pour organiser les connaissances humaines, ce projet fusionne l'informatique algorithmique avec une visualisation futuriste pour créer un outil éducatif et esthétique unique.

## ✨ Caractéristiques

### 🧪 Algorithmes Implémentés

COSMOS SORT implémente les 7 algorithmes de tri suivants, tous optimisés pour allier performance et élégance du code :

- **Tri par sélection** : O(n²) - Isole l'élément minimal et le place en position optimale
- **Tri à bulles** : O(n²) - Les éléments plus légers remontent comme des bulles
- **Tri par insertion** : O(n²) - Chaque élément est inséré à sa place exacte
- **Tri fusion** : O(n log n) - Divise, trie et fusionne les sous-ensembles
- **Tri rapide** : O(n log n) - Pivot qui divise en deux dimensions parallèles
- **Tri par tas** : O(n log n) - Construit une structure arborescente gravitationnelle
- **Tri à peigne** : O(n log n) - Compare des éléments éloignés avec écart réducteur

### 🎮 Interface Graphique Futuriste

L'interface graphique offre 5 modes de visualisation spectaculaires :

- **BARRES** : Représentation classique avec effets néon
- **CERCLE** : Vision radiale avec éléments rayonnant depuis le centre
- **COSMOS** : Univers où les valeurs deviennent des planètes en orbite
- **SPIRALE** : Spirale logarithmique avec traînées dynamiques
- **PARTICULES** : Système de particules énergétiques interconnectées

Chaque mode utilise des effets visuels avancés :
- Effets de lueur néon
- Dégradés de couleurs dynamiques basés sur les valeurs
- Traînées et sillages lumineux
- Particules d'ambiance en mouvement
- Animations fluides et réactives

### ⚡ Performances et Analyse

- **Mesure précise** du temps d'exécution de chaque algorithme
- **Mode comparaison** avec visualisation graphique des performances
- **Parallélisation** des algorithmes pour exploiter tous les cœurs du processeur
- **Analyse en temps réel** pendant l'exécution des algorithmes

## 🖥️ Utilisation

### Prérequis

```bash
# Installation des dépendances
pip install pygame numpy
```

### Lancement

```bash
python main.py
```

### Contrôles

- **ESPACE** : Démarrer/Pause le tri
- **R** : Régénérer une nouvelle liste
- **↑/↓** : Augmenter/Diminuer la taille de la liste
- **←/→** : Changer d'algorithme
- **M** : Changer de mode visualisation
- **P** : Activer/Désactiver le mode parallèle
- **C** : Comparer tous les algorithmes
- **A** : Basculer entre animation et tri réel
- **ESC** : Quitter

## 🔬 Architecture du Code

Le projet est structuré en deux fichiers principaux :

### `sorting.py`

Contient l'implémentation des 7 algorithmes de tri et des fonctions auxiliaires :
- Décorateur `chronometre` pour mesurer le temps d'exécution
- Fonction `tri_parallele` pour la parallélisation
- Fonction `comparer_algorithmes` pour l'analyse comparative

### `main.py`

Implémente l'interface graphique et l'animation :
- Classe `EtatTri` pour le suivi de l'état et l'animation
- Classe `VisualiseurtriQuantique` pour la visualisation et l'interaction
- 5 modes de visualisation différents avec effets visuels avancés
- Gestion des événements et boucle principale

## 🌟 Choix de Conception

### Visualisation

La conception visuelle s'inspire de concepts scientifiques et esthétiques :
- **Cosmologie** : Les valeurs sont représentées comme des corps célestes
- **Énergie Quantique** : Effets lumineux et particules pour symboliser l'activité algorithmique
- **Cybernétique** : Interface futuriste avec grille et néons

### Optimisation

- **Cache de rendu** pour améliorer les performances graphiques
- **Algorithmes optimisés** avec des améliorations spécifiques (médiane de 3 pour le pivot du tri rapide, etc.)
- **Parallélisation intelligente** qui divise les tâches selon le nombre de cœurs disponibles

### Modularité

- Séparation claire entre la logique algorithmique (`sorting.py`) et l'interface utilisateur (`main.py`)
- Architecture extensible permettant l'ajout facile de nouveaux algorithmes ou modes de visualisation

## 🔮 Extensions Possibles

- Ajout d'algorithmes de tri supplémentaires (tri par comptage, tri radix, etc.)
- Visualisation 3D complète avec OpenGL
- Exportation des animations en vidéo
- Mode éducatif avec explications pas à pas

## 🧠 Réflexions sur les Algorithmes

### Tri Fusion vs Tri Rapide

Le tri fusion garantit une complexité O(n log n) mais utilise plus de mémoire, tandis que le tri rapide est généralement plus rapide en pratique grâce à sa localité de cache supérieure, malgré son pire cas O(n²).

### Parallélisation

La parallélisation apporte des gains significatifs principalement pour les listes de grande taille et les algorithmes divisibles (comme le tri fusion). Le tri par sélection, en revanche, est intrinsèquement séquentiel et bénéficie moins de la parallélisation.

---

*COSMOS SORT - Où l'algorithmique devient art et science*
 
