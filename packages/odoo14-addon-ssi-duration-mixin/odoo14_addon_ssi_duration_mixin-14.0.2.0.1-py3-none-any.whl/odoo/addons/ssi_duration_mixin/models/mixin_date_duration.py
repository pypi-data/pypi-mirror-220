# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class MixinDateDuration(models.AbstractModel):
    _name = "mixin.date_duration"
    _description = "Date Duration Mixin"
    _date_start_required = True
    _date_end_required = True
    _date_start_readonly = False
    _date_end_readonly = False
    _date_start_string = "Date Start"
    _date_end_string = "Date End"
    _date_start_states_list = []
    _date_start_states_required = []
    _date_start_states_readonly = []
    _date_end_states_list = []
    _date_end_states_required = []
    _date_end_states_readonly = []

    @api.model
    def _get_date_start_required(self):
        return self._date_start_required

    @api.model
    def _get_date_start_readonly(self):
        return self._date_start_readonly

    @api.model
    def _get_date_end_required(self):
        return self._date_end_required

    @api.model
    def _get_date_end_readonly(self):
        return self._date_end_readonly

    @api.model
    def _get_date_start_string(self):
        return self._date_start_string

    @api.model
    def _get_date_end_string(self):
        return self._date_end_string

    @api.model
    def _get_date_start_state(self):
        result = {}
        if self._date_start_states_list:
            for state in self._date_start_states_list:
                result.update({state: []})

            if self._date_start_states_required:
                for state in self._date_start_states_required:
                    result[state].append(("required", not self._date_start_required))

            if self._date_start_states_readonly:
                for state in self._date_start_states_readonly:
                    result[state].append(("readonly", not self._date_start_readonly))
        return result

    @api.model
    def _get_date_end_state(self):
        result = {}
        if self._date_end_states_list:
            for state in self._date_end_states_list:
                result.update({state: []})

            if self._date_end_states_required:
                for state in self._date_end_states_required:
                    result[state].append(("required", not self._date_end_required))

            if self._date_end_states_readonly:
                for state in self._date_end_states_readonly:
                    result[state].append(("readonly", not self._date_end_readonly))
        return result

    date_start = fields.DateCallable(
        string=_get_date_start_string,
        required=_get_date_start_required,
        readonly=_get_date_start_readonly,
        states=_get_date_start_state,
    )
    date_end = fields.DateCallable(
        string=_get_date_end_string,
        required=_get_date_end_required,
        readonly=_get_date_end_readonly,
        states=_get_date_end_state,
    )

    @api.constrains("date_start", "date_end")
    def _check_date_start_end(self):
        for record in self:
            if record.date_start and record.date_end:
                strWarning = _("Date end must be greater than date start")
                if record.date_end < record.date_start:
                    raise UserError(strWarning)
