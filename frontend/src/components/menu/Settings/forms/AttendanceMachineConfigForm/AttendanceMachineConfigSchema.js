import * as yup from 'yup';

export const AttendanceMachineConfigSchema = yup.object().shape({
  //   user: yup.number().required('Required'),
  //   company: yup.number().required('Required'),
  machineIp: yup
    .string()
    .matches(
      /^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$/,
      'Invalid IPv4 address'
    )
    .required('IPv4 address is required'),
})
