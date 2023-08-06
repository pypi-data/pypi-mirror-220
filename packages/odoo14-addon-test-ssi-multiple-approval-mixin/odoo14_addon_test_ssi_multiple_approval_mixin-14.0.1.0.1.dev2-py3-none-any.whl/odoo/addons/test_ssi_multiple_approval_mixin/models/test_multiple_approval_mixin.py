# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class TestMultipleApprovalMixin(models.Model):
    _name = "test.multiple_approval_mixin"
    _description = "Test Multiple Approval Mixin"
    _inherit = [
        "mixin.multiple_approval",
        "mail.thread",
    ]
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"

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
            document.action_request_approval()

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

    def action_approve_approval(self):
        _super = super(TestMultipleApprovalMixin, self)
        _super.action_approve_approval()
        for document in self:
            if document.approved:
                document.action_open()
