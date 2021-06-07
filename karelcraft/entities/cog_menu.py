from ursina import *


class CogMenu(ButtonList):
    def __init__(self, options_dict):
        super().__init__(
            button_dict=options_dict,
            width=.35,
            x=.58,
            enabled=False,
            eternal=True
        )
        self.y = -.45 + self.scale_y
        self.scale *= .75
        self.text_entity.x += .025
        self.highlight.color = color.azure

        info_text = '''Karelcraft by MKC'''
        self.info = Button(parent=self,
                           model='quad',
                           text='<gray>?',
                           color=color.green,
                           scale=.2,
                           x=1,
                           y=.01,
                           origin=(.5, -.5),
                           tooltip=Tooltip(info_text, scale=.75,
                                           origin=(-.5, -.5))
                           )
        self.info.text_entity.scale *= .75

        self.cog_button = Button(
            parent=camera.ui,
            eternal=True,
            model='circle',
            color=color.gray,
            highlight_color=color.green,
            scale=.04,
            origin=(1, -1),
            position=window.bottom_right
        )

        def _toggle_menu():
            self.enabled = not self.enabled
        self.cog_button.on_click = _toggle_menu
