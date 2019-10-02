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

class App(kivy.app.App):

  def __init__(s):
    super(App, s).__init__()
    s.hand_layout = None
    s.deck_layout = None
    s.deck = None

  def on_touch_up(s, instance, touch):
    # my bug: collision doesn't take into account that the actual image may not cover the entire image widget
    for card in s.hand_layout.children:
      if card.collide_point(*touch.pos):
        print(card)
    for card in s.deck_layout.children:
      if card.collide_point(*touch.pos):
        s.hand_layout.add_widget(s.deck.deal())
    return True

  def build(s):
    s.title = 'App' # workaround to https://github.com/kivy/kivy/pull/6541

    # load cards
    back = kivy.uix.image.Image(source='res/cardBack_green2.png', allow_stretch=True)
    joker_1 = kivy.uix.image.Image(source='res/cardJoker.png', allow_stretch=True)
    joker_2 = kivy.uix.image.Image(source='res/cardJoker.png', allow_stretch=True)
    cards = [joker_1, joker_2]
    files = os.listdir('res/suits')
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
    for card in deck.ndeal(5):
      hand_layout.add_widget(card)
    deck_layout.add_widget(back)

    # events
    layout.bind(on_touch_up=s.on_touch_up)

    # member variable mapping
    s.hand_layout = hand_layout
    s.deck_layout = deck_layout
    s.deck = deck

    return layout

App().run()
