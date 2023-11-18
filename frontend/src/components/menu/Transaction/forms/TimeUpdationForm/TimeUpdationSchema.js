import * as yup from 'yup';

export const TimeUpdationSchema = yup.object().shape({
	year: yup.number(),
	month: yup.number(),
	// manualFromDate: yup.date().required('From date is required'),
	manualToDate: yup
		.number()
		.positive()
		.test('valid-manual-to-date', 'Invalid date', function (value) {
			const { year, month, manualFromDate } = this.parent;
			if (!manualFromDate || !value) return true; // Allow if either date is not set
			const daysInSelectedMonth = new Date(year, month, 0).getDate();

			return value >= manualFromDate && value <= daysInSelectedMonth;
		}),
	manualFromDate: yup
		.number()
		.positive()
		.test('valid-manual-to-date', 'Invalid date', function (value) {
			const { year, month, manualToDate } = this.parent;
			if (!manualToDate || !value) return true; // Allow if either date is not set
			const daysInSelectedMonth = new Date(year, month, 0).getDate();

			return value <= manualToDate && value <= daysInSelectedMonth;
		}),
});

export const ConfirmationModalSchema = yup.object().shape({
	userInput: yup
		.string()
		.matches(/^Confirm$/, 'Must be equal to "Confirm"')
		.required('Required'),
});
