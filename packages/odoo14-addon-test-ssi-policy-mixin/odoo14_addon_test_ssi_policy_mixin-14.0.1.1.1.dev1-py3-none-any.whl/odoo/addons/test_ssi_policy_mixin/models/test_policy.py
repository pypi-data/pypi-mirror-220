# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class TestPolicy(models.Model):
    _name = "test.policy"
    _description = "Test Policy"
    _inherit = [
        "mixin.policy",
        "mail.thread",
    ]

    @api.model
    def _get_policy_field(self):
        res = super(TestPolicy, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "open_ok",
            "done_ok",
            "cancel_ok",
            "restart_ok",
        ]
        res += policy_field
        return res

    name = fields.Char(
        string="# Document",
        default="/",
        required=True,
    )
    type_id = fields.Many2one(
        string="Type",
        comodel_name="test.policy.type",
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
        ],
        default="draft",
    )

    def _compute_policy(self):
        _super = super(TestPolicy, self)
        _super._compute_policy()

    # Policy Field
    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
        default=False,
    )
    open_ok = fields.Boolean(
        string="Can Open",
        compute="_compute_policy",
    )
    done_ok = fields.Boolean(
        string="Can Finish",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )

    @api.onchange(
        "type_id",
    )
    def onchange_policy_template_id(self):
        if self.type_id:
            template_id = self._get_template_policy()
            self.policy_template_id = template_id

    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
        }

    def action_confirm(self):
        for document in self:
            document.write(document._prepare_confirm_data())

    def _prepare_open_data(self):
        self.ensure_one()
        return {
            "state": "open",
        }

    def action_open(self):
        for document in self:
            document.write(document._prepare_open_data())

    def _prepare_done_data(self):
        self.ensure_one()
        return {
            "state": "done",
        }

    def action_done(self):
        for document in self:
            document.write(document._prepare_done_data())

    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
        }

    def action_cancel(self):
        for document in self:
            document.write(document._prepare_cancel_data())

    def _prepare_restart_data(self):
        self.ensure_one()
        return {
            "state": "draft",
        }

    def action_restart(self):
        for document in self:
            document.write(document._prepare_restart_data())
