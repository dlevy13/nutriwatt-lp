#!/usr/bin/env python3
"""
Script pour supprimer le background d'une image de logo.
Version simplifiée utilisant PIL pour détecter et supprimer les pixels de background.
"""

import sys
import os
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("Erreur: Les bibliothèques requises ne sont pas installées.")
    print("Installez-les avec: pip install pillow numpy")
    sys.exit(1)


def remove_background_simple(input_path: str, output_path: str = None, threshold: int = 240):
    """
    Supprime le background blanc/clair d'une image en détectant les pixels clairs.
    
    Args:
        input_path: Chemin vers l'image d'entrée
        output_path: Chemin vers l'image de sortie (optionnel)
        threshold: Seuil de luminosité pour considérer un pixel comme background (0-255)
    """
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"Erreur: Le fichier {input_path} n'existe pas.")
        sys.exit(1)
    
    if output_path is None:
        # Créer un nom de fichier avec _no_bg
        output_file = input_file.parent / f"{input_file.stem}_no_bg{input_file.suffix}"
    else:
        output_file = Path(output_path)
    
    print(f"Traitement de l'image: {input_path}")
    print(f"Suppression du background en cours...")
    
    # Ouvrir l'image
    img = Image.open(input_file)
    
    # Convertir en RGBA si ce n'est pas déjà le cas
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Convertir en numpy array
    data = np.array(img)
    
    # Détecter les pixels de background (pixels très clairs)
    # On considère comme background les pixels où R, G, B sont tous > threshold
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # Créer un masque pour les pixels de background
    # Background = pixels où R, G, B sont tous élevés (blanc/clair)
    background_mask = (r > threshold) & (g > threshold) & (b > threshold)
    
    # Mettre l'alpha à 0 pour les pixels de background
    data[:,:,3] = np.where(background_mask, 0, a)
    
    # Créer la nouvelle image
    result_img = Image.fromarray(data, 'RGBA')
    
    # Sauvegarder
    result_img.save(output_file, 'PNG')
    
    print(f"✓ Image sauvegardée: {output_file}")
    print(f"✓ Background supprimé avec succès!")


if __name__ == "__main__":
    # Chemin par défaut
    default_input = "/Users/davidlevy/Documents/David/NutriApp/SiteWeb/nutriwatt-lp/src/images/nutriwatt-logo-with-name.png"
    
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        input_path = default_input
        output_path = None
    
    remove_background_simple(input_path, output_path)
