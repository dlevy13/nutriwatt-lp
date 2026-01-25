# Script de suppression de background

Ce script permet de supprimer automatiquement le background d'une image de logo.

## Installation

1. Installez Python 3.8 ou supérieur si ce n'est pas déjà fait.

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

Ou directement :
```bash
pip install rembg[new] pillow numpy
```

## Utilisation

### Utilisation par défaut (logo Nutriwatt)
```bash
python3 remove_background.py
```

Le script utilisera automatiquement le fichier :
`src/images/nutriwatt-logo-with-name.png`

Le résultat sera sauvegardé dans :
`src/images/nutriwatt-logo-with-name_no_bg.png`

### Utilisation avec un fichier personnalisé
```bash
python3 remove_background.py /chemin/vers/image.png
```

### Spécifier le fichier de sortie
```bash
python3 remove_background.py /chemin/vers/image.png /chemin/vers/sortie.png
```

## Notes

- Le script utilise `rembg` qui utilise un modèle d'IA pour détecter et supprimer automatiquement le background.
- La première exécution peut prendre plus de temps car le modèle doit être téléchargé.
- Le fichier original n'est pas modifié, une nouvelle image est créée.
