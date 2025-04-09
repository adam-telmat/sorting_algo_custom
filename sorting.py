#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module d'algorithmes de tri avancés.
Chaque algorithme est optimisé pour allier performance et lisibilité.
"""

import time
from typing import List, Callable, Tuple, Any
import multiprocessing as mp
from functools import wraps

# Décorateur pour mesurer le temps d'exécution
def chronometre(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        debut = time.perf_counter()
        resultat = func(*args, **kwargs)
        fin = time.perf_counter()
        temps_execution = fin - debut
        return resultat, temps_execution
    return wrapper

# ========================= ALGORITHMES DE TRI =========================

@chronometre
def tri_selection(liste: List[float]) -> List[float]:
    """
    Tri par sélection - Complexité: O(n²)
    
    Principe quantique: à chaque itération, nous isolons 
    l'élément minimal et le transposons en position optimale.
    """
    n = len(liste)
    liste_copie = liste.copy()  # Préservation de l'immuabilité des données sources
    
    for i in range(n):
        # Recherche du minimum dans la sous-liste non triée
        idx_min = i
        for j in range(i + 1, n):
            if liste_copie[j] < liste_copie[idx_min]:
                idx_min = j
        
        # Permutation quantique (seulement si nécessaire)
        if idx_min != i:
            liste_copie[i], liste_copie[idx_min] = liste_copie[idx_min], liste_copie[i]
            
    return liste_copie

@chronometre
def tri_bulles(liste: List[float]) -> List[float]:
    """
    Tri à bulles - Complexité: O(n²)
    
    Métaphore cosmique: les éléments plus légers remontent à la surface 
    comme des bulles dans un fluide, itération après itération.
    """
    n = len(liste)
    liste_copie = liste.copy()
    
    # Optimisation: détection de liste déjà triée
    for i in range(n):
        echanges = False
        
        # Optimisation: réduction progressive de la plage de tri
        for j in range(0, n - i - 1):
            if liste_copie[j] > liste_copie[j + 1]:
                liste_copie[j], liste_copie[j + 1] = liste_copie[j + 1], liste_copie[j]
                echanges = True
                
        # Si aucun échange n'a eu lieu, la liste est triée
        if not echanges:
            break
            
    return liste_copie

@chronometre
def tri_insertion(liste: List[float]) -> List[float]:
    """
    Tri par insertion - Complexité: O(n²), mais optimal pour les petites listes ou presque triées
    
    Analogie bibliothécaire: comme Héron d'Alexandrie rangeant ses papyrus,
    nous insérons chaque élément à sa place exacte dans la séquence déjà ordonnée.
    """
    liste_copie = liste.copy()
    
    # Pour chaque élément à partir du deuxième
    for i in range(1, len(liste_copie)):
        element_courant = liste_copie[i]
        j = i - 1
        
        # Déplacement des éléments supérieurs
        while j >= 0 and liste_copie[j] > element_courant:
            liste_copie[j + 1] = liste_copie[j]
            j -= 1
            
        # Insertion de l'élément à sa position optimale
        liste_copie[j + 1] = element_courant
        
    return liste_copie

@chronometre
def tri_fusion(liste: List[float]) -> List[float]:
    """
    Tri fusion - Complexité: O(n log n)
    
    Principe de division cosmique: nous fragmentons l'univers des données
    en constellations plus petites, les ordonnons, puis les fusionnons harmonieusement.
    """
    # Fonction interne récursive
    def _fusion(gauche: List[float], droite: List[float]) -> List[float]:
        """Fusionne deux listes triées en une seule liste triée."""
        resultat = []
        i = j = 0
        
        # Fusion ordonnée des deux sous-listes
        while i < len(gauche) and j < len(droite):
            if gauche[i] <= droite[j]:
                resultat.append(gauche[i])
                i += 1
            else:
                resultat.append(droite[j])
                j += 1
                
        # Ajout des éléments restants (un seul des deux appends sera exécuté)
        resultat.extend(gauche[i:])
        resultat.extend(droite[j:])
        
        return resultat
    
    def _tri_fusion_recursif(sous_liste: List[float]) -> List[float]:
        """Implémentation récursive du tri fusion"""
        # Cas de base: liste vide ou singleton
        if len(sous_liste) <= 1:
            return sous_liste
            
        # Division en deux sous-listes
        milieu = len(sous_liste) // 2
        gauche = _tri_fusion_recursif(sous_liste[:milieu])
        droite = _tri_fusion_recursif(sous_liste[milieu:])
        
        # Fusion des deux sous-listes triées
        return _fusion(gauche, droite)
        
    return _tri_fusion_recursif(liste.copy())

@chronometre
def tri_rapide(liste: List[float]) -> List[float]:
    """
    Tri rapide (Quicksort) - Complexité: O(n log n) en moyenne, O(n²) dans le pire cas
    
    Paradigme du pivot cosmique: un élément singulier divise l'univers des données 
    en deux dimensions parallèles, chacune étant récursivement ordonnée.
    """
    liste_copie = liste.copy()
    
    def _tri_rapide_interne(debut: int, fin: int) -> None:
        if debut < fin:
            # Partition et récupération de l'indice pivot
            pivot_idx = _partition(debut, fin)
            
            # Tri récursif des sous-parties
            _tri_rapide_interne(debut, pivot_idx - 1)
            _tri_rapide_interne(pivot_idx + 1, fin)
    
    def _partition(debut: int, fin: int) -> int:
        # Stratégie de sélection du pivot avancée: médiane de 3
        milieu = (debut + fin) // 2
        
        # Ordonnance des trois candidats (début, milieu, fin)
        if liste_copie[milieu] < liste_copie[debut]:
            liste_copie[debut], liste_copie[milieu] = liste_copie[milieu], liste_copie[debut]
        if liste_copie[fin] < liste_copie[debut]:
            liste_copie[debut], liste_copie[fin] = liste_copie[fin], liste_copie[debut]
        if liste_copie[milieu] < liste_copie[fin]:
            liste_copie[milieu], liste_copie[fin] = liste_copie[fin], liste_copie[milieu]
            
        # Utilisation du pivot (maintenant à la position fin)
        pivot = liste_copie[fin]
        i = debut - 1
        
        for j in range(debut, fin):
            if liste_copie[j] <= pivot:
                i += 1
                liste_copie[i], liste_copie[j] = liste_copie[j], liste_copie[i]
                
        # Placement final du pivot
        liste_copie[i + 1], liste_copie[fin] = liste_copie[fin], liste_copie[i + 1]
        return i + 1
    
    # Lancement du tri récursif
    _tri_rapide_interne(0, len(liste_copie) - 1)
    return liste_copie

@chronometre
def tri_tas(liste: List[float]) -> List[float]:
    """
    Tri par tas (Heapsort) - Complexité: O(n log n)
    
    Architecture arborescente cosmique: nous construisons une structure 
    gravitationnelle où chaque nœud parent domine ses enfants,
    puis extrayons systématiquement la racine pour créer l'ordre.
    """
    liste_copie = liste.copy()
    n = len(liste_copie)
    
    def _tamiser(indice_racine: int, taille_tas: int) -> None:
        """Réorganise le sous-arbre enraciné à l'indice_racine."""
        plus_grand = indice_racine
        gauche = 2 * indice_racine + 1
        droite = 2 * indice_racine + 2
        
        # Vérification si le fils gauche existe et est plus grand que la racine
        if gauche < taille_tas and liste_copie[gauche] > liste_copie[plus_grand]:
            plus_grand = gauche
            
        # Vérification si le fils droit existe et est plus grand que la racine ou le fils gauche
        if droite < taille_tas and liste_copie[droite] > liste_copie[plus_grand]:
            plus_grand = droite
            
        # Si un fils est plus grand, échange et récursion
        if plus_grand != indice_racine:
            liste_copie[indice_racine], liste_copie[plus_grand] = liste_copie[plus_grand], liste_copie[indice_racine]
            _tamiser(plus_grand, taille_tas)
    
    # Construction du tas maximal (phase 1)
    for i in range(n // 2 - 1, -1, -1):
        _tamiser(i, n)
        
    # Extraction itérative de la racine (phase 2)
    for i in range(n - 1, 0, -1):
        # Échange de la racine avec le dernier élément
        liste_copie[0], liste_copie[i] = liste_copie[i], liste_copie[0]
        
        # Reconstruction du tas sans l'élément extrait
        _tamiser(0, i)
        
    return liste_copie

@chronometre
def tri_peigne(liste: List[float]) -> List[float]:
    """
    Tri à peigne (Combsort) - Complexité: O(n log n) en moyenne
    
    Évolution du tri à bulles, inspiré du métabolisme des galaxies:
    nous utilisons un facteur de réduction pour comparer des éléments 
    initialement éloignés, puis réduisons progressivement cet écart.
    """
    liste_copie = liste.copy()
    n = len(liste_copie)
    
    # Facteur de réduction optimal: 1.3
    facteur = 1.3
    ecart = n
    
    # Drapeau d'échange pour optimisation
    echange = True
    
    while ecart > 1 or echange:
        # Calcul de l'écart pour cette itération
        ecart = max(1, int(ecart / facteur))
        echange = False
        
        # Comparaison et échange des éléments séparés par l'écart
        for i in range(n - ecart):
            j = i + ecart
            if liste_copie[i] > liste_copie[j]:
                liste_copie[i], liste_copie[j] = liste_copie[j], liste_copie[i]
                echange = True
                
    return liste_copie

# ========================= PARALLÉLISATION =========================

def tri_parallele(liste: List[float], algo_tri: Callable, nb_processus: int = None) -> Tuple[List[float], float]:
    """
    Parallélise un algorithme de tri en divisant la liste et en fusionnant les résultats.
    
    Args:
        liste: Liste à trier
        algo_tri: Fonction de tri à paralléliser
        nb_processus: Nombre de processus (par défaut: nombre de cœurs disponibles)
        
    Returns:
        Tuple contenant la liste triée et le temps d'exécution
    """
    debut = time.perf_counter()
    
    if nb_processus is None:
        nb_processus = mp.cpu_count()
    
    n = len(liste)
    taille_segment = n // nb_processus
    
    # Division de la liste en segments
    segments = [liste[i:i + taille_segment] for i in range(0, n, taille_segment)]
    
    # Création d'un pool de processus
    with mp.Pool(processes=nb_processus) as pool:
        # Tri de chaque segment en parallèle
        segments_tries = pool.map(algo_tri, segments)
        
        # Extraction des listes triées (sans les temps)
        segments_tries = [seg[0] for seg in segments_tries]
    
    # Fusion des segments triés
    resultat = segments_tries[0]
    for segment in segments_tries[1:]:
        resultat = fusion_triee(resultat, segment)
    
    fin = time.perf_counter()
    temps_execution = fin - debut
    
    return resultat, temps_execution

def fusion_triee(liste1: List[float], liste2: List[float]) -> List[float]:
    """Fusionne deux listes déjà triées en une seule liste triée."""
    resultat = []
    i = j = 0
    
    # Fusion ordonnée
    while i < len(liste1) and j < len(liste2):
        if liste1[i] <= liste2[j]:
            resultat.append(liste1[i])
            i += 1
        else:
            resultat.append(liste2[j])
            j += 1
    
    # Ajout des éléments restants
    resultat.extend(liste1[i:])
    resultat.extend(liste2[j:])
    
    return resultat

# ========================= TESTS ET COMPARAISONS =========================

def comparer_algorithmes(liste: List[float], tailles_sous_listes: List[int] = None) -> dict:
    """
    Compare les performances des différents algorithmes de tri.
    
    Args:
        liste: Liste à trier pour les tests
        tailles_sous_listes: Liste des tailles à tester (sous-ensembles de la liste d'origine)
        
    Returns:
        Dictionnaire avec les performances de chaque algorithme
    """
    algorithmes = {
        "Sélection": tri_selection,
        "Bulles": tri_bulles,
        "Insertion": tri_insertion,
        "Fusion": tri_fusion,
        "Rapide": tri_rapide,
        "Tas": tri_tas,
        "Peigne": tri_peigne
    }
    
    resultats = {}
    
    # Si aucune taille spécifiée, utiliser la taille de la liste
    if tailles_sous_listes is None:
        tailles_sous_listes = [len(liste)]
    
    for taille in tailles_sous_listes:
        sous_liste = liste[:taille]
        resultats[taille] = {}
        
        for nom, algo in algorithmes.items():
            _, temps = algo(sous_liste)
            resultats[taille][nom] = temps
            
            # Version parallélisée pour les listes suffisamment grandes
            if taille > 1000:
                _, temps_parallele = tri_parallele(sous_liste, algo)
                resultats[taille][f"{nom} (parallèle)"] = temps_parallele
    
    return resultats

if __name__ == "__main__":
    # Code de test simple
    import random
    
    # Génération d'une liste aléatoire
    test_liste = [random.uniform(0, 1000) for _ in range(1000)]
    
    # Test basique de chaque algorithme
    for nom, algo in [
        ("Sélection", tri_selection),
        ("Bulles", tri_bulles),
        ("Insertion", tri_insertion),
        ("Fusion", tri_fusion),
        ("Rapide", tri_rapide),
        ("Tas", tri_tas),
        ("Peigne", tri_peigne)
    ]:
        liste_triee, temps = algo(test_liste)
        print(f"{nom}: {temps:.6f} secondes") 