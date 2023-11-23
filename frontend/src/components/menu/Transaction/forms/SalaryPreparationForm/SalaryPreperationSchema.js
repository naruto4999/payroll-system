import * as yup from 'yup';

export const ConfirmationModalSchema = yup.object().shape({
	userInput: yup
		.string()
		.matches(/^Confirm$/, 'Must be equal to "Confirm"')
		.required('Required'),
});
