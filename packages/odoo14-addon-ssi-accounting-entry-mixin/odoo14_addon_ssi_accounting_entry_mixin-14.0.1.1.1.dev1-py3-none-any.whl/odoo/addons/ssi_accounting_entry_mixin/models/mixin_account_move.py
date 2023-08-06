# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models


class MixinAccountMove(models.AbstractModel):
    _name = "mixin.account_move"
    _description = "Accounting Entry Header Mixin"
    _journal_id_field_name = "journal_id"
    _move_id_field_name = "move_id"
    _accounting_date_field_name = "date"
    _currency_id_field_name = "currency_id"
    _company_currency_id_field_name = "company_currency_id"

    # Tax computation
    _tax_lines_field_name = False
    _tax_on_self = False
    _tax_source_recordset_field_name = False
    _price_unit_field_name = False
    _quantity_field_name = False

    def _create_standard_move(self):
        self.ensure_one()
        Move = self.env["account.move"]
        move = Move.with_context(check_move_validity=False).create(
            self._prepare_standard_move()
        )
        self.write(
            {
                self._move_id_field_name: move.id,
            }
        )

    def _post_standard_move(self):
        self.ensure_one()
        move = getattr(self, self._move_id_field_name)
        move.action_post()

    def _prepare_standard_move(self):
        self.ensure_one()
        return {
            "name": self.name,
            "journal_id": getattr(self, self._journal_id_field_name).id,
            "date": getattr(self, self._accounting_date_field_name),
        }

    def _delete_standard_move(self):
        self.ensure_one()
        Move = self.env["account.move"]
        move = Move.with_context(check_move_validity=False).create(
            self._prepare_standard_move()
        )
        self.write(
            {
                self._move_id_field_name: move.id,
            }
        )

        move = getattr(self, self._move_id_field_name)

        if not move:
            return True

        self.write(
            {
                self._move_id_field_name: False,
            }
        )

        move.unlink()

    def _get_standard_tax_lines(self):
        self.ensure_one()
        result = False
        if self._tax_lines_field_name and hasattr(self, self._tax_lines_field_name):
            result = getattr(self, self._tax_lines_field_name)
        return result

    def _recompute_standard_tax(self):
        self.ensure_one()

        tax_lines = self._get_standard_tax_lines()

        taxes_grouped = self._get_standard_tax_values()

        tax_lines.unlink()
        list_tax = []
        for tax in taxes_grouped.values():
            list_tax.append((0, 0, tax))
        self.write({"tax_ids": list_tax})

    def _get_standard_tax_values(self):
        self.ensure_one()
        tax_grouped = {}

        if self._tax_on_self:
            tax_grouped = self._get_standard_tax_on_self()
        else:
            tax_grouped = self._get_standard_tax_on_recordset()
        return tax_grouped

    def _get_standard_tax_on_recordset(self):
        self.ensure_one()
        cur = getattr(self, self._currency_id_field_name)
        round_curr = cur.round
        recordset = getattr(self, self._tax_source_recordset_field_name)
        tax_grouped = {}
        for record in recordset:
            price_unit = getattr(record, self._price_unit_field_name)
            if self._quantity_field_name and hasattr(record, self._quantity_field_name):
                quantity = getattr(record, self._quantity_field_name)
            else:
                quantity = 1.0
            taxes = record.tax_ids.compute_all(price_unit, cur, quantity)["taxes"]
            for tax in taxes:
                val = self._prepare_standard_tax_line_values(record, tax)
                key = self._get_standard_tax_grouping_key(val)

                if key not in tax_grouped:
                    tax_grouped[key] = val
                    tax_grouped[key]["base_amount"] = round_curr(val["base_amount"])
                else:
                    tax_grouped[key]["tax_amount"] += val["tax_amount"]
                    tax_grouped[key]["base_amount"] += round_curr(val["base_amount"])
        return tax_grouped

    def _get_standard_tax_grouping_key(self, tax_line):
        self.ensure_one()
        return (
            str(tax_line["tax_id"])
            + "-"
            + str(tax_line["account_id"])
            + "-"
            + str(tax_line["analytic_account_id"])
        )

    def _prepare_standard_tax_line_values(self, record, tax):
        self.ensure_one()
        vals = {
            "name": tax["name"],
            "tax_id": tax["id"],
            "tax_amount": tax["amount"],
            "base_amount": tax["base"],
            "manual": False,
            "account_id": tax["account_id"],
            "analytic_account_id": record.analytic_account_id.id,
        }
        return vals
