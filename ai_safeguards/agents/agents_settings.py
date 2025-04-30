# TODO: turn this file into a yaml settings file

gpt_claims_settings = {
    'format': {
        'type': 'json_schema',
        'name': 'claims',
        'schema': {
            'type': 'object',
            'properties': {
                'claims': {
                    'type': 'array',
                    'items': {'type': 'string'}
                }
            },
            'required': ['claims'],
            'additionalProperties': False
        },
        'strict': True
    }
}

gpt_factuality_settings = {
    'format': {
        'type': 'json_schema',
        'name': 'factuality',
        'schema': {
            'type': 'object',
            'properties': {
                'supported_claims': {
                    'type': 'array',
                    'items': {'type': 'string'}
                },
                'non_supported_claims': {
                    'type': 'array',
                    'items': {'type': 'string'}
                }
            },
            'required': ['supported_claims', 'non_supported_claims'],
            'additionalProperties': False
        },
        'strict': True
    }
}