{
    'name': "One To One",
    'version': "14.0.1.0",
    'sequence': "0",
    'depends': ['base', 'mail', 'logic_base'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/record_rule.xml',
        'views/one_to_one.xml'

    ],
    'demo': [],
    'summary': "logic_one_to_one_meeting",
    'description': "this_is_my_app",
    'installable': True,
    'auto_install': False,
    'license': "LGPL-3",
    'application': False
}
