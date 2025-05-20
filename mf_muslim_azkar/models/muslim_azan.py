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
from datetime import date, timedelta
DEFAULT_MESSAGE = "Default message"
INFO = "info"
DEFAULT = "default"
import random
import pytz


class MuslimAzan(models.Model):
    _name = 'muslim.azan'
    _description = 'Muslim Salah Reminder'


    name = fields.Selection(
        string='Name',
        selection=[('1', 'صلاة الفجر'), ('2', 'صلاة الظهر'), ('3', 'صلاة العصر'), ('4', 'صلاة المغرب'), ('5', 'صلاة العشاء')],
        required=True, )
    zikr = fields.Text(required=True, string='Zikr',default='حان الآن موعد الصلاة')
    azan_time = fields.Float(string='Salah Time', required=True)
    all_users = fields.Boolean(string='All users', required=False,default=True)
    user_ids = fields.Many2many(comodel_name='res.users',string='Users')


    def send_notification(self):
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        selection_dict = dict(self._fields['name'].selection)
        # Get the value (e.g., "صلاة الفجر") from the selection dictionary
        salah_name = selection_dict.get(self.name, self.name)
        target = self.env['res.users'].search([]).mapped('partner_id') if self.all_users else self.user_ids.mapped('partner_id')
        self._notify_channel(DEFAULT, self.zikr, salah_name, sticky=False, target=target , id=None)


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
            target = self.user_ids.mapped('partner_id')
            if not target:
                return

        bus_message = {
            "type": type_message,
            "message": message,
            "title": title,
            "sticky": sticky,
            "id": id,
        }
        notifications = [[partner, "muslim.azan", [bus_message]] for partner in target]
        print(notifications,'NNNNNNNNNNNNNNN')
        self.env["bus.bus"]._sendmany(notifications)

    def cron_for_salah_reminder(self):
        # Get the Cairo timezone from the company's configuration
        cairo_tz = pytz.timezone(self.env.user.company_id.partner_id.tz or 'Africa/Cairo')

        # Get the current UTC time and convert it to Cairo time
        now_utc = fields.Datetime.now()
        now_cairo = pytz.utc.localize(now_utc).astimezone(cairo_tz)

        # Convert Cairo time to float (hours)
        current_time_float = now_cairo.hour + (now_cairo.minute / 60)

        # Calculate the range for 10 minutes before and after
        lower_bound = current_time_float - (10 / 60)  # 10 minutes before
        upper_bound = current_time_float + (10 / 60)  # 10 minutes after

        # Search for the current salah in the time range
        current_salah = self.search([
            ('azan_time', '>=', lower_bound),
            ('azan_time', '<=', upper_bound)
        ], order='azan_time', limit=1)
        if current_salah:
            # Notify users for the current salah
            current_salah.send_notification()

            # Determine the next salah
            next_salah_number = int(current_salah.name) + 1 if int(current_salah.name) < 5 else 1
            next_salah = self.search([('name', '=', str(next_salah_number))], limit=1)

            if next_salah:
                next_salah_time = next_salah.azan_time
                # Calculate the datetime for the next azan based on today's Cairo time
                next_trigger_time = now_cairo.replace(hour=int(next_salah_time),
                                                      minute=int((next_salah_time % 1) * 60),
                                                      second=0, microsecond=0)
                # If the next salah is earlier than now (e.g., Fajr after Isha), set it for tomorrow
                if next_trigger_time <= now_cairo:
                    next_trigger_time += timedelta(days=1)

                # Convert the trigger time back to UTC for cron scheduling
                next_trigger_time_utc = next_trigger_time.astimezone(pytz.utc).replace(tzinfo=None)
                # Update the cron trigger time
                self.env.ref('mf_muslim_azkar.azan_cron')._trigger(at=next_trigger_time_utc)

#we don't need to update the cron nextcall because it's being running
# because of it's forbidden to update it while executing
                # self.env.ref('mf_muslim_azkar.azan_cron').nextcall = next_trigger_time_utc

        return True