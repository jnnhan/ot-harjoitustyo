import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_rahan_lataus_kasvattaa_saldoa_oikein(self):
        self.maksukortti.lataa_rahaa(500)

        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 15.00 euroa")

    def test_rahan_ottaminen_ilman_saldoa_toimii(self):
        onnistui = self.maksukortti.ota_rahaa(1100)
        
        self.assertFalse(onnistui, "False")
        self.assertTrue(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_rahan_ottaminen_toimii_saldo_riittaa(self):
        onnistui = self.maksukortti.ota_rahaa(500)

        self.assertTrue(onnistui, "True")
        self.assertTrue(str(self.maksukortti), "Kortilla on rahaa 5.00 euroa")