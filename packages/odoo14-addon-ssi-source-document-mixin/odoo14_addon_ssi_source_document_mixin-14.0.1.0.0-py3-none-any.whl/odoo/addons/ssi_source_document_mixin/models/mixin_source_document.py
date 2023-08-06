# Copyright 2021 OpenSynergy Indonesia
# Copyright 2021 PT. Simetri Sinergi Indonesia
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models


class MixingSourceDocument(models.AbstractModel):
    _name = "mixin.source_document"
    _description = "Mixin Object for Source Document"

    @api.depends(
        "source_document_res_id",
        "source_document_model_id",
    )
    def _compute_source_document_id(self):
        for record in self:
            result = False
            if record.source_document_res_id > 0 and record.source_document_model_id:
                result = "{},{}".format(
                    record.source_document_model,
                    record.source_document_res_id,
                )
            record.source_document_id = result

    @api.model
    def _source_document_reference_models(self):
        result = []
        for model in self.env["ir.model"].sudo().search([]):
            result.append((model.model, model.name))
        return result

    source_document_res_id = fields.Integer(
        string="Source Document Res ID",
        index=True,
    )
    source_document_model_id = fields.Many2one(
        string="Source Document Model",
        comodel_name="ir.model",
    )
    source_document_model = fields.Char(
        string="Source Document Model Technical Name",
        related="source_document_model_id.model",
        store=True,
    )
    source_document_id = fields.Reference(
        string="Source Document",
        selection="_source_document_reference_models",
        compute="_compute_source_document_id",
    )
