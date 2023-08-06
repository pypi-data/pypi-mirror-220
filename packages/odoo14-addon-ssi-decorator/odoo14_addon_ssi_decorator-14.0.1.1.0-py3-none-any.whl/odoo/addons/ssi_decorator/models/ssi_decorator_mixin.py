# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import models


class MixinDecorator(models.AbstractModel):
    _name = "mixin.decorator"
    _description = "SSI Decorator Mixin"

    def is_decorator(self, func, decorator):
        self.ensure_one()
        return callable(func) and hasattr(func, decorator)

    def run_decorator_method(self, methods):
        self.ensure_one()
        for method_name in methods:
            getattr(self, method_name.__name__)()
