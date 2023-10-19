from odoo import models, fields, api, _


class OneToOneMeetingForm(models.Model):
    _name = 'one_to_one.meeting'
    _description = 'One To One Meeting'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'student_name'

    student_name = fields.Many2one('logic.students', string="Student Name", required=True)
    reason_for_meeting = fields.Selection([('poor_performance', 'Poor Performance'), ('late_comer', 'Late Comer'),
                                           ('not_attending_programme', 'Not Attending Programme'), ('other', 'Other')],
                                          string="Reason For Meeting", required=True)
    remarks = fields.Text(string="Remarks")
    late_by = fields.Float(string="Late By")
    mode_of_study = fields.Char(string="Mode of Study")
    coordinator_id = fields.Many2one('res.users', string="Coordinator", default=lambda self: self.env.user.id,)
    programme = fields.Selection(
        [('sfc', 'SFC'), ('upaya', 'Upaya'), ('yes_plus', 'Yes Plus'), ('mock_interview', 'Mock Interview'),
         ('other', 'Other')], string="Programme")
    name = fields.Char(string="Name", default='')
    start_time = fields.Datetime(string="Start Time")
    end_time = fields.Datetime(string="End Time")
    type = fields.Selection([('online', 'Online'), ('offline', 'Offline')], string="Type")
    meeting_with = fields.Selection([('student', 'Student'), ('parent', 'Parent'), ('both', 'Both'), ('other', 'Other')], string="Meeting With")
    other_meeting_with = fields.Char(string="Specify Reason")
    added_date = fields.Date(string="Added Date", default=lambda self: fields.Date.context_today(self))

    # @api.depends('student_name')
    # def _compute_rec_name(self):
    #     for rec in self:
    #         if rec.reason_for_meeting:
    #             rec.name = rec.student_name.name + ' - ' + rec.reason_for_meeting
    #         else:
    #             rec.name = 'One to One Meeting for ' + rec.student_name.name

    time_difference = fields.Float(string="Total Duration", compute="_compute_duration", store=True)

    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for record in self:
            if record.start_time and record.end_time:
                start_datetime = fields.Datetime.from_string(record.start_time)
                end_datetime = fields.Datetime.from_string(record.end_time)
                difference = (end_datetime - start_datetime).total_seconds() / 3600  # in hours
                record.time_difference = difference
            else:
                record.time_difference = 0.0
