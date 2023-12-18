import * as yup from 'yup';

export const EmployeePersonalDetailSchema = yup.object().shape({
	photo: yup
		.mixed()
		.test('fileSize', 'File size is too large', (value) => {
			if (!value) return true; // Allow empty values

			// Handle URL case
			if (
				typeof `${import.meta.env.VITE_MEDIA_URL}${value}` === 'string' &&
				`${import.meta.env.VITE_MEDIA_URL}${value}`.startsWith('http')
			) {
				return true; // Assume URL is valid
			}

			const maxSize = 1024 * 1024; // 1 MB in bytes
			if (value instanceof File) {
				return value.size <= maxSize;
			}

			return false; // Invalid value type
		})
		.test('fileType', 'Invalid file type', (value) => {
			if (!value) return true; // Allow empty values

			// Handle URL case
			if (
				typeof `${import.meta.env.VITE_MEDIA_URL}${value}` === 'string' &&
				`${import.meta.env.VITE_MEDIA_URL}${value}`.startsWith('http')
			) {
				return true; // Assume URL is valid
			}

			const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
			if (value instanceof File) {
				return allowedTypes.includes(value.type);
			}

			return false; // Invalid value type
		})
		.nullable(), // Allows the field to be null (optional),

	// 1st column
	paycode: yup.string().required('Required').max(7, 'Paycode must have a maximum of 32 characters'),
	attendanceCardNo: yup
		.string()
		.required('Required')
		.matches(/^\d+$/, 'Attendance card number must contain only numbers')
		.max(7, 'Attendance card number must have a maximum of 7 digits'),
	name: yup.string().required('Required').max(100, 'Must be at most 100 characters'),
	fatherOrHusbandName: yup.string().max(100, 'Must be at most 100 characters').nullable(), // Allows the field to be null (optional),
	motherName: yup.string().max(100, 'Must be at most 100 characters').nullable(), // Allows the field to be null (optional),
	wifeName: yup.string().max(100, 'Must be at most 100 characters').nullable(), // Allows the field to be null (optional),
	dob: yup
		.date()
		.max(new Date(), 'Date of birth must be before or on the current date')
		.test('age', 'Person must be at least 15 years old', function (value) {
			if (!value) return true; // Skip validation if the field is empty
			const today = new Date();
			const minimumDate = new Date();
			minimumDate.setFullYear(today.getFullYear() - 15); // Subtract 15 years from the current date
			return value <= minimumDate;
		})
		.nullable(), // Allows the field to be null (optional)
	phoneNumber: yup
		.string()
		.matches(/^[0-9]+$/, 'Phone number must contain only digits')
		.length(10, 'Phone number must be 10 digits long')
		.nullable(), // Allows the field to be null (optional),

	// 2nd column
	alternatePhoneNumber: yup
		.string()
		.matches(/^[0-9]+$/, 'Phone number must contain only digits')
		.length(10, 'Phone number must be 10 digits long')
		.nullable(), // Allows the field to be null (optional),
	religion: yup.string().max(50, 'Religion must be at most 50 characters').nullable(), // Allows the field to be null (optional),
	email: yup.string().email('Invalid email format').max(150, 'Email must be at most 150 characters').nullable(), // Allows the field to be null (optional),
	handicapped: yup.boolean().required('Handicapped field is required'),
	gender: yup.string().oneOf(['M', 'F', 'O'], 'Invalid gender selection').nullable(), // Allows the field to be null (optional),
	maritalStatus: yup.string().oneOf(['S', 'M', 'D', 'W'], 'Invalid Marital Status').nullable(), // Allows the field to be null (optional),
	bloodGroup: yup
		.string()
		.oneOf(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'], 'Invalid Blood Group')
		.nullable(), // Allows the field to be null (optional),
	nationality: yup.string().max(50, 'Nationality must be at most 50 characters'),

	// 3rd column
	panNumber: yup
		.string()
		.length(10, 'Should be 10 characters long')
		.matches(/^[A-Za-z]{5}[0-9]{4}[A-Za-z]{1}$/, 'Invalid format')
		.nullable(), // Allows the field to be null (optional),
	drivingLicence: yup.string().max(16, 'Field must be at most 16 characters').nullable(),
	passport: yup.string().length(8, 'Passport must be 8 characters'),
	aadhaar: yup
		.string()
		.matches(/^\d+$/, 'Aadhaar must contain only numeric characters')
		.length(12, 'Aadhaar must be exactly 12 digits')
		.nullable(),
	educationQualification: yup
		.string()
		.oneOf(
			['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', 'G', 'PG'],
			'Please select a valid educational qualification'
		)
		.nullable(),
	technicalQualification: yup.string().max(50, 'Field must be at most 50 characters long').nullable(),
	localAddress: yup.string().max(250, 'Field must be at most 250 characters long').nullable(),

	// 4th column
	localDistrict: yup.string().max(30, 'Field must be at most 30 characters long').nullable(),
	localStateOrUnionTerritory: yup
		.string()
		.oneOf(
			[
				'AP',
				'AR',
				'AS',
				'BR',
				'CT',
				'GA',
				'GJ',
				'HR',
				'HP',
				'JH',
				'KA',
				'KL',
				'MP',
				'MH',
				'MN',
				'ML',
				'MZ',
				'NL',
				'OR',
				'PB',
				'RJ',
				'SK',
				'TN',
				'TG',
				'TR',
				'UP',
				'UK',
				'WB',
				'JK',
				'AN',
				'CH',
				'DN',
				'DD',
				'DL',
				'LD',
				'PY',
			],
			'Please Select a valid State or UT'
		)
		.nullable(),
	localPincode: yup
		.string()
		.matches(/^\d+$/, 'Local Pin Code must contain only digits')
		.length(6, 'Local Pin Code must be 6 digits long'),

	permanentAddress: yup.string().max(250, 'Field must be at most 250 characters long').nullable(),

	permanentDistrict: yup.string().max(30, 'Field must be at most 30 characters long').nullable(),
	permanentStateOrUnionTerritory: yup
		.string()
		.oneOf(
			[
				'AP',
				'AR',
				'AS',
				'BR',
				'CT',
				'GA',
				'GJ',
				'HR',
				'HP',
				'JH',
				'KA',
				'KL',
				'MP',
				'MH',
				'MN',
				'ML',
				'MZ',
				'NL',
				'OR',
				'PB',
				'RJ',
				'SK',
				'TN',
				'TG',
				'TR',
				'UP',
				'UK',
				'WB',
				'JK',
				'AN',
				'CH',
				'DN',
				'DD',
				'DL',
				'LD',
				'PY',
			],
			'Please Select a valid State or UT'
		)
		.nullable(),
	permanentPincode: yup
		.string()
		.matches(/^\d+$/, 'Permanent Pin Code must contain only digits')
		.length(6, 'Permanent Pin Code must be 6 digits long'),
});

// export const EmployeeProfessionalDetailSchema = yup.object().shape({
// 	employeeProfessionalDetail: yup.object().shape({
// 		dateOfJoining: yup.date().required('Required'), // Allows the field to be null (optional),
// 		dateOfConfirm: yup.date().required('Required'),
// 		department: yup.string().nullable(),
// 		designation: yup.string().nullable(),
// 		category: yup.string().nullable(),
// 		salaryGrade: yup.string().nullable(),
// 		weeklyOff: yup
// 			.string()
// 			.oneOf(
// 				['no_off', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'],
// 				'Invalid weekly off option'
// 			)
// 			.nullable(),
// 		extraOff: yup
// 			.string()
// 			.oneOf(
// 				[
// 					'no_off',
// 					'mon1',
// 					'mon2',
// 					'mon3',
// 					'mon4',
// 					'tue1',
// 					'tue2',
// 					'tue3',
// 					'tue4',
// 					'wed1',
// 					'wed2',
// 					'wed3',
// 					'wed4',
// 					'thu1',
// 					'thu2',
// 					'thu3',
// 					'thu4',
// 					'fri1',
// 					'fri2',
// 					'fri3',
// 					'fri4',
// 					'sat1',
// 					'sat2',
// 					'sat3',
// 					'sat4',
// 					'sun1',
// 					'sun2',
// 					'sun3',
// 					'sun4',
// 				],
// 				'Invalid extra off option'
// 			)
// 			.nullable(),
// 	}),
// 	employeeShift: yup.object().shape({
// 		shift: yup.string().required('Shift is required').nullable(false),
// 	}),
// });

export const EmployeeProfessionalDetailSchema = (isEditing) => {
	return yup.object().shape({
		employeeProfessionalDetail: yup.object().shape({
			dateOfJoining: yup.date().required('Required'),
			dateOfConfirm: yup.date().required('Required'),
			department: yup.string().nullable(),
			designation: yup.string().nullable(),
			category: yup.string().nullable(),
			salaryGrade: yup.string().nullable(),
			weeklyOff: yup
				.string()
				.oneOf(['no_off', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'], 'Invalid weekly off option')
				.nullable(),
			extraOff: yup
				.string()
				.oneOf(
					[
						'no_off',
						'mon1',
						'mon2',
						'mon3',
						'mon4',
						'tue1',
						'tue2',
						'tue3',
						'tue4',
						'wed1',
						'wed2',
						'wed3',
						'wed4',
						'thu1',
						'thu2',
						'thu3',
						'thu4',
						'fri1',
						'fri2',
						'fri3',
						'fri4',
						'sat1',
						'sat2',
						'sat3',
						'sat4',
						'sun1',
						'sun2',
						'sun3',
						'sun4',
					],
					'Invalid extra off option'
				)
				.nullable(),
		}),
		employeeShift: yup.object().shape({
			shift: isEditing == false ? yup.string().required('Shift is required') : yup.string().nullable(false),
		}),
	});
};

export const EmployeePfEsiDetailSchema = yup.object().shape({
	pfNumber: yup.string().max(50, 'Max Length is 50').trim(),
	esiNumber: yup.string().max(30, 'Max Length is 30').trim(),
	pfPercentIgnoreEmployeeValue: yup
		.number()
		.min(0, 'Value must be at least 0')
		.max(100, 'Value must be at most 100')
		.nullable()
		.typeError('Invalid value')
		.test('decimal-digits', 'Maximum 2 decimal digits allowed', (value) => {
			if (value === null || value === undefined) return true;
			const decimalDigits = value.toString().split('.')[1];
			return !decimalDigits || decimalDigits.length <= 2;
		}),
	pfPercentIgnoreEmployerValue: yup
		.number()
		.min(0, 'Value must be at least 0')
		.max(100, 'Value must be at most 100')
		.nullable()
		.typeError('Invalid value')
		.test('decimal-digits', 'Maximum 2 decimal digits allowed', (value) => {
			if (value === null || value === undefined) return true;
			const decimalDigits = value.toString().split('.')[1];
			return !decimalDigits || decimalDigits.length <= 2;
		}),
	pfLimitIgnoreEmployerValue: yup
		.number()
		.max(2147483646, 'Value must be at most 2147483646')
		.nullable()
		.typeError('Invalid value'),
	pfLimitIgnoreEmployeeValue: yup
		.number()
		.max(2147483646, 'Value must be at most 2147483646')
		.nullable()
		.typeError('Invalid value'),
});

export const EmployeeFamilyNomineeDetailSchema = yup.object().shape({
	familyNomineeDetail: yup.array().of(
		yup.object().shape({
			isPfNominee: yup.boolean(),
			name: yup.string().required('Name is required'),
			pfNomineeShare: yup.number().when('isPfNominee', {
				is: true,
				then: (pfNomineeShare) =>
					pfNomineeShare
						.required('Required')
						.max(100, "Can't exceed 100")
						.test('totalShare', 'Total % should not exceed 100', (value, context) => {
							let valuesArray = context.from[1].value.familyNomineeDetail;
							let totalShare = 0;
							valuesArray.forEach((detail) => {
								totalShare += detail.pfNomineeShare || 0;
							});
							return totalShare <= 100;
						}),
			}),

			esiNomineeShare: yup.number().when('isEsiNominee', {
				is: true,
				then: (esiNomineeShare) =>
					esiNomineeShare
						.required('Required')
						.max(100, "Can't exceed 100")
						.test('totalShare', 'Total % should not exceed 100', (value, context) => {
							let valuesArray = context.from[1].value.familyNomineeDetail;
							let totalShare = 0;
							valuesArray.forEach((detail) => {
								totalShare += detail.esiNomineeShare || 0;
							});
							return totalShare <= 100;
						}),
			}),

			faNomineeShare: yup.number().when('isFaNominee', {
				is: true,
				then: (faNomineeShare) =>
					faNomineeShare
						.required('Required')
						.max(100, "Can't exceed 100")
						.test('totalShare', 'Total % should not exceed 100', (value, context) => {
							let valuesArray = context.from[1].value.familyNomineeDetail;
							let totalShare = 0;
							valuesArray.forEach((detail) => {
								totalShare += detail.faNomineeShare || 0;
							});
							return totalShare <= 100;
						}),
			}),

			gratuityNomineeShare: yup.number().when('isGratuityNominee', {
				is: true,
				then: (gratuityNomineeShare) =>
					gratuityNomineeShare
						.required('Required')
						.max(100, "Can't exceed 100")
						.test('totalShare', 'Total % should not exceed 100', (value, context) => {
							let valuesArray = context.from[1].value.familyNomineeDetail;
							let totalShare = 0;
							valuesArray.forEach((detail) => {
								totalShare += detail.gratuityNomineeShare || 0;
							});
							return totalShare <= 100;
						}),
			}),
		})
	),
});

export const generateEmployeeSalaryDetailSchema = (earningHeadInitialValues) => {
	if (earningHeadInitialValues != null) {
		let EmployeeSalaryDetailSchema = yup.object().shape({
			earningsHead: yup.object().shape(
				Object.keys(earningHeadInitialValues).reduce((schema, key) => {
					return {
						...schema,
						[key]: yup.number().required(`${key} is required`),
					};
				}, {})
			),
			year: yup
				.number()
				.required('Year is required')
				.min(1950, 'Year must be greater than or equal to 1950')
				.max(2100, 'Year must be less than or equal to 2100'),
			salaryDetail: yup.object().shape({
				overtimeType: yup.string().required('Overtime Type is required'),
				overtimeRate: yup.string(),
				salaryMode: yup.string().required('Salary Mode is required'),
				paymentMode: yup.string().required('Payment Mode is required'),
				bankName: yup.string(),
				accountNumber: yup.string(),
				ifcs: yup.string(),
				labourWellfareFund: yup.boolean(),
				lateDeduction: yup.boolean(),
				bonusAllow: yup.boolean(),
				bonusExg: yup.boolean(),
			}),
		});
		return EmployeeSalaryDetailSchema;
	} else if (earningHeadInitialValues === null) {
		let EmployeeSalaryDetailSchema = yup.object().shape({
			year: yup
				.number()
				.required('Year is required')
				.min(1950, 'Year must be greater than or equal to 1950')
				.max(2100, 'Year must be less than or equal to 2100'),
			salaryDetail: yup.object().shape({
				overtimeType: yup.string().required('Overtime Type is required'),
				overtimeRate: yup.string(),
				salaryMode: yup.string().required('Salary Mode is required'),
				paymentMode: yup.string().required('Payment Mode is required'),
				bankName: yup.string(),
				accountNumber: yup.string(),
				ifcs: yup.string(),
				labourWellfareFund: yup.boolean(),
				lateDeduction: yup.boolean(),
				bonusAllow: yup.boolean(),
				bonusExg: yup.boolean(),
			}),
		});
		return EmployeeSalaryDetailSchema;
	}
};

// export const EmployeeSalaryDetailSchema = yup.object().shape({
//     earningsHead: yup.object().shape(
//       Object.keys(initialValues.earningsHead).reduce((schema, key) => {
//         return {
//           ...schema,
//           [key]: yup.number().required(`${key} is required`),
//         };
//       }, {})
//     ),
//   });
