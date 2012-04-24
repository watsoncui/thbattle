# -*- coding: utf-8 -*-
from .baseclasses import *
from ..actions import *
from ..cards import *

class FlowerQueen(Skill):
    associated_action = Attack
    target = t_OtherOne
    distance = 1
    def check(self):
        cl = self.associated_cards
        if not cl or len(cl) != 1: return False
        c = cl[0]
        if not c.suit == Card.CLUB: return False
        return c.resides_in and c.resides_in.type in (
            CardList.HANDCARD, CardList.SHOWNCARD, CardList.EQUIPS,
        )

    def is_card(self, cls):
        if issubclass(AttackCard, cls) or issubclass(GrazeCard, cls): return True
        return isinstance(self, cls)

class MagicCannon(Skill):
    associated_action = None
    target = t_None

class PerfectKill(Skill):
    associated_action = None
    target = t_None
    distance = 1

class YuukaHandler(EventHandler):
    def handle(self, evt_type, act):
        if evt_type == 'action_before' and isinstance(act, Attack):
            c = getattr(act, 'associated_card', None)
            if not c: return act
            src = act.source
            if not src.has_skill(MagicCannon): return act
            if c.suit in (Card.HEART, Card.DIAMOND):
                act.damage += 1
        elif evt_type == 'action_before' and isinstance(act, TryRevive):
            g = Game.getgame()
            dmg = g.action_stack[0]
            assert isinstance(dmg, Damage)
            src = dmg.source
            tgt = dmg.target
            if src != tgt and src.has_skill(PerfectKill):
                act.asklist = [src, dmg.target]
        return act

@register_character
class Yuuka(Character):
    skills = [FlowerQueen, MagicCannon, PerfectKill]
    eventhandlers_required = [YuukaHandler]
    maxlife = 4
