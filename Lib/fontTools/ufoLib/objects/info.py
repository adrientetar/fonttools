import attr
from ._common import Number, OptString


@attr.s(slots=True)
class Info(object):
    familyName = attr.ib(default=None, type=OptString)
    styleName = attr.ib(default=None, type=OptString)
    styleMapFamilyName = attr.ib(default=None, type=OptString)
    styleMapStyleName = attr.ib(default=None, type=OptString)
    versionMajor = attr.ib(default=None, type=int)
    # type is positive integer
    versionMinor = attr.ib(default=None, type=int)

    copyright = attr.ib(default=None, type=OptString)
    trademark = attr.ib(default=None, type=OptString)

    # type is positive Number
    unitsPerEm = attr.ib(default=None, type=Number)
    descender = attr.ib(default=None, type=Number)
    xHeight = attr.ib(default=None, type=Number)
    capHeight = attr.ib(default=None, type=Number)
    ascender = attr.ib(default=None, type=Number)
    italicAngle = attr.ib(default=None, type=Number)

    note = attr.ib(default=None, type=OptString)

    # note: all list entries have detailed speccing
    openTypeGaspRangeRecords = attr.ib(default=None, type=list)
    openTypeHeadCreated = attr.ib(default=None, type=OptString)
    # type is positive integer
    openTypeHeadLowestRecPPEM = attr.ib(default=None, type=int)
    openTypeHeadFlags = attr.ib(default=None, type=list)

    openTypeHheaAscender = attr.ib(default=None, type=int)
    openTypeHheaDescender = attr.ib(default=None, type=int)
    openTypeHheaLineGap = attr.ib(default=None, type=int)
    openTypeHheaCaretSlopeRise = attr.ib(default=None, type=int)
    openTypeHheaCaretSlopeRun = attr.ib(default=None, type=int)
    openTypeHheaCaretOffset = attr.ib(default=None, type=int)

    openTypeNameDesigner = attr.ib(default=None, type=OptString)
    openTypeNameDesignerURL = attr.ib(default=None, type=OptString)
    openTypeNameManufacturer = attr.ib(default=None, type=OptString)
    openTypeNameManufacturerURL = attr.ib(default=None, type=OptString)
    openTypeNameLicense = attr.ib(default=None, type=OptString)
    openTypeNameLicenseURL = attr.ib(default=None, type=OptString)
    openTypeNameVersion = attr.ib(default=None, type=OptString)
    openTypeNameUniqueID = attr.ib(default=None, type=OptString)
    openTypeNameDescription = attr.ib(default=None, type=OptString)
    openTypeNamePreferredFamilyName = attr.ib(default=None, type=OptString)
    openTypeNamePreferredSubfamilyName = attr.ib(default=None, type=OptString)
    openTypeNameCompatibleFullName = attr.ib(default=None, type=OptString)
    openTypeNameSampleText = attr.ib(default=None, type=OptString)
    openTypeNameWWSFamilyName = attr.ib(default=None, type=OptString)
    openTypeNameWWSSubfamilyName = attr.ib(default=None, type=OptString)
    openTypeNameRecords = attr.ib(default=None, type=list)

    openTypeOS2WidthClass = attr.ib(default=None, type=int)
    openTypeOS2WeightClass = attr.ib(default=None, type=int)
    openTypeOS2Selection = attr.ib(default=None, type=list)
    openTypeOS2VendorID = attr.ib(default=None, type=OptString)
    openTypeOS2Panose = attr.ib(default=None, type=list)
    openTypeOS2FamilyClass = attr.ib(default=None, type=list)
    openTypeOS2UnicodeRanges = attr.ib(default=None, type=list)
    openTypeOS2CodePageRanges = attr.ib(default=None, type=list)
    openTypeOS2TypoAscender = attr.ib(default=None, type=int)
    openTypeOS2TypoDescender = attr.ib(default=None, type=int)
    openTypeOS2TypoLineGap = attr.ib(default=None, type=int)
    # positive int
    openTypeOS2WinAscent = attr.ib(default=None, type=int)
    # positive int
    openTypeOS2WinDescent = attr.ib(default=None, type=int)
    openTypeOS2Type = attr.ib(default=None, type=list)
    openTypeOS2SubscriptXSize = attr.ib(default=None, type=int)
    openTypeOS2SubscriptYSize = attr.ib(default=None, type=int)
    openTypeOS2SubscriptXOffset = attr.ib(default=None, type=int)
    openTypeOS2SubscriptYOffset = attr.ib(default=None, type=int)
    openTypeOS2SuperscriptXSize = attr.ib(default=None, type=int)
    openTypeOS2SuperscriptYSize = attr.ib(default=None, type=int)
    openTypeOS2SuperscriptXOffset = attr.ib(default=None, type=int)
    openTypeOS2SuperscriptYOffset = attr.ib(default=None, type=int)
    openTypeOS2StrikeoutSize = attr.ib(default=None, type=int)
    openTypeOS2StrikeoutPosition = attr.ib(default=None, type=int)

    openTypeVheaAscender = attr.ib(default=None, type=int)
    openTypeVheaDescender = attr.ib(default=None, type=int)
    openTypeVheaLineGap = attr.ib(default=None, type=int)
    openTypeVheaCaretSlopeRise = attr.ib(default=None, type=int)
    openTypeVheaCaretSlopeRun = attr.ib(default=None, type=int)
    openTypeVheaCaretOffset = attr.ib(default=None, type=int)

    postscriptFontName = attr.ib(default=None, type=OptString)
    postscriptFullName = attr.ib(default=None, type=OptString)
    postscriptSlantAngle = attr.ib(default=None, type=Number)
    postscriptUniqueID = attr.ib(default=None, type=int)
    postscriptUnderlineThickness = attr.ib(default=None, type=Number)
    postscriptUnderlinePosition = attr.ib(default=None, type=Number)
    postscriptIsFixedPitch = attr.ib(default=None, type=bool)
    postscriptBlueValues = attr.ib(default=None, type=list)
    postscriptOtherBlues = attr.ib(default=None, type=list)
    postscriptFamilyBlues = attr.ib(default=None, type=list)
    postscriptFamilyOtherBlues = attr.ib(default=None, type=list)
    postscriptStemSnapH = attr.ib(default=None, type=list)
    postscriptStemSnapV = attr.ib(default=None, type=list)
    postscriptBlueFuzz = attr.ib(default=None, type=Number)
    postscriptBlueShift = attr.ib(default=None, type=Number)
    postscriptBlueScale = attr.ib(default=None, type=float)
    postscriptForceBold = attr.ib(default=None, type=bool)
    postscriptDefaultWidthX = attr.ib(default=None, type=Number)
    postscriptNominalWidthX = attr.ib(default=None, type=Number)
    postscriptWeightName = attr.ib(default=None, type=OptString)
    postscriptDefaultCharacter = attr.ib(default=None, type=OptString)
    postscriptWindowsCharacterSet = attr.ib(default=None, type=OptString)
