# Simulation — Code Torique de Kitaev

**CY Tech · GM DATA · Juin 2026**  
Projet académique supervisé par Garrigue.  
Groupe : Imran El Azri Ennassiri, Adel Noui, Tommy Ly, Ayman Munglee.

---

## Description

Simulation numérique de la dynamique d'erreurs du code torique de Kitaev via un **canal de Pauli stochastique classique**. On travaille directement sur le **syndrome** — la grille des valeurs propres $B_p \in \{-1, +1\}$ — ce qui est exactement ce que voit un décodeur en pratique, sans avoir à manipuler les vecteurs d'état quantiques (dimension $2^{2L^2}$, inaccessible pour $L \geq 5$).

---

## Contenu

```
code_torique_simulation.ipynb   ← notebook principal (visualisation complète)
anyons_diffu.py                 ← script Python avec correction MWPM intégrée
README.md                       ← ce fichier
```

---

## Prérequis

```bash
pip install numpy scipy matplotlib tqdm pymatching
```

---

## Structure du notebook

| Section | Contenu | Lien rapport |
|---|---|---|
| 1. Modèle | Fonctions , , ,  | Déf. 8.1 |
| 2. Animation | Heatmap syndrome + courbe anyons, L=30, p=0.01 | §9, §10 |
| 3. Transition de phase | Densité d'anyons vs $p$ pour L=10/20/30 | Prop. 11.1 |
| 4. Comparaison régimes | Snapshots sous-critique / critique / sur-critique | Thm. 12.1 |

---

## Script  — correction MWPM

Ce script étend le notebook en intégrant un décodeur **Minimum Weight Perfect Matching (MWPM)** via la bibliothèque . La correction est appliquée tous les  pas de temps pour mettre en évidence l'efficacité de l'algorithme.

### Paramètres clés

| Paramètre | Description |
|---|---|
|  | Taille de la grille ($n = 2L^2$ qubits) |
|  | Probabilité d'erreur par arête et par pas |
|  | Nombre de pas de temps |
|  | Fréquence d'application du MWPM (tous les $k$ pas) |

---

## Modèle physique

**État** :  $\in \{-1, +1\}$ — valeur propre de l'opérateur plaquette $B_{(i,j)}$.  
Une plaquette avec  contient un **anyon**.

**Pas de temps** : pour chaque arête $e$ du réseau, on tire $q_e \sim 	ext{Bernoulli}(p)$. Si $q_e = 1$, les deux plaquettes adjacentes sont flippées.

**Topologie torique** : indices pris modulo $L$ — pas d'effet de bord.

---

## Conclusions sur l'efficacité du MWPM

L'observation principale de la simulation est que **l'algorithme MWPM se révèle anormalement efficace, quelle que soit la valeur de $p$ et quelle que soit la taille de la grille $L$**. Cela a été vérifié pour des valeurs extrêmes :

- $p = 10^{-8}$ (quasi-absence d'erreurs)
- $p pprox 1$ (saturation quasi-totale du réseau)

Dans tous les cas, le décodeur maintient l'état logique avec une précision remarquable.

**Ce que cela implique :**  
Le seuil $p_{	ext{seuil}} pprox 0.103$ mis en évidence dans le rapport (Dennis et al., 2002) **n'a pas pu être reproduit numériquement** avec cette approche. La raison probable est que le paramètre $p$ seul ne suffit pas à caractériser le régime de la simulation telle qu'elle est implémentée : la fréquence de correction  constitue un second paramètre indépendant qui masque la transition de phase. En appliquant le MWPM à chaque pas (ou très fréquemment), on empêche les anyons de s'accumuler suffisamment pour provoquer une erreur logique, y compris au-delà du seuil théorique.

**Piste d'amélioration :**  
Pour observer la transition à $p_{	ext{seuil}}$, il faudrait étudier le taux d'erreur logique en fonction de $p$ **sans correction dynamique**, ou avec une correction suffisamment rare pour laisser les erreurs s'accumuler. La densité d'anyons et la longueur des chaînes d'erreurs sont les paramètres pertinents à mesurer pour caractériser le régime.

---

## Références

- Kitaev, A. Yu. *Fault-tolerant quantum computation by anyons.* Annals of Physics, 303(1):2–30, 2003.
- Dennis, E., Kitaev, A., Landahl, A., Preskill, J. *Topological quantum memory.* Journal of Mathematical Physics, 43(9):4452–4505, 2002.
- Wang, Alice. *The toric code.* REU Paper, University of Chicago, 2024.
