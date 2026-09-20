REPORT_OPTION_SCHEMAS = {
    ('payment_sheet', 'xlsx'): {
        'ot_hours_display': {
            'default': 'actual',
            'choices': {'actual', 'weighted'},
        },
    },
}


def normalize_report_options(report_type, output_format, options=None):
    schema = REPORT_OPTION_SCHEMAS.get((report_type, output_format))
    if schema is None:
        raise ValueError('Report configuration is not supported for this report and format.')
    if options is None:
        options = {}
    if not isinstance(options, dict):
        raise ValueError('Report configuration options must be an object.')

    unknown_options = set(options) - set(schema)
    if unknown_options:
        names = ', '.join(sorted(unknown_options))
        raise ValueError(f'Unsupported report configuration option(s): {names}.')

    normalized = {}
    for name, definition in schema.items():
        value = options.get(name, definition['default'])
        if value not in definition['choices']:
            choices = ', '.join(sorted(definition['choices']))
            raise ValueError(f'{name} must be one of: {choices}.')
        normalized[name] = value
    return normalized


def resolve_report_options(company, report_type, output_format):
    from .models import CompanyReportConfiguration

    configuration = CompanyReportConfiguration.objects.filter(
        company=company,
        report_type=report_type,
        output_format=output_format,
    ).first()
    return normalize_report_options(
        report_type,
        output_format,
        configuration.options if configuration else None,
    )
