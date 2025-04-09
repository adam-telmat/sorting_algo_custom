#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
VISUALISATEUR COSMIQUE D'ALGORITHMES DE TRI
-------------------------------------------
Une interface futuriste pour visualiser les algorithmes de tri
comme jamais auparavant.
"""

import sys
import random
import time
import multiprocessing as mp
from typing import List, Tuple, Dict, Any, Callable
import numpy as np
import pygame
from pygame import gfxdraw
import pygame.freetype
from pygame.locals import *
import colorsys
import math
from dataclasses import dataclass
from collections import deque

# Import des algorithmes de tri
from sorting import (
    tri_selection, tri_bulles, tri_insertion,
    tri_fusion, tri_rapide, tri_tas, tri_peigne,
    tri_parallele, comparer_algorithmes
)

# Constantes globales
LARGEUR, HAUTEUR = 1600, 900
FPS = 60

# Palette de couleurs futuriste
COULEURS = {
    "fond": (10, 10, 20),
    "fond_alt": (15, 15, 30),
    "texte": (220, 220, 255),
    "grille": (30, 30, 50),
    "accent1": (0, 200, 255),    # Bleu néon
    "accent2": (255, 0, 128),    # Rose néon
    "accent3": (128, 255, 0),    # Vert néon
    "accent4": (255, 128, 0),    # Orange néon
    "accent5": (180, 0, 255),    # Violet néon
    "selection": (255, 255, 0),  # Jaune
    "complete": (0, 255, 100),   # Vert succès
}

# Mapping des algorithmes
ALGORITHMES = {
    "Selection": {
        "fonction": tri_selection,
        "couleur": COULEURS["accent1"],
        "description": "O(n²) - Isole l'élément minimal et le place en position optimale"
    },
    "Bulles": {
        "fonction": tri_bulles,
        "couleur": COULEURS["accent2"],
        "description": "O(n²) - Les éléments plus légers remontent comme des bulles"
    },
    "Insertion": {
        "fonction": tri_insertion,
        "couleur": COULEURS["accent3"],
        "description": "O(n²) - Chaque élément est inséré à sa place exacte"
    },
    "Fusion": {
        "fonction": tri_fusion,
        "couleur": COULEURS["accent4"],
        "description": "O(n log n) - Divise, trie et fusionne les sous-ensembles"
    },
    "Rapide": {
        "fonction": tri_rapide,
        "couleur": COULEURS["accent5"],
        "description": "O(n log n) - Pivot qui divise en deux dimensions parallèles"
    },
    "Tas": {
        "fonction": tri_tas,
        "couleur": COULEURS["accent1"],
        "description": "O(n log n) - Construit une structure arborescente gravitationnelle"
    },
    "Peigne": {
        "fonction": tri_peigne,
        "couleur": COULEURS["accent2"],
        "description": "O(n log n) - Compare des éléments éloignés avec écart réducteur"
    }
}

@dataclass
class EtatTri:
    """Classe pour suivre l'état du tri et l'animation"""
    liste: List[float]
    indices_actifs: List[int] = None
    etape: int = 0
    termine: bool = False
    temps_debut: float = 0
    temps_fin: float = 0
    traces: deque = None
    
    def __post_init__(self):
        if self.indices_actifs is None:
            self.indices_actifs = []
        if self.traces is None:
            self.traces = deque(maxlen=50)  # Limiter le nombre de traces
    
    def marquer_actif(self, *indices):
        """Marque les indices comme actifs pour l'animation"""
        self.indices_actifs = list(indices)
        # Ajouter une trace lumineuse aux positions actives
        for idx in indices:
            if 0 <= idx < len(self.liste):
                x_rel = idx / (len(self.liste) - 1)
                self.traces.append((x_rel, self.liste[idx] / max(self.liste), time.time()))
    
    def reinitialiser(self, nouvelle_liste=None):
        """Réinitialise l'état du tri"""
        if nouvelle_liste is not None:
            self.liste = nouvelle_liste
        self.indices_actifs = []
        self.etape = 0
        self.termine = False
        self.temps_debut = 0
        self.temps_fin = 0
        self.traces.clear()

class VisualiseurtriQuantique:
    """Interface graphique futuriste pour visualiser les algorithmes de tri"""
    
    def __init__(self):
        """Initialisation de l'environnement graphique"""
        pygame.init()
        pygame.display.set_caption("COSMOS SORT - Visualisateur Quantique d'Algorithmes")
        
        # Configuration de l'écran
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR), RESIZABLE)
        self.horloge = pygame.time.Clock()
        
        # Chargement des polices
        pygame.freetype.init()
        self.police_titre = pygame.freetype.SysFont("Arial", 36)
        self.police = pygame.freetype.SysFont("Arial", 20)
        self.police_petite = pygame.freetype.SysFont("Arial", 16)
        
        # État de l'application
        self.taille_liste = 100
        self.liste_originale = self._generer_liste()
        self.etat = EtatTri(self.liste_originale.copy())
        
        # Paramètres de visualisation
        self.mode_visualisation = "COSMOS"  # Modes: BARRES, CERCLE, COSMOS, SPIRALE, PARTICULES
        self.algo_actif = "Selection"
        self.animation_speed = 1  # Contrôle de la vitesse d'animation
        self.parallele = False
        
        # Résultats de comparaison
        self.resultats_comparaison = {}
        
        # Paramètres d'animation
        self.particules = []
        self.temps_global = 0
        self.rotation_angle = 0
        
        # État du système
        self.en_cours = False
        self.en_pause = False
        self.animation_seulement = False
        self.comparison_mode = False
        
        # Buffers pour le rendu optimisé
        self.particule_img = self._creer_particule_image()
        
        # Crée un cache pour les surfaces de rendu des visualisations
        self.surface_cache = {}
    
    def _generer_liste(self) -> List[float]:
        """Génère une liste aléatoire de nombres"""
        return [random.uniform(0.1, 1.0) for _ in range(self.taille_liste)]
    
    def _creer_particule_image(self) -> pygame.Surface:
        """Crée une image de particule avec éclat pour le mode particules"""
        taille = 24
        surface = pygame.Surface((taille, taille), pygame.SRCALPHA)
        rayon = taille // 2
        
        # Créer un dégradé radial pour l'éclat
        for r in range(rayon, 0, -1):
            alpha = int(255 * (r / rayon) ** 0.5)
            pygame.gfxdraw.filled_circle(surface, rayon, rayon, r, (*COULEURS["accent1"][:3], 255 - alpha))
        
        # Point central plus brillant
        pygame.gfxdraw.filled_circle(surface, rayon, rayon, 2, COULEURS["texte"])
        
        return surface 

    def _valeur_to_couleur(self, valeur: float, max_val: float, saturation: float = 1.0) -> Tuple[int, int, int]:
        """Convertit une valeur en couleur selon un gradient spectral néon"""
        # Utilise la teinte basée sur la valeur (0.0 = rouge, 0.33 = vert, 0.66 = bleu, 1.0 = rouge)
        h = valeur / max_val
        # Ajouter décalage pour éviter les teintes rouges aux deux extrémités
        h = (h * 0.8 + 0.1) % 1.0
        
        # HSV -> RGB avec saturation et luminosité maximales pour effet néon
        r, g, b = colorsys.hsv_to_rgb(h, saturation, 1.0)
        return int(r * 255), int(g * 255), int(b * 255)
    
    def _dessiner_grille_futuriste(self, surface: pygame.Surface):
        """Dessine une grille futuriste en arrière-plan"""
        largeur, hauteur = surface.get_size()
        
        # Lignes horizontales avec effet de profondeur
        espacement_h = hauteur // 10
        for y in range(0, hauteur, espacement_h):
            alpha = 100 - int(80 * (y / hauteur))  # Fade out avec la distance
            pygame.draw.line(surface, (*COULEURS["grille"], alpha), (0, y), (largeur, y), 1)
        
        # Lignes verticales avec effet de profondeur
        espacement_v = largeur // 20
        for x in range(0, largeur, espacement_v):
            alpha = 100 - int(80 * (abs(x - largeur/2) / (largeur/2)))  # Plus lumineux au centre
            pygame.draw.line(surface, (*COULEURS["grille"], alpha), (x, 0), (x, hauteur), 1)
    
    def _dessiner_particules_background(self, surface: pygame.Surface):
        """Dessine des particules en mouvement dans le fond"""
        temps = self.temps_global * 0.1
        
        # Créer de nouvelles particules aléatoirement
        if random.random() < 0.1:
            x = random.randint(0, LARGEUR)
            y = random.randint(0, HAUTEUR)
            taille = random.uniform(1.0, 3.0)
            vitesse = random.uniform(0.3, 1.5)
            couleur = self._valeur_to_couleur(random.random(), 1.0, 0.7)
            self.particules.append([x, y, taille, vitesse, couleur, random.uniform(0, 2*math.pi)])
        
        # Mettre à jour et dessiner les particules
        particules_a_supprimer = []
        for i, (x, y, taille, vitesse, couleur, angle) in enumerate(self.particules):
            # Mouvement sinusoïdal
            x += math.cos(angle) * vitesse
            y += math.sin(angle) * vitesse
            
            # Sortie de l'écran ?
            if x < 0 or x > LARGEUR or y < 0 or y > HAUTEUR:
                particules_a_supprimer.append(i)
                continue
            
            # Dessiner particule avec éclat
            alpha = int(128 + 127 * math.sin(temps * 2 + i))
            rayon = int(taille * (1 + 0.2 * math.sin(temps * 3 + i * 0.7)))
            pygame.gfxdraw.filled_circle(surface, int(x), int(y), rayon, (*couleur, alpha))
            
            # Mettre à jour particule
            self.particules[i] = [x, y, taille, vitesse, couleur, angle]
        
        # Supprimer les particules hors écran
        for i in sorted(particules_a_supprimer, reverse=True):
            if i < len(self.particules):
                del self.particules[i]
    
    def _visualiser_barres(self, surface: pygame.Surface, liste: List[float], indices_actifs: List[int], termine: bool):
        """Visualisation traditionnelle en barres avec effet de néon"""
        largeur, hauteur = surface.get_size()
        max_val = max(liste)
        nb_elements = len(liste)
        largeur_element = largeur / nb_elements
        
        # Espace de tri (zone principale)
        zone_tri = pygame.Rect(0, 0, largeur, hauteur)
        
        # Dessiner chaque élément
        for i, valeur in enumerate(liste):
            # Calcul des dimensions
            x = i * largeur_element
            hauteur_barre = int((valeur / max_val) * hauteur * 0.8)
            y = hauteur - hauteur_barre
            
            # Déterminer la couleur selon l'état
            if termine:
                couleur = COULEURS["complete"]
            elif i in indices_actifs:
                couleur = COULEURS["selection"]
            else:
                couleur = self._valeur_to_couleur(valeur, max_val)
            
            # Dessiner barre avec éclat néon
            rect = pygame.Rect(x, y, max(1, largeur_element - 1), hauteur_barre)
            
            # Effet de lueur (éclat néon)
            rayon_eclat = max(1, int(largeur_element * 0.7))
            for r in range(rayon_eclat, 0, -1):
                alpha = int(50 * (r / rayon_eclat))
                pygame.gfxdraw.box(surface, rect.inflate(r, 0), (*couleur, alpha))
            
            # Barre principale
            pygame.draw.rect(surface, couleur, rect)
    
    def _visualiser_cercle(self, surface: pygame.Surface, liste: List[float], indices_actifs: List[int], termine: bool):
        """Visualisation en cercle avec éléments rayonnants depuis le centre"""
        largeur, hauteur = surface.get_size()
        max_val = max(liste)
        nb_elements = len(liste)
        
        # Centre du cercle
        centre_x, centre_y = largeur // 2, hauteur // 2
        rayon_max = min(largeur, hauteur) * 0.45
        
        # Épaisseur des segments
        angle_segment = 2 * math.pi / nb_elements
        epaisseur_segment = 2 * math.pi * rayon_max / nb_elements * 0.8
        
        # Dessiner chaque élément comme un segment de cercle
        for i, valeur in enumerate(liste):
            # Angle de l'élément
            angle = i * angle_segment
            
            # Rayon basé sur la valeur
            rayon = rayon_max * (0.2 + 0.8 * valeur / max_val)
            
            # Calculer les coordonnées
            x = centre_x + math.cos(angle) * rayon
            y = centre_y + math.sin(angle) * rayon
            
            # Déterminer la couleur
            if termine:
                couleur = COULEURS["complete"]
            elif i in indices_actifs:
                couleur = COULEURS["selection"]
            else:
                couleur = self._valeur_to_couleur(valeur, max_val)
            
            # Ligne du centre vers la position
            pygame.draw.line(surface, couleur, (centre_x, centre_y), (x, y), 2)
            
            # Point à la position de l'élément
            for r in range(5, 0, -1):
                alpha = 250 - r * 40
                pygame.gfxdraw.filled_circle(
                    surface, int(x), int(y), r, (*couleur, max(0, alpha))
                )
    
    def _visualiser_cosmos(self, surface: pygame.Surface, liste: List[float], indices_actifs: List[int], termine: bool):
        """Visualisation cosmique avec orbites et planètes"""
        largeur, hauteur = surface.get_size()
        max_val = max(liste)
        nb_elements = len(liste)
        
        # Centre du cosmos
        centre_x, centre_y = largeur // 2, hauteur // 2
        
        # Rayon de base pour les orbites
        rayon_base = min(largeur, hauteur) * 0.4
        
        # Angle de rotation global (animation)
        angle_global = self.rotation_angle
        
        # Dessiner orbites
        for i in range(5):
            rayon_orbite = rayon_base * (0.3 + i * 0.15)
            alpha = 100 - i * 15
            pygame.gfxdraw.aacircle(
                surface, centre_x, centre_y, int(rayon_orbite), 
                (*COULEURS["grille"], alpha)
            )
        
        # Dessiner chaque élément comme une planète en orbite
        for i, valeur in enumerate(liste):
            # Angle de position sur le cosmos, influencé par la valeur
            # Les valeurs plus élevées sont placées sur des orbites extérieures
            orbite_relative = valeur / max_val
            rayon_orbite = rayon_base * (0.3 + orbite_relative * 0.7)
            
            # Vitesse angulaire inversement proportionnelle au rayon
            vitesse_angulaire = 1.0 - orbite_relative * 0.7
            
            # Position angulaire
            angle = angle_global * vitesse_angulaire + (i * 2 * math.pi / nb_elements)
            
            # Calculer les coordonnées
            x = centre_x + math.cos(angle) * rayon_orbite
            y = centre_y + math.sin(angle) * rayon_orbite
            
            # Taille basée sur la valeur
            taille = 4 + valeur / max_val * 15
            
            # Déterminer la couleur
            if termine:
                couleur = COULEURS["complete"]
            elif i in indices_actifs:
                couleur = COULEURS["selection"]
                taille *= 1.5  # Les éléments sélectionnés sont plus grands
            else:
                couleur = self._valeur_to_couleur(valeur, max_val)
            
            # Effet de lueur (aura planétaire)
            for r in range(int(taille * 2), 0, -2):
                alpha = int(150 * (r / (taille * 2))) if r > taille else 255
                pygame.gfxdraw.filled_circle(
                    surface, int(x), int(y), r, (*couleur, min(alpha, 60))
                )
            
            # Planète
            pygame.gfxdraw.filled_circle(surface, int(x), int(y), int(taille), couleur)
            pygame.gfxdraw.aacircle(surface, int(x), int(y), int(taille), (255, 255, 255, 180))
            
            # Petit éclat lumineux
            eclat_x = x + taille * 0.5 * math.cos(angle - 0.7)
            eclat_y = y + taille * 0.5 * math.sin(angle - 0.7)
            pygame.gfxdraw.filled_circle(
                surface, int(eclat_x), int(eclat_y), max(1, int(taille/5)), (255, 255, 255, 200)
            )
            
            # Tracer l'orbite si élément actif avec effet de sillage
            if i in indices_actifs:
                points = []
                for j in range(20):
                    segment_angle = angle - j * 0.1
                    segment_x = centre_x + math.cos(segment_angle) * rayon_orbite
                    segment_y = centre_y + math.sin(segment_angle) * rayon_orbite
                    points.append((segment_x, segment_y))
                
                if len(points) >= 2:
                    # Effet de dégradé sur le sillage
                    for j in range(len(points) - 1):
                        alpha = 180 - j * (160 / len(points))
                        pygame.draw.line(
                            surface, (*couleur, alpha),
                            (points[j][0], points[j][1]),
                            (points[j+1][0], points[j+1][1]),
                            2
                        )
    
    def _visualiser_spirale(self, surface: pygame.Surface, liste: List[float], indices_actifs: List[int], termine: bool):
        """Visualisation en spirale logarithmique avec traînées dynamiques"""
        largeur, hauteur = surface.get_size()
        max_val = max(liste)
        nb_elements = len(liste)
        
        # Centre de la spirale
        centre_x, centre_y = largeur // 2, hauteur // 2
        
        # Paramètres de la spirale
        rayon_max = min(largeur, hauteur) * 0.45
        coef_spiral = 0.2
        angle_base = self.rotation_angle * 0.5
        
        # Dessiner chaque élément sur la spirale
        for i, valeur in enumerate(liste):
            # Position normalisée dans la liste (de 0 à 1)
            pos_norm = i / nb_elements
            
            # Créer un effet de spirale avec la position normalisée
            angle = angle_base + pos_norm * 15
            
            # Rayon qui augmente avec l'angle (formule de spirale logarithmique)
            rayon = rayon_max * pos_norm * (0.1 + 0.9 * valeur / max_val)
            
            # Calculer les coordonnées
            x = centre_x + math.cos(angle) * rayon
            y = centre_y + math.sin(angle) * rayon
            
            # Taille basée sur la valeur et la position
            taille = 3 + 12 * valeur / max_val
            
            # Déterminer la couleur
            if termine:
                couleur = COULEURS["complete"]
            elif i in indices_actifs:
                couleur = COULEURS["selection"]
                taille *= 1.3
            else:
                # Couleur basée sur la valeur et la position dans la spirale
                couleur = self._valeur_to_couleur(
                    (valeur / max_val + pos_norm) / 2, 
                    1.0
                )
            
            # Dessiner effet de traînée
            points_trainee = []
            for j in range(10):
                angle_trainee = angle - j * 0.1
                r_trainee = rayon * math.exp(-coef_spiral * j * 0.1)
                tx = centre_x + math.cos(angle_trainee) * r_trainee
                ty = centre_y + math.sin(angle_trainee) * r_trainee
                points_trainee.append((tx, ty))
            
            # Dessiner la traînée avec un dégradé d'alpha
            if len(points_trainee) >= 2:
                for j in range(len(points_trainee) - 1):
                    alpha = 150 - j * 15
                    pygame.draw.line(
                        surface, 
                        (*couleur, alpha), 
                        points_trainee[j], 
                        points_trainee[j+1], 
                        max(1, int(taille * 0.7 * (1 - j/10)))
                    )
            
            # Dessiner l'élément principal
            pygame.gfxdraw.filled_circle(
                surface, int(x), int(y), int(taille), (*couleur, 230)
            )
            pygame.gfxdraw.aacircle(
                surface, int(x), int(y), int(taille), (255, 255, 255, 150)
            )
    
    def _visualiser_particules(self, surface: pygame.Surface, liste: List[float], indices_actifs: List[int], termine: bool):
        """Visualisation avec système de particules dynamiques"""
        largeur, hauteur = surface.get_size()
        max_val = max(liste)
        nb_elements = len(liste)
        
        # Zone de rendu des particules
        zone_particules = pygame.Rect(50, 50, largeur - 100, hauteur - 100)
        
        # Facteur temps pour les animations
        temps = self.temps_global * 0.5
        
        # Dessiner chaque élément comme un système de particules
        for i, valeur in enumerate(liste):
            # Position normalisée (de 0 à 1) dans la liste
            pos_norm_x = i / nb_elements
            
            # Position Y basée sur la valeur normalisée
            pos_norm_y = 1.0 - (valeur / max_val)
            
            # Convertir en coordonnées d'écran
            x = zone_particules.left + pos_norm_x * zone_particules.width
            y = zone_particules.top + pos_norm_y * zone_particules.height
            
            # Déterminer la couleur
            if termine:
                couleur = COULEURS["complete"]
            elif i in indices_actifs:
                couleur = COULEURS["selection"]
            else:
                couleur = self._valeur_to_couleur(valeur, max_val)
            
            # Taille et énergie basées sur la valeur
            taille = 4 + 10 * (valeur / max_val)
            energie = 0.5 + 0.5 * (valeur / max_val)
            
            # Animation de pulsation
            pulsation = 1.0 + 0.2 * math.sin(temps * 5 + i * 0.1)
            taille_animee = taille * pulsation
            
            # Dessiner système de particules
            
            # 1. Cercle central lumineux
            pygame.gfxdraw.filled_circle(
                surface, int(x), int(y), int(taille_animee), 
                (*couleur, 230)
            )
            
            # 2. Aura énergétique
            for r in range(int(taille_animee * 3), 0, -3):
                alpha = int(100 * (r / (taille_animee * 3)))
                pygame.gfxdraw.filled_circle(
                    surface, int(x), int(y), r, 
                    (*couleur, min(60, alpha))
                )
            
            # 3. Particules orbitales (pour les éléments actifs ou terminés)
            if i in indices_actifs or termine:
                nb_particules = 5
                for p in range(nb_particules):
                    angle = temps * 3 + (p * 2 * math.pi / nb_particules)
                    rayon_orbite = taille_animee * 2.5
                    px = x + math.cos(angle) * rayon_orbite
                    py = y + math.sin(angle) * rayon_orbite
                    
                    # Taille de la particule orbitale
                    p_taille = max(1, taille_animee / 3)
                    
                    # Dessiner la particule avec flou
                    for r in range(int(p_taille * 2), 0, -1):
                        alpha = 200 if r <= p_taille else int(100 * (1 - (r - p_taille) / p_taille))
                        pygame.gfxdraw.filled_circle(
                            surface, int(px), int(py), r, (*couleur, alpha)
                        )
            
            # Lignes de connexion entre éléments adjacents
            if i < nb_elements - 1:
                next_pos_x = zone_particules.left + ((i + 1) / nb_elements) * zone_particules.width
                next_pos_y = zone_particules.top + (1.0 - (liste[i+1] / max_val)) * zone_particules.height
                
                # Calculer la distance pour ajuster l'intensité de la connexion
                dist = math.sqrt((next_pos_x - x)**2 + (next_pos_y - y)**2)
                max_dist = largeur * 0.15
                
                if dist < max_dist:
                    # Intensité de la connexion inversement proportionnelle à la distance
                    intensite = 1.0 - (dist / max_dist)
                    alpha = int(150 * intensite)
                    
                    # Couleur moyenne entre les deux éléments
                    couleur_next = self._valeur_to_couleur(liste[i+1], max_val)
                    couleur_ligne = (
                        int((couleur[0] + couleur_next[0])/2),
                        int((couleur[1] + couleur_next[1])/2),
                        int((couleur[2] + couleur_next[2])/2)
                    )
                    
                    # Dessiner ligne avec effet d'énergie
                    for w in range(3, 0, -1):
                        a = alpha * (w / 3)
                        pygame.draw.line(
                            surface, (*couleur_ligne, a),
                            (x, y), (next_pos_x, next_pos_y), w
                        ) 

    def _dessiner_interface(self, surface: pygame.Surface):
        """Dessine l'interface utilisateur futuriste"""
        largeur, hauteur = surface.get_size()
        
        # Zone d'informations en haut
        zone_info = pygame.Rect(0, 0, largeur, 60)
        pygame.draw.rect(surface, (*COULEURS["fond_alt"], 180), zone_info)
        
        # Titre
        self.police_titre.render_to(
            surface, (20, 15), "COSMOS SORT - Tri Quantique", COULEURS["texte"]
        )
        
        # Informations sur l'algorithme actif
        algo_info = f"Algorithme: {self.algo_actif} | {ALGORITHMES[self.algo_actif]['description']}"
        self.police.render_to(
            surface, (largeur // 3, 20), algo_info, COULEURS["texte"]
        )
        
        # Informations sur la taille de la liste et le mode
        mode_info = f"Mode: {self.mode_visualisation} | Taille: {self.taille_liste} | {'PARALLÈLE' if self.parallele else 'SÉQUENTIEL'}"
        self.police.render_to(
            surface, (largeur - 450, 20), mode_info, COULEURS["texte"]
        )
        
        # Barre de progression et temps pour tri en cours
        if self.en_cours:
            # Zone de progression
            zone_progression = pygame.Rect(20, hauteur - 40, largeur - 40, 20)
            pygame.draw.rect(surface, COULEURS["grille"], zone_progression, 1)
            
            # Barre de progression
            progression = min(1.0, self.etat.etape / len(self.etat.liste)) if self.etat.liste else 0
            if progression > 0:
                barre = pygame.Rect(
                    zone_progression.left, zone_progression.top,
                    int(zone_progression.width * progression), zone_progression.height
                )
                pygame.draw.rect(surface, ALGORITHMES[self.algo_actif]["couleur"], barre)
            
            # Temps écoulé
            if self.etat.temps_debut > 0:
                if self.etat.termine:
                    temps_total = self.etat.temps_fin - self.etat.temps_debut
                    temps_texte = f"Terminé en {temps_total:.6f} secondes"
                else:
                    temps_actuel = time.time() - self.etat.temps_debut
                    temps_texte = f"Temps: {temps_actuel:.3f}s"
                    
                self.police.render_to(
                    surface, (largeur // 2 - 100, hauteur - 35), temps_texte, COULEURS["texte"]
                )
        
        # Instructions si pas de tri en cours
        else:
            instructions = [
                "ESPACE: Démarrer/Pause",
                "R: Régénérer liste",
                "↑/↓: Taille liste",
                "←/→: Changer algorithme",
                "M: Changer mode visualisation",
                "P: Mode parallèle",
                "C: Comparer tous",
                "ESC: Quitter"
            ]
            
            y_offset = hauteur - 40 * len(instructions)
            for i, texte in enumerate(instructions):
                self.police_petite.render_to(
                    surface, (20, y_offset + i * 30), texte, COULEURS["texte"]
                )
        
        # Si comparaison active, afficher graphique comparatif
        if self.comparison_mode and self.resultats_comparaison:
            self._dessiner_graphique_comparaison(surface)
    
    def _dessiner_graphique_comparaison(self, surface: pygame.Surface):
        """Dessine un graphique de comparaison des performances"""
        largeur, hauteur = surface.get_size()
        
        # Dimensions du graphique
        marge = 80
        graph_rect = pygame.Rect(
            marge, 100, 
            largeur - marge * 2, 
            hauteur - 220
        )
        
        # Fond du graphique
        pygame.draw.rect(surface, (*COULEURS["fond_alt"], 150), graph_rect)
        pygame.draw.rect(surface, COULEURS["grille"], graph_rect, 1)
        
        # Titre
        self.police_titre.render_to(
            surface, (largeur // 2 - 150, 70), 
            "Comparaison des Algorithmes", 
            COULEURS["texte"]
        )
        
        # Données pour le graphe (utilise la première taille disponible)
        taille = list(self.resultats_comparaison.keys())[0]
        resultats = self.resultats_comparaison[taille]
        
        # Trouver la valeur max pour normaliser
        max_temps = max(resultats.values()) * 1.1  # Marge de 10%
        
        # Dessiner les barres pour chaque algorithme
        nb_algos = len(resultats)
        largeur_barre = (graph_rect.width - 40) / nb_algos
        
        for i, (algo, temps) in enumerate(resultats.items()):
            # Calculer dimensions de la barre
            hauteur_barre = (temps / max_temps) * graph_rect.height
            x = graph_rect.left + 20 + i * largeur_barre
            y = graph_rect.bottom - hauteur_barre
            
            # Couleur de la barre
            if "parallèle" in algo.lower():
                couleur = COULEURS["accent3"]
            else:
                algo_name = algo.split(" ")[0]  # Récupérer le nom sans "(parallèle)"
                couleur = ALGORITHMES.get(algo_name, {}).get("couleur", COULEURS["accent1"])
            
            # Dessiner barre avec effet néon
            rect = pygame.Rect(
                x, y, 
                largeur_barre - 10, 
                hauteur_barre
            )
            
            # Effet de lueur (glow)
            for r in range(5, 0, -1):
                alpha = 50 - r * 8
                glow_rect = rect.inflate(r*2, 0)
                pygame.draw.rect(surface, (*couleur, alpha), glow_rect)
            
            # Barre principale
            pygame.draw.rect(surface, couleur, rect)
            
            # Texte avec nom d'algorithme (rotation pour économiser l'espace)
            nom_surface = self.police_petite.render(
                algo, COULEURS["texte"]
            )[0]
            
            # Rotation et positionnement du texte
            nom_surface = pygame.transform.rotate(nom_surface, -45)
            surface.blit(
                nom_surface, 
                (x + largeur_barre//2 - 10, graph_rect.bottom + 10)
            )
            
            # Afficher temps
            temps_texte = f"{temps:.6f}s"
            self.police_petite.render_to(
                surface, 
                (x + largeur_barre//2 - 20, y - 20), 
                temps_texte, 
                COULEURS["texte"]
            )
    
    def _visualiser_donnees(self):
        """Visualise les données selon le mode actif"""
        largeur, hauteur = LARGEUR, HAUTEUR
        
        # Créer ou récupérer la surface de rendu depuis le cache
        cache_key = f"{self.mode_visualisation}_{id(self.etat.liste)}_{self.etat.etape}"
        if cache_key in self.surface_cache:
            return self.surface_cache[cache_key]
        
        # Créer une nouvelle surface de rendu
        surface = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))  # Transparent
        
        # Dessiner la grille futuriste en arrière-plan
        self._dessiner_grille_futuriste(surface)
        
        # Dessiner des particules d'ambiance
        self._dessiner_particules_background(surface)
        
        # Récupérer les données
        liste = self.etat.liste
        indices_actifs = self.etat.indices_actifs
        termine = self.etat.termine
        
        # Sélectionner le mode de visualisation
        if self.mode_visualisation == "BARRES":
            self._visualiser_barres(surface, liste, indices_actifs, termine)
        elif self.mode_visualisation == "CERCLE":
            self._visualiser_cercle(surface, liste, indices_actifs, termine)
        elif self.mode_visualisation == "COSMOS":
            self._visualiser_cosmos(surface, liste, indices_actifs, termine)
        elif self.mode_visualisation == "SPIRALE":
            self._visualiser_spirale(surface, liste, indices_actifs, termine)
        elif self.mode_visualisation == "PARTICULES":
            self._visualiser_particules(surface, liste, indices_actifs, termine)
        
        # Dessiner les traces des éléments actifs
        for x_rel, y_rel, t in self.etat.traces:
            age = time.time() - t
            if age < 1.0:  # Disparition après 1 seconde
                alpha = int(200 * (1.0 - age))
                x = int(x_rel * largeur)
                y = int(y_rel * hauteur)
                taille = int(5 * (1.0 - age))
                pygame.gfxdraw.filled_circle(
                    surface, x, y, taille, 
                    (*COULEURS["selection"], alpha)
                )
        
        # Mettre en cache la surface rendue
        self.surface_cache[cache_key] = surface
        return surface
    
    def _executer_tri(self):
        """Exécute l'algorithme de tri sélectionné"""
        # Si le tri est terminé ou non démarré, initialiser
        if not self.en_cours or self.etat.termine:
            # Réinitialiser l'état
            self.etat.reinitialiser(self.liste_originale.copy())
            self.en_cours = True
            self.etat.temps_debut = time.time()
            self.surface_cache.clear()
        
        # Si en pause, ne pas avancer
        if self.en_pause:
            return
        
        # Si mode animation uniquement, simuler les étapes
        if self.animation_seulement:
            # Animation factice pour le mode démonstration
            n = len(self.etat.liste)
            
            # Simuler différents motifs selon l'algorithme
            if self.algo_actif == "Selection":
                min_idx = self.etat.etape
                if min_idx < n:
                    # Chercher le minimum dans les éléments non triés
                    j = min_idx + (self.etat.etape % 10)
                    if j >= n:
                        j = n - 1
                    self.etat.marquer_actif(min_idx, j)
                    
                    # Occasionnellement, échanger des éléments
                    if random.random() < 0.05:
                        idx1, idx2 = random.sample(range(n), 2)
                        self.etat.liste[idx1], self.etat.liste[idx2] = self.etat.liste[idx2], self.etat.liste[idx1]
                        
                    self.etat.etape += 1
                else:
                    self.etat.termine = True
                    self.etat.temps_fin = time.time()
            else:
                # Animation générique pour les autres algorithmes
                if self.etat.etape < n * 2:
                    indices = sorted(random.sample(range(n), min(3, n)))
                    self.etat.marquer_actif(*indices)
                    
                    # Occasionnellement, échanger des éléments
                    if random.random() < 0.1:
                        for i in range(len(indices)-1):
                            if random.random() < 0.5 and indices[i+1] - indices[i] == 1:
                                self.etat.liste[indices[i]], self.etat.liste[indices[i+1]] = \
                                    self.etat.liste[indices[i+1]], self.etat.liste[indices[i]]
                    
                    self.etat.etape += 1
                else:
                    # Tri final pour montrer le résultat
                    self.etat.liste.sort()
                    self.etat.termine = True
                    self.etat.temps_fin = time.time()
            
            return
        
        # Exécution réelle de l'algorithme
        algo_info = ALGORITHMES[self.algo_actif]
        algo_fonction = algo_info["fonction"]
        
        # Exécution selon le mode (parallèle ou séquentiel)
        if self.parallele:
            liste_triee, temps = tri_parallele(
                self.liste_originale, 
                algo_fonction, 
                mp.cpu_count()
            )
            self.etat.liste = liste_triee
            self.etat.termine = True
            self.etat.temps_fin = self.etat.temps_debut + temps
        else:
            # Exécution séquentielle standard
            liste_triee, temps = algo_fonction(self.liste_originale)
            self.etat.liste = liste_triee
            self.etat.termine = True
            self.etat.temps_fin = self.etat.temps_debut + temps
    
    def _comparer_tous_algorithmes(self):
        """Compare les performances de tous les algorithmes"""
        # Taille des listes à tester
        tailles = [self.taille_liste]
        
        # Effectuer les comparaisons
        self.resultats_comparaison = comparer_algorithmes(
            self.liste_originale, 
            tailles
        )
        
        # Activer le mode comparaison
        self.comparison_mode = True
    
    def _gerer_evenements(self):
        """Gère les événements utilisateur"""
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                return False
            
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # Démarre ou met en pause le tri
                    if self.en_cours:
                        self.en_pause = not self.en_pause
                    else:
                        self.animation_seulement = True  # Mode animation
                        self.en_cours = True
                        self.en_pause = False
                
                elif event.key == K_r:
                    # Régénère une nouvelle liste
                    self.liste_originale = self._generer_liste()
                    self.etat.reinitialiser(self.liste_originale.copy())
                    self.en_cours = False
                    self.en_pause = False
                    self.comparison_mode = False
                    self.surface_cache.clear()
                
                elif event.key == K_UP:
                    # Augmente la taille de la liste
                    self.taille_liste = min(1000, self.taille_liste + 50)
                    self.liste_originale = self._generer_liste()
                    self.etat.reinitialiser(self.liste_originale.copy())
                    self.en_cours = False
                    self.comparison_mode = False
                    self.surface_cache.clear()
                
                elif event.key == K_DOWN:
                    # Diminue la taille de la liste
                    self.taille_liste = max(10, self.taille_liste - 50)
                    self.liste_originale = self._generer_liste()
                    self.etat.reinitialiser(self.liste_originale.copy())
                    self.en_cours = False
                    self.comparison_mode = False
                    self.surface_cache.clear()
                
                elif event.key == K_LEFT:
                    # Algorithme précédent
                    algos = list(ALGORITHMES.keys())
                    idx = algos.index(self.algo_actif)
                    self.algo_actif = algos[(idx - 1) % len(algos)]
                    self.en_cours = False
                    self.surface_cache.clear()
                
                elif event.key == K_RIGHT:
                    # Algorithme suivant
                    algos = list(ALGORITHMES.keys())
                    idx = algos.index(self.algo_actif)
                    self.algo_actif = algos[(idx + 1) % len(algos)]
                    self.en_cours = False
                    self.surface_cache.clear()
                
                elif event.key == K_m:
                    # Changer le mode de visualisation
                    modes = ["BARRES", "CERCLE", "COSMOS", "SPIRALE", "PARTICULES"]
                    idx = modes.index(self.mode_visualisation)
                    self.mode_visualisation = modes[(idx + 1) % len(modes)]
                    self.surface_cache.clear()
                
                elif event.key == K_p:
                    # Activer/désactiver le mode parallèle
                    self.parallele = not self.parallele
                
                elif event.key == K_c:
                    # Comparer tous les algorithmes
                    self._comparer_tous_algorithmes()
                
                elif event.key == K_a:
                    # Basculer entre animation seule et tri réel
                    self.animation_seulement = not self.animation_seulement
        
        return True
    
    def boucle_principale(self):
        """Boucle principale de l'application"""
        en_execution = True
        
        while en_execution:
            # Gestion des événements
            en_execution = self._gerer_evenements()
            
            # Mettre à jour l'état du tri
            if self.en_cours and not self.en_pause:
                self._executer_tri()
            
            # Mettre à jour les variables d'animation globales
            self.temps_global += 1 / FPS
            self.rotation_angle += 0.005
            
            # Effacer l'écran
            self.ecran.fill(COULEURS["fond"])
            
            # Visualiser les données
            surface_visu = self._visualiser_donnees()
            self.ecran.blit(surface_visu, (0, 0))
            
            # Dessiner l'interface utilisateur
            self._dessiner_interface(self.ecran)
            
            # Rafraîchir l'écran
            pygame.display.flip()
            
            # Contrôle du taux de rafraîchissement
            self.horloge.tick(FPS)
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    # Créer et lancer l'application
    app = VisualiseurtriQuantique()
    app.boucle_principale() 