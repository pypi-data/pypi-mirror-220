# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class TestTransactionMixin(models.Model):
    _name = "test.transaction_mixin"
    _description = "Test Transaction Mixin"
    _inherit = [
        "mixin.transaction_confirm",
        "mixin.transaction_open",
        "mixin.transaction_done",
        "mixin.transaction_cancel",
        "mixin.transaction_terminate",
        "mixin.company_currency",
    ]

    # Multiple Approval Attribute
    _approval_from_state = "draft"
    _approval_to_state = "open"
    _approval_state = "confirm"
    _after_approved_method = "action_open"

    # Attributes related to add element on view automatically
    _automatically_insert_view_element = True

    # Attributes related to add element on form view automatically
    _automatically_insert_multiple_approval_page = True
    _statusbar_visible_label = "draft,confirm,open,done"
    _policy_field_order = [
        "confirm_ok",
        "approve_ok",
        "reject_ok",
        "restart_approval_ok",
        "cancel_ok",
        "terminate_ok",
        "restart_ok",
        "open_ok",
        "done_ok",
        "manual_number_ok",
    ]
    _header_button_order = [
        "action_confirm",
        "action_approve_approval",
        "action_reject_approval",
        "action_done",
        "%(ssi_transaction_cancel_mixin.base_select_cancel_reason_action)d",
        "%(ssi_transaction_terminate_mixin.base_select_terminate_reason_action)d",
        "action_restart",
    ]

    # Attributes related to add element on search view automatically
    _state_filter_order = [
        "dom_draft",
        "dom_confirm",
        "dom_reject",
        "dom_open",
        "dom_done",
        "dom_cancel",
        "dom_terminate",
    ]

    # Sequence attribute
    _create_sequence_state = "open"

    @api.model
    def _get_policy_field(self):
        res = super(TestTransactionMixin, self)._get_policy_field()
        policy_field = [
            "confirm_ok",
            "approve_ok",
            "done_ok",
            "open_ok",
            "cancel_ok",
            "terminate_ok",
            "reject_ok",
            "restart_ok",
            "restart_approval_ok",
            "manual_number_ok",
        ]
        res += policy_field
        return res

    date = fields.Date(
        string="Date",
        readonly=True,
        states={"draft": [("readonly", False)]},
        copy=False,
    )
    chk_pre_restart = fields.Boolean(
        string="# Pre Restart",
        required=False,
    )
    str_pre_restart = fields.Char(
        string="# Pre Restart",
        required=False,
    )
    chk_post_restart = fields.Boolean(
        string="# Post Restart",
        required=False,
    )
    str_post_restart = fields.Char(
        string="# Post Restart",
        required=False,
    )
    chk_pre_confirm = fields.Boolean(
        string="# Pre Confirm",
        required=False,
    )
    str_pre_confirm = fields.Char(
        string="# Pre Confirm",
        required=False,
    )
    chk_post_confirm = fields.Boolean(
        string="# Post Confirm",
        required=False,
    )
    str_post_confirm = fields.Char(
        string="# Post Confirm",
        required=False,
    )
    chk_pre_cancel = fields.Boolean(
        string="# Pre Cancel",
        required=False,
    )
    str_pre_cancel = fields.Char(
        string="# Pre Cancel",
        required=False,
    )
    chk_post_cancel = fields.Boolean(
        string="# Post Cancel",
        required=False,
    )
    str_post_cancel = fields.Char(
        string="# Post Cancel",
        required=False,
    )
    chk_pre_open = fields.Boolean(
        string="# Pre Open",
        required=False,
    )
    str_pre_open = fields.Char(
        string="# Pre Open",
        required=False,
    )
    chk_post_open = fields.Boolean(
        string="# Post Open",
        required=False,
    )
    str_post_open = fields.Char(
        string="# Post Open",
        required=False,
    )
    chk_pre_done = fields.Boolean(
        string="# Pre Done",
        required=False,
    )
    str_pre_done = fields.Char(
        string="# Pre Done",
        required=False,
    )
    chk_post_done = fields.Boolean(
        string="# Post Done",
        required=False,
    )
    str_post_done = fields.Char(
        string="# Post Done",
        required=False,
    )
    chk_pre_terminate = fields.Boolean(
        string="# Pre Terminate",
        required=False,
    )
    str_pre_terminate = fields.Char(
        string="# Pre Terminate",
        required=False,
    )
    chk_post_terminate = fields.Boolean(
        string="# Post Terminate",
        required=False,
    )
    str_post_terminate = fields.Char(
        string="# Post Terminate",
        required=False,
    )
    chk_pre_approve = fields.Boolean(
        string="# Pre Approve",
        required=False,
    )
    str_pre_approve = fields.Char(
        string="# Pre Approve",
        required=False,
    )
    chk_post_approve = fields.Boolean(
        string="# Post Approve",
        required=False,
    )
    str_post_approve = fields.Char(
        string="# Post Approve",
        required=False,
    )
    chk_pre_reject = fields.Boolean(
        string="# Pre Reject",
        required=False,
    )
    str_pre_reject = fields.Char(
        string="# Pre Reject",
        required=False,
    )
    chk_post_reject = fields.Boolean(
        string="# Post Reject",
        required=False,
    )
    str_post_reject = fields.Char(
        string="# Post Reject",
        required=False,
    )
    detail_ids = fields.One2many(
        string="Details",
        comodel_name="test.transaction_detail_mixin",
        inverse_name="test_transaction_id",
        readonly=True,
        states={
            "draft": [
                ("readonly", False),
            ],
        },
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("draft", "Draft"),
            ("confirm", "Waiting for Approval"),
            ("open", "In Progress"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
            ("reject", "Rejected"),
            ("terminate", "Terminate"),
        ],
        default="draft",
        copy=False,
    )

    # CHECK
    @ssi_decorator.pre_restart_check()
    def _set_pre_restart_check(self):
        for record in self:
            record.chk_pre_restart = True

    @ssi_decorator.post_restart_check()
    def _set_post_restart_check(self):
        for record in self:
            record.chk_post_restart = True

    @ssi_decorator.pre_confirm_check()
    def _set_pre_confirm_check(self):
        for record in self:
            record.chk_pre_confirm = True

    @ssi_decorator.post_confirm_check()
    def _set_post_confirm_check(self):
        for record in self:
            record.chk_post_confirm = True

    @ssi_decorator.pre_cancel_check()
    def _pre_cancel_check(self):
        for record in self:
            record.chk_pre_cancel = True

    @ssi_decorator.post_cancel_check()
    def _post_cancel_check(self):
        for record in self:
            record.chk_post_cancel = True

    @ssi_decorator.pre_open_check()
    def _pre_open_check(self):
        for record in self:
            record.chk_pre_open = True

    @ssi_decorator.post_open_check()
    def _post_open_check(self):
        for record in self:
            record.chk_post_open = True

    @ssi_decorator.pre_done_check()
    def _pre_done_check(self):
        for record in self:
            record.chk_pre_done = True

    @ssi_decorator.post_done_check()
    def _post_done_check(self):
        for record in self:
            record.chk_post_done = True

    @ssi_decorator.pre_terminate_check()
    def _pre_terminate_check(self):
        for record in self:
            record.chk_pre_terminate = True

    @ssi_decorator.post_terminate_check()
    def _post_terminate_check(self):
        for record in self:
            record.chk_post_terminate = True

    @ssi_decorator.pre_approve_check()
    def _pre_approve_check(self):
        for record in self:
            record.chk_pre_approve = True

    @ssi_decorator.post_approve_check()
    def _post_approve_check(self):
        for record in self:
            record.chk_post_approve = True

    @ssi_decorator.pre_reject_check()
    def _pre_reject_check(self):
        for record in self:
            record.chk_pre_reject = True

    @ssi_decorator.post_reject_check()
    def _post_reject_check(self):
        for record in self:
            record.chk_post_reject = True

    # ACTION
    @ssi_decorator.pre_restart_action()
    def _set_pre_restart(self):
        for record in self:
            record.str_pre_restart = "Pre-Restart"

    @ssi_decorator.post_restart_action()
    def _set_post_restart(self):
        for record in self:
            record.str_post_restart = "Post-Restart"

    @ssi_decorator.pre_confirm_action()
    def _set_pre_confirm(self):
        for record in self:
            record.str_pre_confirm = "Pre-Confirm"

    @ssi_decorator.post_confirm_action()
    def _set_post_confirm(self):
        for record in self:
            record.str_post_confirm = "Post-Confirm"

    @ssi_decorator.pre_cancel_action()
    def _pre_cancel_1(self):
        for record in self:
            record.str_pre_cancel = "Pre-Cancel"

    @ssi_decorator.post_cancel_action()
    def _post_cancel_1(self):
        for record in self:
            record.str_post_cancel = "Post-Cancel"

    @ssi_decorator.pre_open_action()
    def _pre_open_1(self):
        for record in self:
            record.str_pre_open = "Pre-Open"

    @ssi_decorator.post_open_action()
    def _post_open_1(self):
        for record in self:
            record.str_post_open = "Post-Open"

    @ssi_decorator.pre_done_action()
    def _pre_done_1(self):
        for record in self:
            record.str_pre_done = "Pre-Done"

    @ssi_decorator.post_done_action()
    def _post_done_1(self):
        for record in self:
            record.str_post_done = "Post-Done"

    @ssi_decorator.pre_terminate_action()
    def _pre_terminate_1(self):
        for record in self:
            record.str_pre_terminate = "Pre-Terminate"

    @ssi_decorator.post_terminate_action()
    def _post_terminate_1(self):
        for record in self:
            record.str_post_terminate = "Post-Terminate"

    @ssi_decorator.pre_approve_action()
    def _pre_approve_1(self):
        for record in self:
            record.str_pre_approve = "Pre-Approve"

    @ssi_decorator.post_approve_action()
    def _post_approve_1(self):
        for record in self:
            record.str_post_approve = "Post-Approve"

    @ssi_decorator.pre_reject_action()
    def _pre_reject_1(self):
        for record in self:
            record.str_pre_reject = "Pre-Reject"

    @ssi_decorator.post_reject_action()
    def _post_reject_1(self):
        for record in self:
            record.str_post_reject = "Post-Reject"
