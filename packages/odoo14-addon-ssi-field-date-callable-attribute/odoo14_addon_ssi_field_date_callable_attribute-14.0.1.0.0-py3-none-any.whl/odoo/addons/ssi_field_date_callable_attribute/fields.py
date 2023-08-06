# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging

from odoo import fields

_logger = logging.getLogger(__name__)


class DateCallable(fields.Date):
    def _setup_attrs(self, model, name):
        super()._setup_attrs(model, name)
        readonly_attr = self.readonly
        if self.readonly and callable(readonly_attr):
            self.readonly = readonly_attr(model)

        required_attr = self.required
        if self.required and callable(readonly_attr):
            self.required = required_attr(model)

        string_attr = self.string
        if self.string and callable(string_attr):
            self.string = string_attr(model)

        states_attr = self.states
        if self.states and callable(states_attr):
            self.states = states_attr(model)


fields.DateCallable = DateCallable
