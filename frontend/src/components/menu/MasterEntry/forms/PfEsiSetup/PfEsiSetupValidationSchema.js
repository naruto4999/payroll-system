import * as yup from 'yup';

export const PfEsiSetupValidationSchema = yup.object().shape({
//   user: yup.number().required(),
//   company: yup.number().required(),
  ac1EpfEmployeePercentage: yup.number().required().positive().max(100, "Cannot be more than 100"),
  ac1EpfEmployeeLimit: yup.number().integer('Cannot be a decimal').required().positive(),
  ac1EpfEmployerPercentage: yup.number().required().positive().max(100, "Cannot be more than 100"),
  ac1EpfEmployerLimit: yup.number().integer('Cannot be a decimal').required().positive(),
  ac10EpsEmployerPercentage: yup.number().required().positive().max(100, "Cannot be more than 100"),
  ac10EpsEmployerLimit: yup.number().integer('Cannot be a decimal').required().positive(),
  ac2EmployerPercentage: yup.number().required().positive().max(100, "Cannot be more than 100"),
  ac21EmployerPercentage: yup.number().required().positive().max(100, "Cannot be more than 100"),
  ac22EmployerPercentage: yup.number().required().positive().max(100, "Cannot be more than 100"),
  employerPfCode: yup.string().max(100, "Cannot be more than 100"),
  esiEmployeePercentage: yup.number().required().positive().max(100, "Cannot be more than 100"),
  esiEmployeeLimit: yup.number().integer('Cannot be a decimal').required().positive(),
  esiEmployerPercentage: yup.number().required().positive().max(100, "Cannot be more than 100"),
  esiEmployerLimit: yup.number().integer('Cannot be a decimal').required().positive(),
  employerEsiCode: yup.string().max(100, "Cannot be more than 100"),
});

// export default PfEsiSetupValidationSchema;
