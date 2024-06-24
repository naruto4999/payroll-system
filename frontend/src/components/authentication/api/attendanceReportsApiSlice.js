import { apiSlice } from "./apiSlice";

export const attendanceReportsApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    allEmployeeMissPunches: builder.query({
      query: (body) => ({
        url: `/api/employee-monthly-misspunch/${body.globalCompany.id}/${body.year}/${body.month}`,
        method: "GET",
      }),
      keepUnusedDataFor: 500,
      providesTags: ["AllEmployeeMissPunches"],
    }),
  }),
});

export const { useAllEmployeeMissPunchesQuery } = attendanceReportsApiSlice;
