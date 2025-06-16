# -*- coding: utf-8 -*-
##############################################################################
#    Copyright (C) 2024.
#    Author: Eng.Mohamed Fouad (<m.fouad@mfhm95.com>)
#    website: https://rizmiware.com
#    linkedin: https://www.linkedin.com/in/mfhm95
#
# This contribution is considered a form of "Zakat al-Ilm" (charity through knowledge),
# which is highly encouraged in Islam.
# We welcome and appreciate your contributions and suggestions for improving this project.
# Feel free to report issues or propose improvements,
# as this is a charity-focused initiative aimed at benefiting the community.
##############################################################################
from docutils.nodes import target

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError
DEFAULT_MESSAGE = "Default message"
INFO = "info"
DEFAULT = "default"
import random


class MuslimAzkar(models.Model):
    _name = 'muslim.azkar'
    _description = 'Muslim Azkar'

    name = fields.Char(required=True)
    zikr = fields.Text(required=True)
    from_time = fields.Float(
        string='From time',
        required=False)
    to_time = fields.Float(
        string='To time',
        required=False)
    all_users = fields.Boolean(string='All users', required=False)
    user_ids = fields.Many2many(comodel_name='res.users',string='Users')

    def _send_notification(self):
        target = self.env['res.users'].search([]).mapped('partner_id') if self.all_users else self.user_ids.mapped('partner_id')
        self._notify_channel(DEFAULT, self.zikr, self.name, sticky=False, target=target , id=None)


    def _notify_channel(
            self,
            type_message=DEFAULT,
            message=DEFAULT_MESSAGE,
            title=None,
            sticky=False,
            target=None,
            id=None,
    ):
        if not target:
            target = self.env['res.users'].search([]).mapped('partner_id')
            if not target:
                return

        bus_message = {
            "type": type_message,
            "message": message,
            "title": title,
            "sticky": sticky,
            "id": id,
        }
        notifications = [[partner, "muslim.azkar", [bus_message]] for partner in target]
        self.env["bus.bus"]._sendmany(notifications)


    def random_zikr_for_cron(self):
        zikr = self.env['muslim.azkar'].search([])
        zikr = zikr[random.randint(0, len(zikr) - 1)]
        zikr._send_notification()
        return True