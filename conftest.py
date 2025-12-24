"""Configuration globale pour pytest"""
import pytest
from utilisateur.models import Utilisateur


@pytest.fixture
def utilisateur_cree(db):
    """Fixture réutilisable pour créer un utilisateur de test"""
    return Utilisateur.objects.create_user(
        email="thomas.adrien.ta@gmail.com",
        password="MotDePasse123456@",
        civilite=Utilisateur.Civilite.MONSIEUR,
        prenom="Thomas",
        nom="Adrien",
        adresse="16 rue Jules Védrines",
        cp="26140",
        ville="Saint Rambert d'Albon",
    )
