from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProjectProject(models.Model):
    _inherit = 'project.project'

    is_frozen = fields.Boolean(string="Frizado", default=False)

    @api.constrains('task_ids')
    def _check_frozen_project(self):
        """ Evita modificar tareas si el proyecto está frizado """
        for project in self:
            if project.is_frozen:
                raise ValidationError("No puedes modificar tareas en un proyecto frizado.")

class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def create(self, vals):
        """ Evita crear tareas en proyectos frizados """
        project = self.env['project.project'].browse(vals.get('project_id'))
        if project.is_frozen:
            raise ValidationError("No puedes agregar tareas a un proyecto frizado.")
        return super(ProjectTask, self).create(vals)

    def write(self, vals):
        """ Evita modificar tareas en proyectos frizados """
        for task in self:
            if task.project_id.is_frozen:
                raise ValidationError("No puedes modificar tareas en un proyecto frizado.")
        return super(ProjectTask, self).write(vals)

    def unlink(self):
        """ Evita eliminar tareas de proyectos frizados """
        for task in self:
            if task.project_id.is_frozen:
                raise ValidationError("No puedes eliminar tareas de un proyecto frizado.")
        return super(ProjectTask, self).unlink()
