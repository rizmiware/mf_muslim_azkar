# -*- coding: utf-8 -*-
##############################################################################
#    Copyright (C) 2024.
#    Author: Eng.Mohamed Fouad (<m.fouad@mfhm95.com>)
#    website: https://rizmiware.com
#    linkedin: https://www.linkedin.com/in/mfhm95
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

{
    'name': "Hisn Al-Muslim",

    'summary': """
        Muslim Fortress is a module to display Muslim Azkar and Salah reminders on the top right corner of the screen.
    
    """,

    'description': """

        Muslim Azkar is a module to display Muslim Azkar and Salah reminders on the top right corner of the screen.
            It is a simple module that displays a notification with a message and a sound to remind the user of the Azkar and Salah times.""",

    'author': "Mohamed Fouad",
    'website': "https://rizmiware.com",
    'images': ['static/description/icon.png'],

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','bus','web','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/ir_cron.xml',
        'views/muslim_azkar_view.xml',
        'views/muslim_azan_view.xml',
    ],
    'assets': {
        'web.assets_backend':
            ['mf_muslim_azkar/static/src/js/*.js']
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'AGPL-3',
    'application': True,

}

