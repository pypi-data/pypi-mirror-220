# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class MixinPartner(models.AbstractModel):
    _name = "mixin.partner"
    _description = "Mixin for Object With Partner"

    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        domain=[
            ("parent_id", "=", False),
        ],
    )

    @api.depends(
        "partner_id",
    )
    def _compute_allowed_contact_ids(self):
        Partner = self.env["res.partner"]
        for record in self:
            result = []
            if record.partner_id:
                criteria = [
                    ("commercial_partner_id", "=", record.partner_id.id),
                    ("id", "!=", record.partner_id.id),
                    ("type", "=", "contact"),
                ]
                result = Partner.search(criteria).ids
            record.allowed_contact_ids = result

    allowed_contact_ids = fields.Many2many(
        string="Allowed Contact",
        comodel_name="res.partner",
        compute="_compute_allowed_contact_ids",
        store=False,
    )
    contact_partner_id = fields.Many2one(
        string="Contact",
        comodel_name="res.partner",
    )

    @api.onchange(
        "partner_id",
    )
    def onchange_contact_partner_id(self):
        self.contact_partner_id = False
