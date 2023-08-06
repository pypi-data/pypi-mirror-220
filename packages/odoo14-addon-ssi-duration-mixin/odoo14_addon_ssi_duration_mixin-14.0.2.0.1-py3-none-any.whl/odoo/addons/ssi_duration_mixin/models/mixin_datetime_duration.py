# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class MixinDatetimeDuration(models.AbstractModel):
    _name = "mixin.datetime_duration"
    _description = "Datetime Duration Mixin"

    date_start = fields.Datetime(
        string="Date Start",
    )
    date_end = fields.Datetime(
        string="Date End",
    )
