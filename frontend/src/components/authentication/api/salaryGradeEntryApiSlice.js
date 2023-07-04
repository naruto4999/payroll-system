import { apiSlice } from "./apiSlice";

export const salaryGradeEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getSalaryGrades: builder.query({
            query: globalCompany => ({
                url: `/api/salary-grade/${globalCompany.id}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 1,
            providesTags: ['SalaryGrades']
        }),
        addSalaryGrade: builder.mutation({
            query: salaryGrade => ({
                url: `/api/salary-grade/${salaryGrade.company}`,
                method: 'POST',
                body: salaryGrade,
            }),
            invalidatesTags: ['SalaryGrades']
        }),
        updateSalaryGrade: builder.mutation({
            query: salaryGrade => ({
                url: `/api/salary-grade/${salaryGrade.company}/${salaryGrade.id}`,
                method: 'PUT',
                body: salaryGrade,
            }),
            invalidatesTags: ['SalaryGrades']
        }),
        deleteSalaryGrade: builder.mutation({
            query: salaryGrade => ({
                url: `/api/salary-grade/${salaryGrade.company}/${salaryGrade.id}`,
                method: 'DELETE',
            }),
            invalidatesTags: ['SalaryGrades']
        }),
    })
})

export const {
    useGetSalaryGradesQuery,
    useAddSalaryGradeMutation,
    useUpdateSalaryGradeMutation,
    useDeleteSalaryGradeMutation,
} = salaryGradeEntryApiSlice