# Simulation — Code Torique de Kitaev

**CY Tech · GM DATA · Juin 2026**  
Projet académique supervisé par Garrigue.  
Groupe : Imran El Azri Ennassiri, Adel Noui, Tommy Ly, Ayman Munglee.

---

## Description

Simulation numérique de la dynamique d'erreurs du code torique de Kitaev via un **canal de Pauli stochastique classique**. On travaille directement sur le **syndrome** — la grille des valeurs propres $B_p \in \{-1, +1\}$ — ce qui est exactement ce que voit un décodeur en pratique, sans avoir à manipuler les vecteurs d'état quantiques (dimension $2^{2L^2}$, inaccessible pour $L \geq 5$).

Le notebook illustre les résultats des sections 8–12 du rapport.

---

## Contenu

```
code_torique_simulation.ipynb   ← notebook principal
README.md                       ← ce fichier
```

---

## Prérequis

```bash
pip install numpy matplotlib tqdm
```

Pas de dépendance à des bibliothèques de physique quantique — la simulation est purement classique sur le syndrome.

---

## Structure du notebook

| Section | Contenu | Lien rapport |
|---|---|---|
| 1. Modèle | Fonctions `edge_h/v`, `adjacent_plaquettes`, `step`, `simulate` | Déf. 8.1 |
| 2. Animation | Heatmap syndrome + courbe anyons, L=30, p=0.01 | §9, §10 |
| 3. Transition de phase | Densité d'anyons vs $p$ pour L=10/20/30 | Prop. 11.1 |
| 4. Comparaison régimes | Snapshots sous-critique / critique / sur-critique | Thm. 12.1 |

---

## Modèle physique

**État** : `syndrome[i,j]` $\in \{-1, +1\}$ — valeur propre de l'opérateur plaquette $B_{(i,j)}$.  
Une plaquette avec `syndrome = -1` contient un **anyon**.

**Pas de temps** : pour chaque arête $e$ du réseau (horizontales + verticales), on tire $q_e \sim \text{Bernoulli}(p)$. Si $q_e = 1$, les deux plaquettes adjacentes sont flippées :
$$B_p \mapsto -B_p \quad \text{pour } p \text{ adjacent à } e.$$

**Topologie torique** : les indices sont pris modulo $L$ — pas d'effet de bord.

---

## Paramètres clés

| Paramètre | Valeur par défaut | Description |
|---|---|---|
| `L` | 30 | Taille de la grille ($n = 2L^2$ qubits physiques) |
| `p` | 0.01 | Probabilité d'erreur par arête et par pas |
| `n_steps` | 300 | Nombre de pas de temps (animation) |
| `p_seuil` | ≈ 0.103 | Seuil de la transition de phase (Dennis et al., 2002) |

---

## Ce que la simulation montre

- **Anyons toujours en nombre pair** — Proposition 9.2 du rapport (`np.sum(syndrome == -1)` toujours pair, quelle que soit la suite d'erreurs).
- **Régime sous-critique** ($p \ll 0.103$) : anyons rares, isolés, dynamique lente.
- **Régime critique** ($p \approx 0.103$) : amas d'anyons sans échelle caractéristique — connexion avec la percolation (Dennis et al., 2002).
- **Régime sur-critique** ($p > 0.103$) : quasi-saturation du réseau, erreurs logiques inévitables.

## Ce que la simulation ne montre pas

La diffusion au sens quantique rigoureux, ni la mesure quantitative de l'invariance d'échelle à la transition — ces affirmations nécessiteraient des mesures de percolation supplémentaires. Le syndrome est une projection classique de l'état quantique : c'est une approximation valide pour modéliser le comportement du décodeur, pas l'évolution unitaire complète.

---

## Références

- Kitaev, A. Yu. *Fault-tolerant quantum computation by anyons.* Annals of Physics, 303(1):2–30, 2003.
- Dennis, E., Kitaev, A., Landahl, A., Preskill, J. *Topological quantum memory.* Journal of Mathematical Physics, 43(9):4452–4505, 2002.
- Wang, Alice. *The toric code.* REU Paper, University of Chicago, 2024.
