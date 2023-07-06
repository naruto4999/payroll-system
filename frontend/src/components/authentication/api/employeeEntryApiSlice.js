import { apiSlice } from "./apiSlice";

export const employeeEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        getEmployeePersonalDetails: builder.query({
            query: (globalCompany) => ({
                url: `/api/employee-personal-detail/${globalCompany.id}`,
                method: "GET",
            }),
            keepUnusedDataFor: 1,
            providesTags: ["EmployeePersonalDetails"],
        }),
        addEmployeePersonalDetail: builder.mutation({
            query: (employeePersonalDetail) => ({
                url: `/api/employee-personal-detail`,
                method: "POST",
                body: employeePersonalDetail.formData,
                // formData:true 
            }),
            invalidatesTags: ["EmployeePersonalDetails"],
        }),
        getSingleEmployeePersonalDetail: builder.query({
            query: (employee) => ({
                url: `/api/employee-personal-detail/${employee.company}/${employee.id}`,
                method: "GET",
            }),
            keepUnusedDataFor: 1,
            // providesTags: ["EmployeePersonalDetails"],
        }),
        updateEmployeePersonalDetail: builder.mutation({
            query: employee => ({
                url: `/api/employee-personal-detail/${employee.globalCompany}/${employee.id}`,
                method: 'PATCH',
                body: employee.formData,
            }),
            invalidatesTags: ['EmployeePersonalDetails']
        }),
        // deleteShift: builder.mutation({
        //     query: shift => ({
        //         url: `/api/shift/${shift.company}/${shift.id}`,
        //         method: 'DELETE',
        //     }),
        //     invalidatesTags: ['Shifts']
        // }),
        addEmployeeProfessionalDetail: builder.mutation({
            query: (employeeProfessionalDetail) => ({
                url: `/api/employee-professional-detail`,
                method: "POST",
                body: employeeProfessionalDetail,
                // formData:true 
            }),
            invalidatesTags: ["EmployeeProfessionalDetails"],
        }),
    }),
});

export const {
    useGetEmployeePersonalDetailsQuery,
    useAddEmployeePersonalDetailMutation,
    useAddEmployeeProfessionalDetailMutation,
    useLazyGetSingleEmployeePersonalDetailQuery,
    useUpdateEmployeePersonalDetailMutation,
} = employeeEntryApiSlice;
