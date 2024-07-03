import { apiSlice } from "./apiSlice";

export const attendanceReportsApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    allEmployeeYearlyMissPunches: builder.query({
      query: (body) => ({
        url: `/api/employee-monthly-misspunch/${body.globalCompany.id}/${body.year}`,
        method: "GET",
      }),
      keepUnusedDataFor: 500,
      providesTags: ["AllEmployeeMissPunches"],
    }),
  }),
});

export const { useAllEmployeeYearlyMissPunchesQuery } = attendanceReportsApiSlice;
