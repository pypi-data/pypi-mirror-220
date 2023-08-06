# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from lxml import etree

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval


class MixinCustomInfo(models.AbstractModel):
    _description = "Inheritable abstract model to add custom info in any model"
    _name = "mixin.custom_info"

    _custom_info_create_page = False
    _custom_info_page_xpath = "//page[last()]"

    custom_info_template_id = fields.Many2one(
        string="Custom Information Template",
        comodel_name="custom_info.template",
        domain=lambda self: [("model", "=", self._name)],
    )
    custom_info_ids = fields.One2many(
        string="Custom Properties",
        comodel_name="custom_info.value",
        inverse_name="res_id",
        domain=lambda self: [("model", "=", self._name)],
        auto_join=True,
    )

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        if view_type == "form" and self._custom_info_create_page:
            doc = etree.XML(res["arch"])
            node_xpath = doc.xpath(self._custom_info_page_xpath)
            str_element = self.env["ir.qweb"]._render(
                "ssi_custom_information_mixin.custom_information_page"
            )
            for node in node_xpath:
                new_node = etree.fromstring(str_element)
                node.addnext(new_node)

            View = self.env["ir.ui.view"]

            if view_id and res.get("base_model", self._name) != self._name:
                View = View.with_context(base_model_name=res["base_model"])
            new_arch, new_fields = View.postprocess_and_fields(doc, self._name)
            res["arch"] = new_arch
            new_fields.update(res["fields"])
            res["fields"] = new_fields
        return res

    def onchange(self, values, field_name, field_onchange):
        x2many_field = "custom_info_ids"
        if x2many_field in field_onchange:
            subfields = getattr(self, x2many_field)._fields.keys()
            for subfield in subfields:
                field_onchange.setdefault(
                    "{}.{}".format(x2many_field, subfield),
                    "",
                )
        return super(MixinCustomInfo, self).onchange(
            values,
            field_name,
            field_onchange,
        )

    @api.onchange(
        "custom_info_template_id",
    )
    def _onchange_custom_info_template_id(self):
        values = self.custom_info_ids.filtered(lambda r: r.value)
        if self.custom_info_template_id:
            template = self.custom_info_template_id
            allowed_details = template.detail_ids
            to_remove_details = self.custom_info_ids.mapped("detail_id")
            to_add_details = allowed_details - to_remove_details
            for detail in to_add_details:
                newvalue = self.custom_info_ids.new(
                    {
                        "detail_id": detail.id,
                        "res_id": self.id,
                        "model": self._name,
                    }
                )
                values += newvalue
        self.custom_info_ids = values

    def action_reload_custom_info_template(self):
        for record in self:
            record.write(
                {
                    "custom_info_template_id": self._get_template_custom_info(),
                }
            )
            record._reload_custom_info()

    def action_reload_custom_info(self):
        for record in self:
            record._reload_custom_info()

    def _reload_custom_info(self):
        self.ensure_one()
        if self.custom_info_template_id:
            template = self.custom_info_template_id
            allowed_details = template.detail_ids
            self.custom_info_ids.filtered(
                lambda r: r.detail_id.id not in allowed_details.ids
            ).unlink()
            to_be_added = template.detail_ids - self.custom_info_ids.mapped("detail_id")
            for detail in to_be_added:
                self.custom_info_ids.create(
                    {
                        "detail_id": detail.id,
                        "res_id": self.id,
                        "model": self._name,
                    }
                )
        else:
            self.custom_info_ids.unlink()

    def unlink(self):
        """Remove linked custom info this way, as can't be handled
        automatically.
        """
        info_values = self.mapped("custom_info_ids")
        res = super(MixinCustomInfo, self).unlink()
        if res:
            info_values.unlink()
        return res

    def _get_custom_info_localdict(self):
        self.ensure_one()
        return {
            "env": self.env,
            "document": self,
        }

    def _evaluate_custom_info(self, template):
        self.ensure_one()
        if not template:
            return False
        try:
            method_name = "_evaluate_custom_info_" + template.computation_method
            result = getattr(self, method_name)(template)
        except Exception as error:
            msg_err = _("Error evaluating conditions.\n %s") % error
            raise UserError(msg_err)
        return result

    def _evaluate_custom_info_use_python(self, template):
        self.ensure_one()
        res = False
        localdict = self._get_custom_info_localdict()
        try:
            safe_eval(template.python_code, localdict, mode="exec", nocopy=True)
            res = localdict["result"]
        except Exception as error:
            raise UserError(_("Error evaluating conditions.\n %s") % error)
        return res

    def _evaluate_custom_info_use_domain(self, template):
        self.ensure_one()
        result = False
        domain = [("id", "=", self.id)] + safe_eval(template.domain, {})

        count_result = self.search_count(domain)
        if count_result > 0:
            result = True
        return result

    def _get_template_custom_info(self):
        result = False
        obj_template = self.env["custom_info.template"]
        criteria = [
            ("model_id.model", "=", str(self._name)),
        ]
        templates = obj_template.search(
            criteria,
            order="sequence desc",
        )
        for template in templates:
            if self._evaluate_custom_info(template):
                result = template.id
                break
        return result
