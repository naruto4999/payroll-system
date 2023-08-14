// validationSchema.js

import * as yup from 'yup';

const createValidationSchema = (dateOfJoining) =>
	yup.object().shape({
		fromDate: yup
			.date()
			.min(dateOfJoining, 'Cannot be earlier than date of joining')
			.nullable(),
		shift: yup.string().required('Shift is required').nullable(false),
	});

export default createValidationSchema;
