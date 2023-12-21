#!/usr/bin/env python3
# pylint: disable=maybe-no-member

"""
TO DO
"""

import os
import cv2
import numpy as np
from PIL import Image

def generate_versus(image_path1, image_path2, model_path):
    """
    TO DO
    """
    _, model_width, _ = cv2.imread(model_path).shape

    crop_path1, height1, width1  = crop_and_save_image(image_path1)
    crop_path2, height2, _ = crop_and_save_image(image_path2)

    diagonal_coords_1 = [[width1, 0], [width1-model_width, height1], [width1, height1]]
    diagonal_coords_2 = [[0, 0], [model_width, 0], [0, height2]]

    slice_path1 = remove_background(crop_path1, diagonal_coords_1)
    slice_path2 = remove_background(crop_path2, diagonal_coords_2)

    combine_images(slice_path1, slice_path2, model_path, model_width+2)

def crop_and_save_image(image_path):
    """
    TO DO
    """
    new_height = 1000
    new_width = 700

    # Charger l'image
    image = cv2.imread(image_path)

    # Obtenir les dimensions actuelles de l'image
    height, width, _ = image.shape

    # Calculer le ratio de redimensionnement
    target_ratio = new_width / new_height
    current_ratio = width / height

    if current_ratio < target_ratio:
        # Recadrer l'image en retirant une partie de l'image en haut et en bas
        target_height = int(width / target_ratio)
        crop_start = int((height - target_height) / 2)
        crop_end = int(crop_start + target_height)
        cropped_image = image[crop_start:crop_end, :]
    else:
        # Recadrer l'image en retirant une partie de l'image à gauche et à droite
        target_width = int(height * target_ratio)
        crop_start = int((width - target_width) / 2)
        crop_end = int(crop_start + target_width)
        cropped_image = image[:, crop_start:crop_end]

    # Redimensionner l'image aux nouvelles dimensions
    resized_image = cv2.resize(cropped_image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Sauvegarder l'image redimensionnée à l'emplacement spécifié
    output_path = 'data/resized_images/cropped_' + os.path.basename(image_path)
    cv2.imwrite(output_path, resized_image)

    return output_path, new_height, new_width 

def remove_background(image_path, diagonal_coords):
    """
    TO DO
    """
    # Charger l'image
    image = cv2.imread(image_path)

    # Créer un masque d'image avec des pixels opaques (canal alpha à 255)
    mask = np.ones_like(image[:, :, 0], dtype=np.uint8) * 255

    # Tracer la diagonale et marquer les pixels correspondants dans le masque comme transparents
    cv2.drawContours(mask, [np.array(diagonal_coords)], -1, 0, thickness=cv2.FILLED)

    # Séparer les canaux B, G, R de l'image d'origine
    blue, green, red = cv2.split(image)

    # Convertir les canaux en format RGBA en ajoutant un canal alpha
    bgra = cv2.merge((blue, green, red, mask))

    # Enregistrer l'image résultante au format PNG avec transparence
    file_name = os.path.basename(image_path).replace('cropped_', '')
    output_path = 'data/resized_images/sliced_' + file_name.replace('.jpg', '.png')
    cv2.imwrite(output_path, bgra)

    return output_path

def combine_images(image1_path, image2_path, model_path, superposition):
    """
    TO DO
    """
    # Charger les images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    model = Image.open(model_path)

    # Récupérer les dimensions des images
    largeur_image1, hauteur_image1 = image1.size
    largeur_image2, hauteur_image2 = image2.size

    # Déterminer les dimensions du fond blanc
    hauteur_fond = max(hauteur_image1, hauteur_image2)
    largeur_fond = largeur_image1 + largeur_image2 - superposition

    # Créer une nouvelle image avec le fond blanc
    fond = Image.new('RGBA', (largeur_fond, hauteur_fond), (255, 255, 255, 255))

    # Placer la première image à gauche
    fond.paste(image1, (0, 0), mask=image1)

    # Placer la deuxième image à droite
    fond.paste(image2, (largeur_image1-superposition, 0), mask=image2)

    # Placement du modèle
    fond.paste(model, (largeur_image1-superposition, 0), mask=model)

    # Sauvegarder l'image combinée
    name1 = os.path.basename(image1_path).replace('.png', '').replace('sliced_', '')
    name2 = os.path.basename(image2_path).replace('.png', '').replace('sliced_', '')
    output_path = f'data/vs_images/{name1}_VS_{name2}.png'
    fond.save(output_path)
