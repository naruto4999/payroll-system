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
            invalidatesTags: ["EmployeePersonalDetails"],
        }),
        getSingleEmployeeProfessionalDetail: builder.query({
            query: (employee) => ({
                url: `/api/employee-professional-detail/${employee.company}/${employee.id}`,
                method: "GET",
            }),
            keepUnusedDataFor: 1,
            // providesTags: ["EmployeePersonalDetails"],
        }),
        updateEmployeeProfessionalDetail: builder.mutation({
            query: employee => ({
                url: `/api/employee-professional-detail/${employee.globalCompany}/${employee.employee}`,
                method: 'PATCH',
                body: employee,
            }),
            invalidatesTags: ['EmployeeProfessionalDetails']
        }),
        addEmployeeSalaryEarning: builder.mutation({
            query: (body) => ({
                url: `/api/employee-salary-earning`,
                method: "POST",
                body: body,
            }),
            // invalidatesTags: ["EmployeePersonalDetails"],
        }),
        addEmployeeSalaryDetail: builder.mutation({
            query: (employeeSalaryDetail) => ({
                url: `/api/employee-salary-detail/${employeeSalaryDetail.company}`,
                method: "POST",
                body: employeeSalaryDetail,
            }),
            // invalidatesTags: ["EmployeePersonalDetails"],
        }),
        getSingleEmployeeSalaryEarning: builder.query({
            query: (employee) => ({
                url: `/api/employee-salary-earning/${employee.company}/${employee.id}`,
                method: "GET",
            }),
            keepUnusedDataFor: 1,
            // providesTags: ["EmployeePersonalDetails"],
        }),
        getSingleEmployeeSalaryDetail: builder.query({
            query: (employee) => ({
                url: `/api/employee-salary-detail/${employee.company}/${employee.id}`,
                method: "GET",
            }),
            keepUnusedDataFor: 1,
            // providesTags: ["EmployeePersonalDetails"],
        }),
        updateEmployeeSalaryEarning: builder.mutation({
            query: employee => ({
                url: `/api/employee-salary-earning-update/${employee.globalCompany}/${employee.employee}`,
                method: 'PUT',
                body: employee,
            }),
            // invalidatesTags: ['EmployeeProfessionalDetails']
        }),
        updateEmployeeSalaryDetail: builder.mutation({
            query: employee => ({
                url: `/api/employee-salary-detail/${employee.company}/${employee.employee}`,
                method: 'PUT',
                body: employee,
            }),
            // invalidatesTags: ['EmployeeProfessionalDetails']
        }),
        addEmployeeFamilyDetail: builder.mutation({
            query: (body) => ({
                url: `/api/employee-family-nominee-detail`,
                method: "POST",
                body: body,
            }),
            // invalidatesTags: ["EmployeePersonalDetails"],
        }),
    }),
});

export const {
    useGetEmployeePersonalDetailsQuery,
    useAddEmployeePersonalDetailMutation,
    useAddEmployeeProfessionalDetailMutation,
    useLazyGetSingleEmployeePersonalDetailQuery,
    useUpdateEmployeePersonalDetailMutation,
    useUpdateEmployeeProfessionalDetailMutation,
    useLazyGetSingleEmployeeProfessionalDetailQuery,
    useAddEmployeeSalaryEarningMutation,
    useLazyGetSingleEmployeeSalaryEarningQuery,
    useUpdateEmployeeSalaryEarningMutation,
    useAddEmployeeSalaryDetailMutation,
    useLazyGetSingleEmployeeSalaryDetailQuery,
    useUpdateEmployeeSalaryDetailMutation,
    useAddEmployeeFamilyDetailMutation,
} = employeeEntryApiSlice;
