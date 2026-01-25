#!/usr/bin/env python3
"""
Script pour supprimer le background d'une image de logo.
Utilise rembg pour la suppression automatique du background.
"""

import sys
import os
from pathlib import Path

try:
    from rembg import remove
    from PIL import Image
    import numpy as np
except ImportError:
    print("Erreur: Les bibliothèques requises ne sont pas installées.")
    print("Installez-les avec: pip install rembg pillow numpy")
    sys.exit(1)


def remove_background(input_path: str, output_path: str = None):
    """
    Supprime le background d'une image.
    
    Args:
        input_path: Chemin vers l'image d'entrée
        output_path: Chemin vers l'image de sortie (optionnel, remplace l'original si non spécifié)
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
    
    # Lire l'image
    with open(input_file, 'rb') as f:
        input_data = f.read()
    
    # Supprimer le background
    output_data = remove(input_data)
    
    # Sauvegarder l'image
    with open(output_file, 'wb') as f:
        f.write(output_data)
    
    print(f"✓ Image sauvegardée: {output_file}")
    print(f"✓ Background supprimé avec succès!")


if __name__ == "__main__":
    # Chemin par défaut
    default_input = "/Users/raphaellevy/Desktop/nutriwatt-lp/src/images/nutriwatt-logo-with-name.png"
    
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        input_path = default_input
        output_path = None
    
    remove_background(input_path, output_path)
