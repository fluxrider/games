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

  def on_touch_up(s, instance, touch):
    # TODO: collision doesn't take into account that the actual image may not cover the entire image widget
    # TODO: touch_down/up match

    # card
    for card in s.hand_layout.children:
      if card.collide_point(*touch.pos):
        print(card)

    # deck
    for card in s.deck_layout.children:
      if card.collide_point(*touch.pos):
        s.hand_layout.add_widget(s.deck.deal())
        if len(s.deck) == 0:
          s.deck_layout.remove_widget(s.back)
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

    # layout and sync presentation
    layout = kivy.uix.boxlayout.BoxLayout(padding=5, spacing=5, orientation='vertical')
    deck_layout = kivy.uix.boxlayout.BoxLayout(spacing=5)
    hand_layout = kivy.uix.boxlayout.BoxLayout(spacing=5)
    layout.add_widget(deck_layout)
    layout.add_widget(hand_layout)
    deck_layout.add_widget(back)

    # events
    layout.bind(on_touch_up=s.on_touch_up)

    # member variable mapping
    s.hand_layout = hand_layout
    s.deck_layout = deck_layout
    s.deck = deck
    s.back = back

    return layout

App().run()
