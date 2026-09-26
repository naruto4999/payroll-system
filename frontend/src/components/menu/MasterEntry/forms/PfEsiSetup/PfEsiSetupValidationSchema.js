import * as yup from 'yup';

export const PfEsiSetupValidationSchema = yup.object().shape({
	//   user: yup.number().required('Required'),
	//   company: yup.number().required('Required'),
	ac1EpfEmployeePercentage: yup
		.number()
		.required('Required')
		.min(0, 'Cannot be less than 0')
		.max(100, 'Cannot be more than 100'),
	ac1EpfEmployeeLimit: yup
		.number()
		.integer('Cannot be a decimal')
		.required('Required')
		.min(0, 'Cannot be less than 0'),
	ac1EpfEmployerPercentage: yup
		.number()
		.required('Required')
		.min(0, 'Cannot be less than 0')
		.max(100, 'Cannot be more than 100'),
	ac1EpfEmployerLimit: yup
		.number()
		.integer('Cannot be a decimal')
		.required('Required')
		.min(0, 'Cannot be less than 0'),
	ac10EpsEmployerPercentage: yup
		.number()
		.required('Required')
		.min(0, 'Cannot be less than 0')
		.max(100, 'Cannot be more than 100'),
	ac10EpsEmployerLimit: yup
		.number()
		.integer('Cannot be a decimal')
		.required('Required')
		.min(0, 'Cannot be less than 0'),
	ac2EmployerPercentage: yup
		.number()
		.required('Required')
		.min(0, 'Cannot be less than 0')
		.max(100, 'Cannot be more than 100'),
	ac21EmployerPercentage: yup
		.number()
		.required('Required')
		.min(0, 'Cannot be less than 0')
		.max(100, 'Cannot be more than 100'),
	ac22EmployerPercentage: yup
		.number()
		.required('Required')
		.min(0, 'Cannot be less than 0')
		.max(100, 'Cannot be more than 100'),
	employerPfCode: yup.string().max(100, 'Cannot be more than 100'),
	esiEmployeePercentage: yup
		.number()
		.required('Required')
		.min(0, 'Cannot be less than 0')
		.max(100, 'Cannot be more than 100'),
	esiEmployeeLimit: yup
		.number()
		.integer('Cannot be a decimal')
		.required('Required')
		.min(0, 'Cannot be less than 0'),
	esiEmployerPercentage: yup
		.number()
		.required('Required')
		.min(0, 'Cannot be less than 0')
		.max(100, 'Cannot be more than 100'),
	esiEmployerLimit: yup
		.number()
		.integer('Cannot be a decimal')
		.required('Required')
		.min(0, 'Cannot be less than 0'),
	esiEarningsHeads: yup
		.array()
		.of(
			yup.number().integer('Earnings head IDs must be integers').positive('Earnings head IDs must be positive')
		)
		.ensure()
		.min(1, 'Select at least one ESI earnings head')
		.test(
			'unique',
			'Each earnings head can only be selected once',
			(ids) => new Set(ids.map(Number)).size === ids.length
		),
	employerEsiCode: yup.string().max(100, 'Cannot be more than 100'),
});

// export default PfEsiSetupValidationSchema;
