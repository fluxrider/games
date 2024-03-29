#!/usr/bin/env python

import deck as games

# reduce default verbosity of kivy logs
import os
os.environ["KIVY_NO_ENV_CONFIG"] = "1" # TMP workaround until https://github.com/kivy/kivy/pull/6540
os.environ["KCFG_KIVY_LOG_LEVEL"] = "warning"

import kivy

# disable multi-touch emulation, which adds red circles all over when using non-left-click buttons
# however, it break and duplicates android touch events
#import kivy.config
#kivy.config.Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# kivy is sadly an import intensive library
import kivy.app
import kivy.uix.boxlayout
import kivy.uix.image
import kivy.uix.togglebutton

class App(kivy.app.App):

  def build(s):
    s.title = 'Deck Test'
    s.icon = 'res/suits/cardSpades2.png'

    # load 5 cards and make a deck with them
    cards = [kivy.uix.image.Image(source=f'res/suits/{filename}', allow_stretch=True) for filename in games.Deck(os.listdir('res/suits')).ndeal(5)]
    deck = games.Deck(cards)
    # load back cover image
    back_cover = kivy.uix.image.Image(source='res/cardBack_green2.png', allow_stretch=True)

    # layout
    layout = kivy.uix.boxlayout.BoxLayout(padding=5, spacing=5, orientation='vertical')
    deck_layout = kivy.uix.boxlayout.BoxLayout(spacing=5)
    hand_layout = kivy.uix.boxlayout.BoxLayout(spacing=5)
    ctl_layout = kivy.uix.boxlayout.BoxLayout(spacing=5)
    layout.add_widget(deck_layout)
    layout.add_widget(hand_layout)
    layout.add_widget(ctl_layout)
    ctl_layout.add_widget(kivy.uix.togglebutton.ToggleButton(group='place', text='top', state='down'))
    ctl_layout.add_widget(kivy.uix.togglebutton.ToggleButton(group='place', text='shuffle'))
    ctl_layout.add_widget(kivy.uix.togglebutton.ToggleButton(group='place', text='bottom'))

    # sync presentation
    if len(deck) > 0: deck_layout.add_widget(back_cover)

    # radio button helper
    def get_selected_placement_func():
      text = 'top'
      for widget in ctl_layout.children:
        if widget.state == 'down':
          text = widget.text
      if text == 'shuffle': return deck.place_shuffle
      if text == 'bottom': return deck.place_bottom
      return deck.place_top

    # touch events
    touch_list = []

    def on_touch_down(what, touch):
      # store the widgets the touch down collides with so we can match it in touch_up
      widgets = hand_layout.children + deck_layout.children
      for widget in widgets:
        if widget.collide_point(*touch.pos):
          touch_list.append(widget)
      return False

    def on_touch_up(what, touch):
      # TODO: collision doesn't take into account that the actual image may not cover the entire image widget

      for widget in touch_list:
        if widget.collide_point(*touch.pos):
          # hand
          if widget in hand_layout.children:
            # remove card from hand
            hand_layout.remove_widget(widget)
            # show the back cover image if deck will not be empty anymore
            if len(deck) == 0: deck_layout.add_widget(back_cover)
            # place it on the deck
            get_selected_placement_func()(widget)

          # deck
          if widget in deck_layout.children:
            # draw a card
            hand_layout.add_widget(deck.deal())
            # remove back cover image if deck is empty
            if len(deck) == 0: deck_layout.remove_widget(back_cover)

      touch_list.clear()
      return False

    layout.bind(on_touch_up=on_touch_up)
    layout.bind(on_touch_down=on_touch_down)

    return layout

App().run()
