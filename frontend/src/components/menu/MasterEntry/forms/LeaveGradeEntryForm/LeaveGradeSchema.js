import * as yup from 'yup';

export const LeaveGradeSchema = yup.object().shape({
	name: yup
		.string()
		.matches(/^\S*$/, 'Field must not contain spaces')
		.min(1, 'Leave Grade name must be atleast 1 characters long')
		.required('Required'),
	paid: yup.boolean().required('Paid field is required'),
	limit: yup
		.number()
		.typeError('Field must be a number')
		.max(365, 'Field must be less than or equal to 365'),
	generateFrequency: yup
		.number()
		.typeError('Field must be a number')
		.max(365, 'Field must be less than or equal to 365'),
});
