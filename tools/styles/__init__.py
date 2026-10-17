# -*- coding: utf-8 -*-
"""Visual styles for the JobNow social visuals.

Each theme of a day's content picks a style with its `style` field (see RUNBOOK.md), and
optionally a `palette` index; without one, the palette rotates with the date.
"""
import datetime

from .base import FORMATS, SCALE, Style
from .bleu import Bleu
from .cahier import Cahier
from .affiche import Affiche
from .dossier import Dossier
from .bureau import Bureau
from .riso import Riso

STYLES = {s.key: s for s in (Bleu, Cahier, Affiche, Dossier, Bureau, Riso)}
NAMES = list(STYLES)

DESCRIPTIONS = {
    'bleu': "le look d'origine : fond bleu quadrillé, surlignage vert citron",
    'cahier': 'page de cahier à grands carreaux, écriture, corrections au stylo rouge, surligneur et post-it',
    'affiche': 'affiche de rue aux couleurs vives, énormes titres condensés, languettes à détacher',
    'dossier': 'chemise cartonnée, feuilles tapées à la machine, tampons encreurs et trombones',
    'bureau': "fenêtres d'ordinateur rétro, police pixel, boîtes de dialogue et barre de progression",
    'riso': 'impression risographie deux encres : grain, trames de points et léger décalage des couleurs',
}


def palette_for(name, date, key):
    n = len(STYLES[name].palettes)
    if n <= 1:
        return 0
    try:
        o = datetime.date.fromisoformat(date).toordinal()
    except (TypeError, ValueError):
        o = 0
    return (o + (0 if key == 'A' else 2)) % n


def get(theme):
    name = theme.get('style') or 'bleu'
    if name not in STYLES:
        raise ValueError(f'style inconnu : {name} (choix : {", ".join(NAMES)})')
    pal = theme.get('palette')
    if pal is None:
        pal = palette_for(name, theme.get('_date'), theme.get('key', 'A'))
    return STYLES[name](int(pal), theme.get('_date'))
