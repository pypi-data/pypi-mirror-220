# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models


class TestRelatedAttachment(models.Model):
    _name = "test.related_attachment"
    _description = "Test Related Attachment"
    _inherit = [
        "mixin.related_attachment",
        "mail.thread",
    ]

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
    )
    date = fields.Date(
        string="Date",
        index=True,
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=False,
        default=fields.Date.context_today,
    )
    user_id = fields.Many2one(
        string="Users",
        comodel_name="res.users",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    notes = fields.Text(
        string="Notes",
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "On Progress"),
            ("done", "Finished"),
            ("cancel", "Cancelled"),
            ("terminate", "Terminated"),
            ("reject", "Rejected"),
        ],
        default="draft",
    )

    def action_confirm(self):
        for document in self:
            document.write({"state": "confirm"})

    def action_open(self):
        for document in self:
            document.write({"state": "open"})

    def action_done(self):
        for document in self:
            document.write({"state": "done"})

    def action_cancel(self):
        for document in self:
            document.write({"state": "cancel"})

    def action_restart(self):
        for document in self:
            document.write({"state": "draft"})

    @api.onchange(
        "user_id",
    )
    def _onchange_related_attachment_template_id(self):
        self.related_attachment_template_id = False
        if self.user_id:
            template_id = self._get_template_related_attachment()
            self.related_attachment_template_id = template_id
