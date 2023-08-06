# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo import api, fields, models


class MixinTransactionReady(models.AbstractModel):
    _name = "mixin.transaction_ready"
    _inherit = [
        "mixin.transaction",
    ]
    _description = "Transaction Mixin - Ready to Start State Mixin"
    _ready_state = "ready"

    # Attributes related to add element on form view automatically
    _automatically_insert_ready_policy_fields = True
    _automatically_insert_ready_button = True

    # Attributes related to add element on search view automatically
    _automatically_insert_ready_filter = True

    # Attributes related to add element on tree view automatically
    _automatically_insert_ready_state_badge_decorator = True

    def _compute_policy(self):
        _super = super(MixinTransactionReady, self)
        _super._compute_policy()

    ready_ok = fields.Boolean(
        string="Can Stagged",
        compute="_compute_policy",
        compute_sudo=True,
    )

    def _prepare_ready_data(self):
        self.ensure_one()
        result = {
            "state": self._ready_state,
        }
        if self._create_sequence_state == self._ready_state:
            self._create_sequence()
        return result

    def action_ready(self):
        for record in self.sudo():
            record.write(record._prepare_ready_data())

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        result = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        View = self.env["ir.ui.view"]

        view_arch = etree.XML(result["arch"])
        if view_type == "form" and self._automatically_insert_view_element:
            view_arch = self._view_add_ready_policy_field(view_arch)
            view_arch = self._view_add_ready_button(view_arch)
            view_arch = self._reorder_header_button(view_arch)
            view_arch = self._reorder_policy_field(view_arch)
        elif view_type == "tree" and self._automatically_insert_view_element:
            view_arch = self._add_ready_state_badge_decorator(view_arch)
        elif view_type == "search" and self._automatically_insert_view_element:
            view_arch = self._add_ready_filter_on_search_view(view_arch)
            view_arch = self._reorder_state_filter_on_search_view(view_arch)

        if view_id and result.get("base_model", self._name) != self._name:
            View = View.with_context(base_model_name=result["base_model"])
        new_arch, new_fields = View.postprocess_and_fields(view_arch, self._name)
        result["arch"] = new_arch
        new_fields.update(result["fields"])
        result["fields"] = new_fields

        return result

    @api.model
    def _add_ready_state_badge_decorator(self, view_arch):
        if self._automatically_insert_ready_state_badge_decorator:
            _xpath = "/tree/field[@name='state']"
            if len(view_arch.xpath(_xpath)) == 0:
                return view_arch
            node_xpath = view_arch.xpath(_xpath)[0]
            node_xpath.set("decoration-primary", "state == 'ready'")
        return view_arch

    @api.model
    def _add_ready_filter_on_search_view(self, view_arch):
        if self._automatically_insert_ready_filter:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_ready_mixin.ready_filter",
                self._state_filter_xpath,
                "after",
            )
        return view_arch

    @api.model
    def _view_add_ready_policy_field(self, view_arch):
        if self._automatically_insert_ready_policy_fields:
            policy_element_templates = [
                "ssi_transaction_ready_mixin.ready_policy_field",
            ]
            for template in policy_element_templates:
                view_arch = self._add_view_element(
                    view_arch,
                    template,
                    self._policy_field_xpath,
                    "before",
                )
        return view_arch

    @api.model
    def _view_add_ready_button(self, view_arch):
        if self._automatically_insert_ready_button:
            view_arch = self._add_view_element(
                view_arch,
                "ssi_transaction_ready_mixin.button_ready",
                "/form/header/field[@name='state']",
                "before",
            )
        return view_arch
