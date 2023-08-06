from bird.object import BObject


class BTThumbnailButton(BObject):
    def Init(self):
        from Telerik.WinControls.Taskbar import RadThumbnailButton
        self._ = RadThumbnailButton()
