from django.urls import reverse
import pytest

@pytest.mark.django_db
def test_affichage_bouton_connexion_inscription_utilisateur_non_connecte(client):
    url = reverse('accueil')
    response = client.get(url)

    assert response.status_code == 200
    assert "Connexion" in response.content.decode()
    assert "Inscription" in response.content.decode()

@pytest.mark.django_db
def test_affichage_texte_bouton_deconnexion_utilisateur_connecte(client, utilisateur_cree):
    url = reverse('accueil')
    client.login(email="thomas.adrien.ta@gmail.com",
                 password="MotDePasse123456@")
    response = client.get(url)
    content = response.content.decode()

    assert response.status_code == 200
    assert "Bienvenue" in content
    assert "Déconnexion" in content