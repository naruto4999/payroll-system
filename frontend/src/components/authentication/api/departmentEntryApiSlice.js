import { apiSlice } from "./apiSlice";

export const departmentEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getDepartments: builder.query({
            query: (company) => ({
                url: `/api/department/${company.id}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 1,
            provideTags: ['Departments']
        }),
        addDepartment: builder.mutation({
            query: department => ({
                url: "/api/department",
                method: 'POST',
                body: department,
            }),
            invalidatesTags: ['Departments']
        })
    })
})

export const {
    useGetDepartmentsQuery,
    useAddDepartmentMutation,
} = departmentEntryApiSlice