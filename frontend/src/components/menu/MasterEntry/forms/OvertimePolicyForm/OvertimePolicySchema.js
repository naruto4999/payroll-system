import * as yup from 'yup';

const dayRuleSchema = yup.object({
	enabled: yup.boolean(),
	dayType: yup.string().oneOf(['REGULAR', 'WEEKLY_OFF', 'HOLIDAY']).required(),
	multiplier: yup.string().when('enabled', {
		is: true,
		then: (schema) =>
			schema
				.required('Multiplier is required')
				.matches(/^\d{1,3}(?:\.\d{1,3})?$/, 'Use a positive number with up to 3 decimal places')
				.test('positive', 'Multiplier must be greater than zero', (value) => Number(value) > 0),
	}),
	lateDeductionPriority: yup.mixed().when('enabled', {
		is: true,
		then: () =>
			yup
				.number()
				.typeError('Priority must be a whole number')
				.integer('Priority must be a whole number')
				.min(1, 'Priority must be at least 1')
				.required('Priority is required'),
	}),
});

export const OvertimePolicySchema = yup.object({
	name: yup.string().trim().max(100, 'Name must be 100 characters or fewer').required('Name is required'),
	isActive: yup.boolean(),
	isDefault: yup.boolean().test('active-default', 'An inactive policy cannot be the default', function (value) {
		return !value || this.parent.isActive;
	}),
	earningsBasis: yup.string().oneOf(['ALL_EARNINGS', 'SELECTED_HEADS']).required(),
	selectedEarningHeadIds: yup.array().when('earningsBasis', {
		is: 'SELECTED_HEADS',
		then: (schema) => schema.min(1, 'Select at least one earning head'),
	}),
	roundingIncrementMinutes: yup
		.number()
		.typeError('Enter a whole number')
		.integer('Enter a whole number')
		.min(1, 'Rounding increment must be greater than zero')
		.required('Rounding increment is required'),
	roundUpFromMinutes: yup
		.number()
		.typeError('Enter a whole number')
		.integer('Enter a whole number')
		.min(1, 'Round-up threshold must be at least 1')
		.required('Round-up threshold is required')
		.test('within-increment', 'Round-up threshold cannot exceed the increment', function (value) {
			return value == null || Number(value) <= Number(this.parent.roundingIncrementMinutes);
		}),
	dayRules: yup.array().of(dayRuleSchema).test('unique-priorities', 'Enabled priorities must be unique', (rules) => {
		const priorities = (rules || []).filter((rule) => rule.enabled).map((rule) => Number(rule.lateDeductionPriority));
		return priorities.length === new Set(priorities).size;
	}),
});
