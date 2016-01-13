# -*- coding: utf-8 -*-

#    Author: Nicolas Bessi. Copyright Camptocamp SA
#    Copyright (C)
#       2014:       Agile Business Group (<http://www.agilebg.com>)
#       2015:       Grupo ESOC <www.grupoesoc.es>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
from openerp import api, fields, models


_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Adds last name and first name; name becomes a stored function field."""
    _inherit = 'res.partner'

    firstname = fields.Char("First name")
    lastname = fields.Char("Last name")
#     name = fields.Char(
#         compute="_compute_name",
#         inverse="_inverse_name_after_cleaning_whitespace",
#         required=False,
#         store=True)

    @api.model
    def create(self, vals):
        """Add Name if person and firstname or lastname in vals"""
        name = vals.get("name", self.env.context.get("default_name"))
        is_company = vals.get("is_company", self.env.context.get("default_is_company"))
        firstname = vals.get("firstname", self.env.context.get("default_firstname"))
        lastname = vals.get("lastname", self.env.context.get("default_lastname"))
        
        _logger.info("Firstname create: %s", vals)

        if not is_company:
            if firstname or lastname:
                vals['name'] = ' '.join(filter(None, [firstname, lastname]))
        return super(ResPartner, self).create(vals)
    
    @api.multi
    def write(self, vals):
        """ Fix Name if Lastname or firstname is in vals """
        if vals.has_key('lastname') or vals.has_key('firstname'):
            for par in self:
                firstname = vals.get("firstname", par.firstname)
                lastname = vals.get("lastname", par.lastname)
                vals['name'] = ' '.join(filter(None, [firstname, lastname]))
        
        return super(ResPartner, self).write(vals)
