from django.utils import timezone
from django.core.exceptions import ValidationError

from utilisateur.models import Utilisateur
import pytest

@pytest.fixture
def utilisateur_cree(db):
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

def test_modele_Utilisateur_date_de_creation(utilisateur_cree):
    assert utilisateur_cree.creation is not None

def test_modele_Utilisateur_creation_code_utilisateur(utilisateur_cree):
    maintenant=timezone.now()
    date=f"{maintenant.month:02d}{maintenant.year}"
    assert utilisateur_cree.code is not None
    assert utilisateur_cree.code.startswith("ID-")
    assert utilisateur_cree.code.endswith("0001")
    assert utilisateur_cree.code==f"ID-{date}-0001"

def test_modele_Utilisateur_creation_slug(utilisateur_cree):
    maintenant=timezone.now()
    date=f"{maintenant.month:02d}{maintenant.year}"
    assert utilisateur_cree.slug is not None
    assert utilisateur_cree.slug==f"id-{date}-0001"

def test_modele_Utilisateur_tel_valide(utilisateur_cree):
    utilisateur_cree.tel="0665962952"
    utilisateur_cree.full_clean()
    assert utilisateur_cree.tel=="0665962952"

def test_modele_Utilisateur_tel_moins_de_10_chiffres(utilisateur_cree):
    utilisateur_cree.tel="066596295"
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()

def test_modele_Utilisateur_tel_plus_de_10_chiffres(utilisateur_cree):
    utilisateur_cree.tel="06659629521"
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()

def test_modele_Utilisateur_tel_pas_que_chiffre(utilisateur_cree):
    utilisateur_cree.tel="066596295a"
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()

def test_modele_Utilisateur_tel_vide(utilisateur_cree):
    utilisateur_cree.tel=""
    utilisateur_cree.full_clean()
    assert utilisateur_cree.tel==""

def test_modele_Utilisateur_cp_valide(utilisateur_cree):
    utilisateur_cree.full_clean()
    assert utilisateur_cree.cp=="26140"

def test_modele_Utilisateur_cp_moins_de_5_chiffres(utilisateur_cree):
    utilisateur_cree.cp="2614"
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()

def test_modele_Utilisateur_cp_plus_de_5_chiffres(utilisateur_cree):
    utilisateur_cree.cp="261400"
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()

def test_modele_Utilisateur_cp_pas_que_chiffres(utilisateur_cree):
    utilisateur_cree.cp="2614a"
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()

def test_mdoele_Utilisateur_cp_vide(utilisateur_cree):
    utilisateur_cree.cp=""
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()

def test_modele_Utilisateur_email_valide(utilisateur_cree):
    utilisateur_cree.full_clean()
    assert utilisateur_cree.email=="thomas.adrien.ta@gmail.com"


def test_modele_Utilisateur_email_non_valide(utilisateur_cree):
    utilisateur_cree.email="thomasgmail.com"
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()

def test_modele_Utilisateur_email_vide(utilisateur_cree):
    utilisateur_cree.email=""
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()


def test_modele_Utilisateur_email_en_doublon(utilisateur_cree):
    utilisateur_doublon = Utilisateur(
        email="thomas.adrien.ta@gmail.com",
        password="mOTdEpASSE654321!",
        civilite=Utilisateur.Civilite.MADAME,
        prenom="Valentine",
        nom="Schu",
        adresse="16 rue de l'église",
        cp="58500",
        ville="Clamecy",
    )
    with pytest.raises(ValidationError):
        utilisateur_doublon.full_clean()

def test_modele_Utilisateur_email_mis_en_majuscule(utilisateur_cree):
    utilisateur_cree.email="THOMAS.ADRIEN.TA@GMAIL.COM"
    utilisateur_cree.full_clean()
    assert utilisateur_cree.email=="thomas.adrien.ta@gmail.com"

def test_modele_Utilisateur_email_avec_espace_avant_et_apres_email(utilisateur_cree):
    utilisateur_cree.email=" thomas.adrien.ta@gmail.com "
    utilisateur_cree.clean()
    assert utilisateur_cree.email=="thomas.adrien.ta@gmail.com"

def test_modele_Utilisateur_civilite_moniseur(utilisateur_cree):
    assert utilisateur_cree.civilite=="M"

def test_modele_Utilisateur_civilite_madame(utilisateur_cree):
    utilisateur_cree.civilite=Utilisateur.Civilite.MADAME
    assert utilisateur_cree.civilite=="Mme"

def test_modele_Utilisateur_civilite_entreprise(utilisateur_cree):
    utilisateur_cree.civilite=Utilisateur.Civilite.ENTREPRISE
    assert utilisateur_cree.civilite=="Entr"

def test_modele_Utilisateur_civilite_invalide(utilisateur_cree):
    utilisateur_cree.civilite="invalide"
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()

def test_modele_Utilisateur_civilite_vide(utilisateur_cree):
    utilisateur_cree.civilite=""
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()

def test_modele_Utilisateur_nom_rempli(utilisateur_cree):
    assert utilisateur_cree.nom=="Adrien"

def test_modele_Utilisateur_nom_vide(utilisateur_cree):
    utilisateur_cree.nom=""
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()

def test_modele_Utilisateur_prenom_rempli(utilisateur_cree):
    assert utilisateur_cree.prenom=="Thomas"

def test_modele_Utilisateur_prenom_vide(utilisateur_cree):
    utilisateur_cree.prenom=""
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()

def test_modele_Utilisateur_adresse_rempli(utilisateur_cree):
    assert utilisateur_cree.adresse=="16 rue Jules Védrines"

def test_modele_Utilisateur_adresse_vide(utilisateur_cree):
    utilisateur_cree.adresse=""
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()

def test_modele_complement_rempli(utilisateur_cree):
    utilisateur_cree.complement="Appartement 2"
    assert utilisateur_cree.complement=="Appartement 2"

def test_modele_complement_vide(utilisateur_cree):
    utilisateur_cree.complement=""
    assert utilisateur_cree.complement==""

def test_modele_Utilisateur_ville_lettre_uniquement(utilisateur_cree):
    utilisateur_cree.ville="Clamecy"
    assert utilisateur_cree.ville=="Clamecy"

def test_modele_Utilisateur_ville_avec_espace_tiret_apostrophe(utilisateur_cree):
    utilisateur_cree.ville="Saint-Rambert d'Albon"
    assert utilisateur_cree.ville=="Saint-Rambert d'Albon"

def test_modele_Utilisateur_ville_accent_cedille_(utilisateur_cree):
    utilisateur_cree.ville="Saint François de l'Isère"
    assert utilisateur_cree.ville=="Saint François de l'Isère"

def test_modele_Utilisateur_ville_parenthese(utilisateur_cree):
    utilisateur_cree.ville="Mantaille (commune d'Anneyron)"
    assert utilisateur_cree.ville=="Mantaille (commune d'Anneyron)"

def test_modele_Utilisateur_ville_non_valide(utilisateur_cree):
    utilisateur_cree.ville="Saint Rambert d'Albon 456"
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()

def test_modele_Utilisateur_ville_vide(utilisateur_cree):
    utilisateur_cree.ville=""
    with pytest.raises(ValidationError):
        utilisateur_cree.full_clean()




"""
-mdp valide
-mdp – 8 caractères
-mdp sans lettre
-mdp sans chiffre
-mdp sans caractères spécial
-mdp sans maj
-mdp sans min
-mdp vide
-is_active, is_staff, is_superuser pour create user
-is_active, is_staff, is_superuser pour create superuser
"""