import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_luotu_kassapaate_on_olemassa(self):
        self.assertNotEqual(self.kassapaate, None)

    def test_kassassa_rahaa_oikea_maara(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_myytyja_lounaita_oikea_maara(self):
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kateisosto_toimii_edullisesti_maksu_riittaa(self):
        maksu = 250
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(maksu)
        self.assertEqual(vaihtoraha, 10)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_kateisosto_toimii_edullisesti_maksu_ei_riita(self):
        maksu = 200
        vaihtoraha = self.kassapaate.syo_edullisesti_kateisella(maksu)
        self.assertEqual(vaihtoraha, 200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kateisosto_toimii_maukkaasti_maksu_riittaa(self):
        maksu = 440
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(maksu)
        self.assertEqual(vaihtoraha, 40)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kateisosto_toimii_maukkaasti_maksu_ei_riita(self):
        maksu = 300
        vaihtoraha = self.kassapaate.syo_maukkaasti_kateisella(maksu)
        self.assertEqual(vaihtoraha, 300)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_korttiosto_toimii_edullisesti_kortilla_rahaa(self):
        kortti = Maksukortti(1000)
        onnistui = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertTrue(onnistui, "True")
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(str(kortti), "Kortilla on rahaa 7.60 euroa")

    def test_korttiosto_toimii_edullisesti_kortilla_ei_rahaa(self):
        kortti = Maksukortti(100)
        onnistui = self.kassapaate.syo_edullisesti_kortilla(kortti)
        self.assertFalse(onnistui, "False")
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(str(kortti), "Kortilla on rahaa 1.00 euroa")

    def test_korttiosto_toimii_maukkaasti_kortilla_rahaa(self):
        kortti = Maksukortti(1000)
        onnistui = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertTrue(onnistui, "True")
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(str(kortti), "Kortilla on rahaa 6.00 euroa")

    def test_korttiosto_toimii_maukkaasti_kortilla_ei_rahaa(self):
        kortti = Maksukortti(100)
        onnistui = self.kassapaate.syo_maukkaasti_kortilla(kortti)
        self.assertFalse(onnistui, "False")
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(str(kortti), "Kortilla on rahaa 1.00 euroa")

    def test_kortille_rahan_lataus_onnistuu_saldo_muuttuu(self):
        kortti = Maksukortti(100)
        raha = 5000
        self.kassapaate.lataa_rahaa_kortille(kortti, raha)
        self.assertEqual(str(kortti), "Kortilla on rahaa 51.00 euroa")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 105000)

    def test_rahan_lataus_ei_muuta_saldoa_negatiivisesti(self):
        kortti = Maksukortti(100)
        self.kassapaate.lataa_rahaa_kortille(kortti, -100)
        self.assertEqual(str(kortti), "Kortilla on rahaa 1.00 euroa")
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
