
import { apiSlice } from './apiSlice';

export const attendanceMachineConfigApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getAttendanceMachineConfig: builder.query({
      query: (company) => ({
        url: `/api/attendance-machine-config/${company}`,
        method: 'GET',
      }),
      keepUnusedDataFor: 600,
      providesTags: ['AttendanceMachineConfig'],
    }),
    addAttendanceMachineConfig: builder.mutation({
      query: (body) => ({
        url: `/api/attendance-machine-config-create`,
        method: 'POST',
        body: body,
      }),
      invalidatesTags: ['AttendanceMachineConfig'],
    }),
    updateAttendanceMachineConfig: builder.mutation({
      query: (body) => ({
        url: `/api/attendance-machine-config/${body.company}`,
        method: 'PUT',
        body: body,
      }),
      invalidatesTags: ['AttendanceMachineConfig'],
    }),
  }),
});

export const {
  useGetAttendanceMachineConfigQuery,
  useAddAttendanceMachineConfigMutation,
  useUpdateAttendanceMachineConfigMutation,
} = attendanceMachineConfigApiSlice;
