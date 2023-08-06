from DevExpress.LookAndFeel import UserLookAndFeel, DefaultLookAndFeel, SkinStyle, SkinSvgPalette


class BDStyle(object):
    def Skin(self, style):
        if style == "wxi":
            _style = SkinStyle.WXI
        elif style == "wxi-freshness":
            _style = SkinSvgPalette.WXI.Freshness
        elif style == "wxi-darkness":
            _style = SkinSvgPalette.WXI.Darkness
        elif style == "wxi-clearness":
            _style = SkinSvgPalette.WXI.Clearness
        elif style == "wxi-sharpness":
            _style = SkinSvgPalette.WXI.Sharpness
        elif style == "wxi-calmness":
            _style = SkinSvgPalette.WXI.Calmness
        if style == "wxicompact":
            _style = SkinStyle.WXICompact
        elif style == "wxicompact-freshness":
            _style = SkinSvgPalette.WXICompact.Freshness
        elif style == "wxicompact-darkness":
            _style = SkinSvgPalette.WXICompact.Darkness
        elif style == "wxicompact-clearness":
            _style = SkinSvgPalette.WXICompact.Clearness
        elif style == "wxicompact-sharpness":
            _style = SkinSvgPalette.WXICompact.Sharpness
        elif style == "wxicompact-calmness":
            _style = SkinSvgPalette.WXICompact.Calmness
        UserLookAndFeel.Default.SetSkinStyle(_style)