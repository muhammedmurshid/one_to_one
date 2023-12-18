from odoo import models, fields, api, _


class EmployeeOneToOneMeeting(models.Model):
    _name = 'employee.one.to.one.meeting'
    _description = 'Employee One To One Meeting'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'

    reason_for_meeting = fields.Selection([('poor_performance', 'Poor Performance'), ('late_comer', 'Late Comer'),
                                           ('not_attending_programme', 'Not Attending Programme'), ('other', 'Other')],
                                          string="Reason For Meeting", required=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    remarks = fields.Text(string="Remarks")
    late_by = fields.Float(string="Late By")
    programme = fields.Selection(
        [('sfc', 'SFC'), ('upaya', 'Upaya'), ('yes_plus', 'Yes Plus'), ('mock_interview', 'Mock Interview'),
         ('other', 'Other')], string="Programme")
    start_time = fields.Float(string="Start Time")
    end_time = fields.Float(string="End Time")
    type = fields.Selection([('online', 'Online'), ('offline', 'Offline')], string="Type")
    meeting_date = fields.Date(string="Meeting Date", required=1)
    state = fields.Selection([('draft', 'Draft'), ('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancel', 'Cancelled')], string="State",
                             tracking=True, default='draft')

    def action_schedule(self):
        for user in self:
            if user.employee_id:
                self.activity_schedule(
                    'one_to_one.mail_activity_one_to_one_meeting', user_id=user.employee_id.user_id.id,
                    note=f'Your one to one meeting has been scheduled. for {self.meeting_date}'),
        self.state = 'scheduled'

    def action_completed(self):
        activity_id = self.env['mail.activity'].search(
            [('res_id', '=', self.id), ('user_id', '=', self.employee_id.user_id.id), (
                'activity_type_id', '=', self.env.ref('one_to_one.mail_activity_one_to_one_meeting').id)])
        activity_id.action_feedback(feedback=f'one to one meeting has been completed.')
        self.state = 'completed'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'One to one meeting has been completed.',
                'type': 'rainbow_man',
            }
        }

    def action_cancel(self):
        activity_id = self.env['mail.activity'].search(
            [('res_id', '=', self.id), ('user_id', '=', self.employee_id.user_id.id), (
                'activity_type_id', '=', self.env.ref('one_to_one.mail_activity_one_to_one_meeting').id)])
        activity_id.action_feedback(feedback=f'one to one meeting has been cancelled.')
        self.state = 'cancel'
