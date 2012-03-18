# -*- coding: utf-8 -*-

from .base import *
from ..skill import *
from ..actions import *

class WearEquipmentAction(UserAction):
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def apply_action(self):
        g = Game.getgame()
        card = self.associated_card
        target = self.target
        equips = target.equips
        for oc in equips:
            if oc.equipment_category == card.equipment_category:
                migrate_cards([oc], g.deck.droppedcards)
                break
        migrate_cards([card], target.equips)
        return True

@register_eh
class EquipmentTransferHandler(EventHandler):
    def handle(self, evt, args):
        if evt == 'card_migration':
            act, cards, _from, to = args
            if _from.type == CardList.EQUIPS:
                for c in cards:
                    _from.owner.skills.remove(c.equipment_skill)

            if to.type == CardList.EQUIPS:
                for c in cards:
                    to.owner.skills.append(c.equipment_skill)

        return args

class OpticalCloakSkill(Skill): # just a tag
    associated_action = None
    target = None

class OpticalCloak(FatetellAction, GenericAction):
    # 光学迷彩
    def __init__(self, target, ori):
        self.target = target
        self.ori_usegraze = ori

    def apply_action(self):
        g = Game.getgame()
        target = self.target
        ft = Fatetell(target, lambda card: card.suit in (Card.HEART, Card.DIAMOND))
        g.process_action(ft)
        if ft.succeeded:
            return True
        else:
            return g.process_action(self.ori_usegraze)

@register_eh
class OpticalCloakHandler(EventHandler):
    def handle(self, evt_type, act):
        from .basic import UseGraze
        if evt_type == 'action_before' and isinstance(act, UseGraze) and not hasattr(act, 'oc_tag'):
            target = act.target
            if target.has_skill(OpticalCloakSkill):
                # TODO: ask for skill invoke
                act.oc_tag = True
                new_act = OpticalCloak(target=target, ori=act)
                return new_act
        return act