#!/usr/bin/env python

import os

os.environ["KIVY_NO_ENV_CONFIG"] = "1" # TMP workaround until https://github.com/kivy/kivy/pull/6540
os.environ["KCFG_KIVY_LOG_LEVEL"] = "warning"

# TODO right/middle click add red circle. WTF?

# kivy is sadly an import intensive library
import kivy
import kivy.app
import kivy.uix.boxlayout
import kivy.uix.image
import kivy.uix.togglebutton
import deck as games

# TODO app icon
class App(kivy.app.App):

  def build(s):
    s.title = 'Deck Test'

    # load 5 cards
    back = kivy.uix.image.Image(source='res/cardBack_green2.png', allow_stretch=True)
    cards = []
    files = games.Deck(os.listdir('res/suits')).ndeal(5)
    for filename in files:
      cards.append(kivy.uix.image.Image(source=f'res/suits/{filename}', allow_stretch=True))

    # create deck
    deck = games.Deck(cards)

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
    if len(deck) > 0: deck_layout.add_widget(back)

    # touch events
    touch_list = []

    def on_touch_down(what, touch):
      # store the widgets the touch down collides with so we can match it in touch_up
      nonlocal touch_list
      widgets = hand_layout.children + deck_layout.children
      for widget in widgets:
        if widget.collide_point(*touch.pos):
          touch_list.append(widget)
      return False

    def on_touch_up(what, touch):
      # TODO: collision doesn't take into account that the actual image may not cover the entire image widget

      # TODO find a way to have a handler for deck/hand instead of doing two separate collision loops
      # TODO just go through the widgets in touch_list

      # card
      for card in hand_layout.children[:]:
        if card.collide_point(*touch.pos):
          if card in touch_list:
            # remove card from hand
            hand_layout.remove_widget(card)
            # show the back cover image if deck will not be empty anymore
            if len(deck) == 0: deck_layout.add_widget(back)
            # place it on the deck
            deck.place_top(card)

      # deck
      for card in deck_layout.children:
        if card.collide_point(*touch.pos):
          if card in touch_list:
            # draw a card
            hand_layout.add_widget(deck.deal())
            # remove back cover image if deck is empty
            if len(deck) == 0: deck_layout.remove_widget(back)

      touch_list.clear()
      return False

    # events
    layout.bind(on_touch_up=on_touch_up)
    layout.bind(on_touch_down=on_touch_down)

    return layout

App().run()
