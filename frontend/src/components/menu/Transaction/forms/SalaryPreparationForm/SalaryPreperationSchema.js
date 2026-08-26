import * as yup from 'yup';

export const ConfirmationModalSchema = yup.object().shape({
	userInput: yup
		.string()
		.matches(/^Confirm$/, 'Must be equal to "Confirm"')
		.required('Required'),
});

const nonNegativeWholeAmount = yup
	.number()
	.typeError('Must be a number')
	.integer('Must be a whole number')
	.min(0, 'Cannot be negative')
	.required('Required');

export const SalaryPreparationSchema = yup.object().shape({
	year: yup.number().integer().required(),
	month: yup.number().integer().min(1).max(12).required(),
	employeeSalaryPrepared: yup.object().shape({
		incentiveAmount: nonNegativeWholeAmount,
		advanceDeducted: nonNegativeWholeAmount,
		vpfDeducted: nonNegativeWholeAmount,
		tdsDeducted: nonNegativeWholeAmount,
		othersDeducted: nonNegativeWholeAmount,
	}),
	earnedAmount: yup.array().of(
		yup.object().shape({
			arearAmount: nonNegativeWholeAmount,
		})
	),
});
