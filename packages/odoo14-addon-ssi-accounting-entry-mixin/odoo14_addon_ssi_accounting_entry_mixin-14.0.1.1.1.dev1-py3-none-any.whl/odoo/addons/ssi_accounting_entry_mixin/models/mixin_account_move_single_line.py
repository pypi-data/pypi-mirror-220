# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class MixinAccountMoveSingleLine(models.AbstractModel):
    _name = "mixin.account_move_single_line"
    _description = "Accounting Move Single Line Mixin"

    _move_id_field_name = "move_id"
    _account_id_field_name = "account_id"
    _partner_id_field_name = False
    _analytic_account_id_field_name = False
    _label_field_name = False
    _currency_id_field_name = "currency_id"
    _company_currency_id_field_name = "company_currency_id"
    _amount_currency_field_name = "amount"
    _company_id_field_name = "company_id"
    _date_field_name = "date"

    _need_date_due = False
    _date_due_field_name = "date_due"

    _normal_amount = "debit"

    def _create_standard_ml(self):
        self.ensure_one()
        ML = self.env["account.move.line"]
        ml = ML.with_context(check_move_validity=False).create(
            self._prepare_standard_ml()
        )
        return ml

    def _prepare_standard_ml(self):
        self.ensure_one()
        debit, credit, amount_currency = self._get_standard_amount()
        partner = self._get_standard_partner()
        aa = self._get_standard_aa()
        move = self._get_standard_move()
        label = self._get_standard_label()
        date_due = self._get_standard_date_due()
        return {
            "move_id": move.id,
            "name": label,
            "account_id": getattr(self, self._account_id_field_name).id,
            "debit": debit,
            "credit": credit,
            "currency_id": getattr(self, self._currency_id_field_name).id,
            "amount_currency": amount_currency,
            "partner_id": partner and partner.id or False,
            "analytic_account_id": aa and aa.id or False,
            "date_maturity": date_due,
        }

    def _get_standard_move(self):
        self.ensure_one()
        move = getattr(self, self._move_id_field_name)
        return move

    def _get_standard_partner(self):
        self.ensure_one()
        result = False
        if self._partner_id_field_name and hasattr(self, self._partner_id_field_name):
            result = getattr(self, self._partner_id_field_name)
        return result

    def _get_standard_label(self):
        self.ensure_one()
        result = False
        if self._label_field_name and hasattr(self, self._label_field_name):
            result = getattr(self, self._label_field_name)
        return result

    def _get_standard_date_due(self):
        self.ensure_one()
        result = False

        if not self._need_date_due:
            return result

        if self._date_due_field_name and hasattr(self, self._date_due_field_name):
            result = getattr(self, self._date_due_field_name)

        if self._need_date_due and not result:
            result = getattr(self, self._accounting_date_field_name)
        return result

    def _get_standard_aa(self):
        self.ensure_one()
        result = False
        if self._analytic_account_id_field_name and hasattr(
            self, self._analytic_account_id_field_name
        ):
            result = getattr(self, self._analytic_account_id_field_name)
        return result

    def _get_standard_amount(self):
        self.ensure_one()
        debit = credit = amount = 0.0
        amount_currency = getattr(self, self._amount_currency_field_name)
        currency = getattr(self, self._currency_id_field_name)
        company_currency = getattr(self, self._company_currency_id_field_name)
        getattr(self, self._company_id_field_name)
        getattr(self, self._date_field_name)

        amount = currency.compute(
            abs(amount_currency),
            company_currency,
        )

        if self._normal_amount == "debit" and amount_currency > 0:
            debit = amount
        elif self._normal_amount == "debit" and amount_currency < 0:
            credit = amount
        elif self._normal_amount == "credit" and amount_currency > 0:
            credit = amount
            amount_currency *= -1
        elif self._normal_amount == "credit" and amount_currency < 0:
            debit = amount
            amount_currency *= -1

        return debit, credit, amount_currency
