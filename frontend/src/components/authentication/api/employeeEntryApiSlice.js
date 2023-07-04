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
        // updateShift: builder.mutation({
        //     query: shift => ({
        //         url: `/api/shift/${shift.company}/${shift.id}`,
        //         method: 'PUT',
        //         body: shift,
        //     }),
        //     invalidatesTags: ['Shifts']
        // }),
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
    
} = employeeEntryApiSlice;
