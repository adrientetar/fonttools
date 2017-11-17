from __future__ import (
    print_function, division, absolute_import, unicode_literals)
from fontTools.misc.py23 import *


from fontTools import unicodedata


def test__binary_search_range():
    ranges = [
        (0, 10, "foo"),
        (11, 11, "bar"),
        (12, 20, "baz"),
        (21, 22, "bum"),
    ]
    search = unicodedata._binary_search_range

    for i in range(11):
        assert search(1, ranges) == "foo"

    assert search(11, ranges) == "bar"

    for i in range(12, 21):
        assert search(i, ranges) == "baz"

    for i in range(21, 23):
        assert search(i, ranges) == "bum"

    assert search(23, ranges) is None


def test_script():
    assert unicodedata.script("a") == "Latin"

    assert hasattr(unicodedata.script, "cache")
    assert unicodedata.script("a") == unicodedata.script.cache["a"]

    # these were randomly sampled, one character per script
    assert unicodedata.script(unichr(0x1E918)) == 'Adlam'
    assert unicodedata.script(unichr(0x1170D)) == 'Ahom'
    assert unicodedata.script(unichr(0x145A0)) == 'Anatolian_Hieroglyphs'
    assert unicodedata.script(unichr(0x0607)) == 'Arabic'
    assert unicodedata.script(unichr(0x056C)) == 'Armenian'
    assert unicodedata.script(unichr(0x10B27)) == 'Avestan'
    assert unicodedata.script(unichr(0x1B41)) == 'Balinese'
    assert unicodedata.script(unichr(0x168AD)) == 'Bamum'
    assert unicodedata.script(unichr(0x16ADD)) == 'Bassa_Vah'
    assert unicodedata.script(unichr(0x1BE5)) == 'Batak'
    assert unicodedata.script(unichr(0x09F3)) == 'Bengali'
    assert unicodedata.script(unichr(0x11C5B)) == 'Bhaiksuki'
    assert unicodedata.script(unichr(0x3126)) == 'Bopomofo'
    assert unicodedata.script(unichr(0x1103B)) == 'Brahmi'
    assert unicodedata.script(unichr(0x2849)) == 'Braille'
    assert unicodedata.script(unichr(0x1A0A)) == 'Buginese'
    assert unicodedata.script(unichr(0x174E)) == 'Buhid'
    assert unicodedata.script(unichr(0x18EE)) == 'Canadian_Aboriginal'
    assert unicodedata.script(unichr(0x102B7)) == 'Carian'
    assert unicodedata.script(unichr(0x1053D)) == 'Caucasian_Albanian'
    assert unicodedata.script(unichr(0x11123)) == 'Chakma'
    assert unicodedata.script(unichr(0xAA1F)) == 'Cham'
    assert unicodedata.script(unichr(0xAB95)) == 'Cherokee'
    assert unicodedata.script(unichr(0x1F0C7)) == 'Common'
    assert unicodedata.script(unichr(0x2C85)) == 'Coptic'
    assert unicodedata.script(unichr(0x12014)) == 'Cuneiform'
    assert unicodedata.script(unichr(0x1082E)) == 'Cypriot'
    assert unicodedata.script(unichr(0xA686)) == 'Cyrillic'
    assert unicodedata.script(unichr(0x10417)) == 'Deseret'
    assert unicodedata.script(unichr(0x093E)) == 'Devanagari'
    assert unicodedata.script(unichr(0x1BC4B)) == 'Duployan'
    assert unicodedata.script(unichr(0x1310C)) == 'Egyptian_Hieroglyphs'
    assert unicodedata.script(unichr(0x1051C)) == 'Elbasan'
    assert unicodedata.script(unichr(0x2DA6)) == 'Ethiopic'
    assert unicodedata.script(unichr(0x10AD)) == 'Georgian'
    assert unicodedata.script(unichr(0x2C52)) == 'Glagolitic'
    assert unicodedata.script(unichr(0x10343)) == 'Gothic'
    assert unicodedata.script(unichr(0x11371)) == 'Grantha'
    assert unicodedata.script(unichr(0x03D0)) == 'Greek'
    assert unicodedata.script(unichr(0x0AAA)) == 'Gujarati'
    assert unicodedata.script(unichr(0x0A4C)) == 'Gurmukhi'
    assert unicodedata.script(unichr(0x23C9F)) == 'Han'
    assert unicodedata.script(unichr(0xC259)) == 'Hangul'
    assert unicodedata.script(unichr(0x1722)) == 'Hanunoo'
    assert unicodedata.script(unichr(0x108F5)) == 'Hatran'
    assert unicodedata.script(unichr(0x05C2)) == 'Hebrew'
    assert unicodedata.script(unichr(0x1B072)) == 'Hiragana'
    assert unicodedata.script(unichr(0x10847)) == 'Imperial_Aramaic'
    assert unicodedata.script(unichr(0x033A)) == 'Inherited'
    assert unicodedata.script(unichr(0x10B66)) == 'Inscriptional_Pahlavi'
    assert unicodedata.script(unichr(0x10B4B)) == 'Inscriptional_Parthian'
    assert unicodedata.script(unichr(0xA98A)) == 'Javanese'
    assert unicodedata.script(unichr(0x110B2)) == 'Kaithi'
    assert unicodedata.script(unichr(0x0CC6)) == 'Kannada'
    assert unicodedata.script(unichr(0x3337)) == 'Katakana'
    assert unicodedata.script(unichr(0xA915)) == 'Kayah_Li'
    assert unicodedata.script(unichr(0x10A2E)) == 'Kharoshthi'
    assert unicodedata.script(unichr(0x17AA)) == 'Khmer'
    assert unicodedata.script(unichr(0x11225)) == 'Khojki'
    assert unicodedata.script(unichr(0x112B6)) == 'Khudawadi'
    assert unicodedata.script(unichr(0x0ED7)) == 'Lao'
    assert unicodedata.script(unichr(0xAB3C)) == 'Latin'
    assert unicodedata.script(unichr(0x1C48)) == 'Lepcha'
    assert unicodedata.script(unichr(0x1923)) == 'Limbu'
    assert unicodedata.script(unichr(0x1071D)) == 'Linear_A'
    assert unicodedata.script(unichr(0x100EC)) == 'Linear_B'
    assert unicodedata.script(unichr(0xA4E9)) == 'Lisu'
    assert unicodedata.script(unichr(0x10284)) == 'Lycian'
    assert unicodedata.script(unichr(0x10926)) == 'Lydian'
    assert unicodedata.script(unichr(0x11161)) == 'Mahajani'
    assert unicodedata.script(unichr(0x0D56)) == 'Malayalam'
    assert unicodedata.script(unichr(0x0856)) == 'Mandaic'
    assert unicodedata.script(unichr(0x10AF0)) == 'Manichaean'
    assert unicodedata.script(unichr(0x11CB0)) == 'Marchen'
    assert unicodedata.script(unichr(0x11D28)) == 'Masaram_Gondi'
    assert unicodedata.script(unichr(0xABDD)) == 'Meetei_Mayek'
    assert unicodedata.script(unichr(0x1E897)) == 'Mende_Kikakui'
    assert unicodedata.script(unichr(0x109B0)) == 'Meroitic_Cursive'
    assert unicodedata.script(unichr(0x10993)) == 'Meroitic_Hieroglyphs'
    assert unicodedata.script(unichr(0x16F5D)) == 'Miao'
    assert unicodedata.script(unichr(0x1160B)) == 'Modi'
    assert unicodedata.script(unichr(0x18A8)) == 'Mongolian'
    assert unicodedata.script(unichr(0x16A48)) == 'Mro'
    assert unicodedata.script(unichr(0x1128C)) == 'Multani'
    assert unicodedata.script(unichr(0x105B)) == 'Myanmar'
    assert unicodedata.script(unichr(0x108AF)) == 'Nabataean'
    assert unicodedata.script(unichr(0x19B3)) == 'New_Tai_Lue'
    assert unicodedata.script(unichr(0x1143D)) == 'Newa'
    assert unicodedata.script(unichr(0x07F4)) == 'Nko'
    assert unicodedata.script(unichr(0x1B192)) == 'Nushu'
    assert unicodedata.script(unichr(0x169C)) == 'Ogham'
    assert unicodedata.script(unichr(0x1C56)) == 'Ol_Chiki'
    assert unicodedata.script(unichr(0x10CE9)) == 'Old_Hungarian'
    assert unicodedata.script(unichr(0x10316)) == 'Old_Italic'
    assert unicodedata.script(unichr(0x10A93)) == 'Old_North_Arabian'
    assert unicodedata.script(unichr(0x1035A)) == 'Old_Permic'
    assert unicodedata.script(unichr(0x103D5)) == 'Old_Persian'
    assert unicodedata.script(unichr(0x10A65)) == 'Old_South_Arabian'
    assert unicodedata.script(unichr(0x10C09)) == 'Old_Turkic'
    assert unicodedata.script(unichr(0x0B60)) == 'Oriya'
    assert unicodedata.script(unichr(0x104CF)) == 'Osage'
    assert unicodedata.script(unichr(0x104A8)) == 'Osmanya'
    assert unicodedata.script(unichr(0x16B12)) == 'Pahawh_Hmong'
    assert unicodedata.script(unichr(0x10879)) == 'Palmyrene'
    assert unicodedata.script(unichr(0x11AF1)) == 'Pau_Cin_Hau'
    assert unicodedata.script(unichr(0xA869)) == 'Phags_Pa'
    assert unicodedata.script(unichr(0x10909)) == 'Phoenician'
    assert unicodedata.script(unichr(0x10B81)) == 'Psalter_Pahlavi'
    assert unicodedata.script(unichr(0xA941)) == 'Rejang'
    assert unicodedata.script(unichr(0x16C3)) == 'Runic'
    assert unicodedata.script(unichr(0x0814)) == 'Samaritan'
    assert unicodedata.script(unichr(0xA88C)) == 'Saurashtra'
    assert unicodedata.script(unichr(0x111C8)) == 'Sharada'
    assert unicodedata.script(unichr(0x1045F)) == 'Shavian'
    assert unicodedata.script(unichr(0x115AD)) == 'Siddham'
    assert unicodedata.script(unichr(0x1D8C0)) == 'SignWriting'
    assert unicodedata.script(unichr(0x0DB9)) == 'Sinhala'
    assert unicodedata.script(unichr(0x110F9)) == 'Sora_Sompeng'
    assert unicodedata.script(unichr(0x11A60)) == 'Soyombo'
    assert unicodedata.script(unichr(0x1B94)) == 'Sundanese'
    assert unicodedata.script(unichr(0xA81F)) == 'Syloti_Nagri'
    assert unicodedata.script(unichr(0x0740)) == 'Syriac'
    assert unicodedata.script(unichr(0x1714)) == 'Tagalog'
    assert unicodedata.script(unichr(0x1761)) == 'Tagbanwa'
    assert unicodedata.script(unichr(0x1965)) == 'Tai_Le'
    assert unicodedata.script(unichr(0x1A32)) == 'Tai_Tham'
    assert unicodedata.script(unichr(0xAA86)) == 'Tai_Viet'
    assert unicodedata.script(unichr(0x116A5)) == 'Takri'
    assert unicodedata.script(unichr(0x0B8E)) == 'Tamil'
    assert unicodedata.script(unichr(0x1754D)) == 'Tangut'
    assert unicodedata.script(unichr(0x0C40)) == 'Telugu'
    assert unicodedata.script(unichr(0x07A4)) == 'Thaana'
    assert unicodedata.script(unichr(0x0E42)) == 'Thai'
    assert unicodedata.script(unichr(0x0F09)) == 'Tibetan'
    assert unicodedata.script(unichr(0x2D3A)) == 'Tifinagh'
    assert unicodedata.script(unichr(0x114B0)) == 'Tirhuta'
    assert unicodedata.script(unichr(0x1038B)) == 'Ugaritic'
    assert unicodedata.script(unichr(0xA585)) == 'Vai'
    assert unicodedata.script(unichr(0x118CF)) == 'Warang_Citi'
    assert unicodedata.script(unichr(0xA066)) == 'Yi'
    assert unicodedata.script(unichr(0x11A31)) == 'Zanabazar_Square'
