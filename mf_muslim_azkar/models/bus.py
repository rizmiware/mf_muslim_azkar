import datetime
import json
import logging
import odoo
from odoo import api, fields, models
from odoo.service.server import CommonServer
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools import json_default, SQL,date_utils
_logger = logging.getLogger(__name__)

# longpolling timeout connection
TIMEOUT = 50

#----------------------------------------------------------
# Bus
#----------------------------------------------------------
def json_dump(v):
    return json.dumps(v, separators=(',', ':'), default=json_default)

def hashable(key):
    if isinstance(key, list):
        key = tuple(key)
    return key


def channel_with_db(dbname, channel):
    if isinstance(channel, models.Model):
        return (dbname, channel._name, channel.id)
    if isinstance(channel, str):
        return (dbname, channel)
    return channel


class ImBus(models.Model):

    _inherit = 'bus.bus'


    @api.model
    def _sendmany(self, notifications):
        for notification in notifications:
            self._sendone(*notification)

    @api.model
    def _sendone(self, target, notification_type, message):
        self._ensure_hooks()
        channel = channel_with_db(self.env.cr.dbname, target)
        self.env.cr.precommit.data["bus.bus.values"].append(
            {
                "channel": json_dump(channel),
                "message": json_dump(
                    {
                        "type": notification_type,
                        "payload": message,
                    }
                ),
            }
        )
        self.env.cr.postcommit.data["bus.bus.channels"].add(channel)
