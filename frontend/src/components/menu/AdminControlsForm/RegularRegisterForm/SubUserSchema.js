import * as yup from 'yup';

export const subUserSchema = yup.object().shape({
	email: yup.string().email('Please enter a valid email address').required('Email is required'),
	password: yup
		.string()
		.required('Password is required')
		.min(8, 'Password must be at least 8 characters long')
		.matches(
			/^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*])/,
			'Password must contain at least one letter, one number, and one special symbol'
		),
	passConfirm: yup
		.string()
		.required('Please confirm your password')
		.oneOf([yup.ref('password')], 'Passwords do not match'),
	username: yup.string().required('Username is required').min(3, 'Username must be at least 3 characters long'),
	phoneNo: yup
		.string()
		.required('Phone number is required')
		.matches(/^[0-9]{10}$/, 'Phone number must be 10 digits'),
});

export const subUserUpdateSchema = yup.object().shape({
	email: yup.string().email('Please enter a valid email address').required('Email is required'),
	// password: yup
	// 	.string()
	// 	.required('Password is required')
	// 	.min(8, 'Password must be at least 8 characters long')
	// 	.matches(
	// 		/^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*])/,
	// 		'Password must contain at least one letter, one number, and one special symbol'
	// 	),
	// passConfirm: yup
	// 	.string()
	// 	.required('Please confirm your password')
	// 	.oneOf([yup.ref('password')], 'Passwords do not match'),
	username: yup.string().required('Username is required').min(3, 'Username must be at least 3 characters long'),
	phoneNo: yup
		.string()
		.required('Phone number is required')
		.matches(/^[0-9]{10}$/, 'Phone number must be 10 digits'),
});

export default subUserSchema;
