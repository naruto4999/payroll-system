import * as Yup from 'yup';

const passwordSchema = Yup.object().shape({
	password: Yup.string()
		.required('Password is required')
		.min(8, 'Password must be at least 8 characters long')
		.matches(
			/^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*])/,
			'Password must contain at least one letter, one number, and one special symbol'
		),
	confirmPassword: Yup.string()
		.required('Confirm Password is required')
		.oneOf([Yup.ref('password'), null], 'Passwords must match'),
});

export default passwordSchema;
