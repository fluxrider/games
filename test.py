#!/usr/bin/env python

import os

os.environ["KIVY_NO_ENV_CONFIG"] = "1" # TMP workaround until https://github.com/kivy/kivy/pull/6540
os.environ["KCFG_KIVY_LOG_LEVEL"] = "warning"

# kivy is sadly an import intensive library
import kivy
import kivy.app
import kivy.uix.boxlayout
import kivy.uix.image
import deck as games

# TODO app icon
class App(kivy.app.App):

  def __init__(s):
    super(App, s).__init__()
    s.hand_layout = None
    s.deck_layout = None
    s.deck = None
    s.back = None
    s.touch_list = []

  def on_touch_down(s, w, touch):
    widgets = s.hand_layout.children + s.deck_layout.children
    for widget in widgets:
      if widget.collide_point(*touch.pos):
        s.touch_list.append(widget)
    return True

  def on_touch_up(s, w, touch):
    # TODO: collision doesn't take into account that the actual image may not cover the entire image widget

    # card
    for card in s.hand_layout.children[:]:
      if card.collide_point(*touch.pos):
        if card in s.touch_list:
          # remove card from hand
          s.hand_layout.remove_widget(card)
          # show the back cover image if deck will not be empty anymore
          if len(s.deck) == 0: s.deck_layout.add_widget(s.back)
          # place it on the deck
          s.deck.place_top(card)

    # deck
    for card in s.deck_layout.children:
      if card.collide_point(*touch.pos):
        if card in s.touch_list:
          # draw a card
          s.hand_layout.add_widget(s.deck.deal())
          # remove back cover image if deck is empty
          if len(s.deck) == 0: s.deck_layout.remove_widget(s.back)

    s.touch_list = []
    return True

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
    layout.add_widget(deck_layout)
    layout.add_widget(hand_layout)

    # sync presentation
    if len(deck) > 0: deck_layout.add_widget(back)

    # events
    layout.bind(on_touch_up=s.on_touch_up)
    layout.bind(on_touch_down=s.on_touch_down)

    # member variable mapping
    s.hand_layout = hand_layout
    s.deck_layout = deck_layout
    s.deck = deck
    s.back = back

    return layout

App().run()
