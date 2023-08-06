# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields, models

from odoo.addons.ssi_decorator import ssi_decorator


class TestTransactionMixin(models.Model):
    _inherit = "test.transaction_mixin"

    str_pre_restart_2 = fields.Char(
        string="# Pre Restart 2",
        required=False,
    )
    str_pre_restart_3 = fields.Char(
        string="# Pre Restart 3",
        required=False,
    )
    str_pre_confirm_2 = fields.Char(
        string="# Pre Confirm 2",
        required=False,
    )
    str_pre_confirm_3 = fields.Char(
        string="# Pre Confirm 3",
        required=False,
    )
    str_pre_cancel_2 = fields.Char(
        string="# Pre Cancel 2",
        required=False,
    )
    str_pre_cancel_3 = fields.Char(
        string="# Pre Cancel 3",
        required=False,
    )
    str_pre_open_2 = fields.Char(
        string="# Pre Open 2",
        required=False,
    )
    str_pre_open_3 = fields.Char(
        string="# Pre Open 3",
        required=False,
    )
    str_pre_done_2 = fields.Char(
        string="# Pre Done 2",
        required=False,
    )
    str_pre_done_3 = fields.Char(
        string="# Pre Done 3",
        required=False,
    )
    str_pre_terminate_2 = fields.Char(
        string="# Pre Terminate 2",
        required=False,
    )
    str_pre_terminate_3 = fields.Char(
        string="# Pre Terminate 3",
        required=False,
    )
    str_pre_approve_2 = fields.Char(
        string="# Pre Approve 2",
        required=False,
    )
    str_pre_approve_3 = fields.Char(
        string="# Pre Approve 3",
        required=False,
    )
    str_pre_reject_2 = fields.Char(
        string="# Pre Reject 2",
        required=False,
    )
    str_pre_reject_3 = fields.Char(
        string="# Pre Reject 3",
        required=False,
    )

    @ssi_decorator.pre_restart_action()
    def _set_pre_restart_2(self):
        for record in self:
            record.str_pre_restart_2 = "Pre-Restart 2"

    @ssi_decorator.pre_restart_action()
    def _set_pre_restart(self):
        _super = super(TestTransactionMixin, self)
        _super._set_pre_restart()
        for record in self:
            record.str_pre_restart_3 = "Pre-Restart 3"

    @ssi_decorator.pre_confirm_action()
    def _set_pre_confirm_2(self):
        for record in self:
            record.str_pre_confirm_2 = "Pre-Confirm 2"

    @ssi_decorator.pre_confirm_action()
    def _set_pre_confirm(self):
        _super = super(TestTransactionMixin, self)
        _super._set_pre_confirm()
        for record in self:
            record.str_pre_confirm_3 = "Pre-Confirm 3"

    @ssi_decorator.pre_cancel_action()
    def _pre_cancel_2(self):
        for record in self:
            record.str_pre_cancel_2 = "Pre-Cancel 2"

    @ssi_decorator.pre_cancel_action()
    def _pre_cancel_1(self):
        _super = super(TestTransactionMixin, self)
        _super._pre_cancel_1()
        for record in self:
            record.str_pre_cancel_3 = "Pre-Cancel 3"

    @ssi_decorator.pre_open_action()
    def _pre_open_2(self):
        for record in self:
            record.str_pre_open_2 = "Pre-Open 2"

    @ssi_decorator.pre_open_action()
    def _pre_open_1(self):
        _super = super(TestTransactionMixin, self)
        _super._pre_open_1()
        for record in self:
            record.str_pre_open_3 = "Pre-Open 3"

    @ssi_decorator.pre_done_action()
    def _pre_done_2(self):
        for record in self:
            record.str_pre_done_2 = "Pre-Done 2"

    @ssi_decorator.pre_done_action()
    def _pre_done_1(self):
        _super = super(TestTransactionMixin, self)
        _super._pre_done_1()
        for record in self:
            record.str_pre_done_3 = "Pre-Done 3"

    @ssi_decorator.pre_terminate_action()
    def _pre_terminate_2(self):
        for record in self:
            record.str_pre_terminate_2 = "Pre-Terminate 2"

    @ssi_decorator.pre_terminate_action()
    def _pre_terminate_1(self):
        _super = super(TestTransactionMixin, self)
        _super._pre_terminate_1()
        for record in self:
            record.str_pre_terminate_3 = "Pre-Terminate 3"

    @ssi_decorator.pre_approve_action()
    def _pre_approve_2(self):
        for record in self:
            record.str_pre_approve_2 = "Pre-Approve 2"

    @ssi_decorator.pre_approve_action()
    def _pre_approve_1(self):
        _super = super(TestTransactionMixin, self)
        _super._pre_approve_1()
        for record in self:
            record.str_pre_approve_3 = "Pre-Approve 3"

    @ssi_decorator.pre_reject_action()
    def _pre_reject_2(self):
        for record in self:
            record.str_pre_reject_2 = "Pre-Reject 2"

    @ssi_decorator.pre_reject_action()
    def _pre_reject_1(self):
        _super = super(TestTransactionMixin, self)
        _super._pre_reject_1()
        for record in self:
            record.str_pre_reject_3 = "Pre-Reject 3"
