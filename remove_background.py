#!/usr/bin/env python3
"""
Script pour supprimer le background blanc d'une image de logo.
Détecte et supprime uniquement les pixels blancs/très clairs du background.
"""

import sys
from pathlib import Path

try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("Erreur: Les bibliothèques requises ne sont pas installées.")
    print("Installez-les avec: pip install pillow numpy")
    sys.exit(1)


def remove_white_background(input_path: str, output_path: str = None, threshold: int = 245):
    """
    Supprime le background blanc d'une image en préservant le logo.
    
    Args:
        input_path: Chemin vers l'image d'entrée
        output_path: Chemin vers l'image de sortie (optionnel, remplace l'original si None)
        threshold: Seuil de luminosité pour considérer un pixel comme blanc (0-255)
    """
    input_file = Path(input_path)
    
    if not input_file.exists():
        print(f"Erreur: Le fichier {input_path} n'existe pas.")
        sys.exit(1)
    
    if output_path is None:
        output_file = input_file
    else:
        output_file = Path(output_path)
    
    print(f"Traitement de l'image: {input_path}")
    print(f"Suppression du background blanc (seuil: {threshold})...")
    
    # Ouvrir l'image
    img = Image.open(input_file)
    
    # Convertir en RGBA si ce n'est pas déjà le cas
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Convertir en numpy array
    data = np.array(img)
    
    # Extraire les canaux RGB
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # Détecter les pixels blancs/très clairs (background)
    # Un pixel est considéré comme background si R, G et B sont tous > threshold
    white_background = (r > threshold) & (g > threshold) & (b > threshold)
    
    # Rendre ces pixels transparents
    data[:,:,3] = np.where(white_background, 0, a)
    
    # Créer la nouvelle image
    result_img = Image.fromarray(data, 'RGBA')
    
    # Sauvegarder
    result_img.save(output_file, 'PNG', optimize=True)
    
    print(f"✓ Image sauvegardée: {output_file}")
    print(f"✓ Background blanc supprimé avec succès!")


if __name__ == "__main__":
    # Chemin par défaut
    default_input = "/Users/raphaellevy/Desktop/nutriwatt-lp/src/images/nutriwatt-logo-with-name.png"
    
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
        threshold = int(sys.argv[3]) if len(sys.argv) > 3 else 245
    else:
        input_path = default_input
        output_path = None
        threshold = 245
    
    remove_white_background(input_path, output_path, threshold)
