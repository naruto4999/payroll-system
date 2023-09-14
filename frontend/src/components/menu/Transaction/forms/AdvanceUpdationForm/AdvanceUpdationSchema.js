import * as Yup from 'yup';

const createAdvanceUpdationValidationSchema = (dateOfJoining, dateOfResignation) => {
	return Yup.object().shape({
		// dateOfJoining: Yup.date().required('Date of Joining is required'),
		// dateOfResignation: Yup.date(),
		employeeAdvanceDetails: Yup.array().of(
			Yup.object().shape({
				date: Yup.date()
					.required('Required')
					.min(dateOfJoining, 'Cannot be less than Date of Joining')
					.when('dateOfResignation', (resignationDate, schema) => {
						if (dateOfResignation && resignationDate !== '') {
							return schema.max(dateOfResignation, 'Cannot be more than Date of Resignation');
						}
						return schema;
					}),
				emi: Yup.number().required('Required').positive('Must be Greater than 0').integer('Cannot be decimal'),
				principal: Yup.number()
					.required('Required')
					.positive('Must be Greater than 0')
					.integer('Cannot be decimal'),
				// repaidAmount: Yup.number()
				// 	.required('Repaid Amount is required')
				// 	.min(0, 'Repaid Amount must be greater than or equal to 0'),
				// tenureMonthsLeft: Yup.string().required('Tenure Months Left is required'),
			})
		),
	});
};

export default createAdvanceUpdationValidationSchema;
