# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import io
import logging
from base64 import b64encode

from lxml import etree

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

try:
    import qrcode
except (ImportError, IOError) as err:
    _logger.debug(err)


class MixinQRCode(models.AbstractModel):
    _name = "mixin.qr_code"
    _description = "QR Code Mixin"

    _qr_code_create_page = False
    _qr_code_page_xpath = "//page[last()]"

    def _compute_qr_image(self):
        for document in self:
            qrcode_content = document._get_qr_code_content()
            img = qrcode.make(qrcode_content)
            result = io.BytesIO()
            img.save(result, format="PNG")
            result.seek(0)
            img_bytes = result.read()
            base64_encoded_result_bytes = b64encode(img_bytes)
            qr_image = base64_encoded_result_bytes.decode("ascii")
            document.qr_image = qr_image

    qr_image = fields.Binary(
        string="QR Code",
        compute="_compute_qr_image",
        store=False,
    )

    @api.model
    def fields_view_get(
        self, view_id=None, view_type="form", toolbar=False, submenu=False
    ):
        res = super().fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu
        )
        if view_type == "form" and self._qr_code_create_page:
            doc = etree.XML(res["arch"])
            node_xpath = doc.xpath(self._qr_code_page_xpath)
            if node_xpath:
                str_element = self.env["ir.qweb"]._render(
                    "ssi_qr_code_mixin.qr_code_page"
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

    def _get_qr_code_content(self):
        self.ensure_one()
        criteria = [
            ("model", "=", self._name),
        ]
        obj_ir_model = self.env["ir.model"]
        content_policy = obj_ir_model.search(criteria)
        if len(content_policy) > 0:
            content = content_policy[0]._get_qr_content(self)
        else:
            content = self._get_qr_standard_content()
        return content

    def _get_qr_standard_content(self):
        self.ensure_one()
        odoo_url = self.env["ir.config_parameter"].get_param("web.base.url")
        document_url = "/web?#id=%d&view_type=form&model=%s" % (
            self.id,
            self._name,
        )
        full_url = odoo_url + document_url
        return full_url
