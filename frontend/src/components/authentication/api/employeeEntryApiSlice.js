import { apiSlice } from './apiSlice';

export const employeeEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        // Personal Details
        getEmployeePersonalDetails: builder.query({
            query: (globalCompany) => ({
                url: `/api/employee-personal-detail/${globalCompany.id}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 600,
            providesTags: [{ type: 'EmployeePersonalDetails', id: 'LIST' }],
        }),
        addEmployeePersonalDetail: builder.mutation({
            query: (employeePersonalDetail) => ({
                url: `/api/employee-personal-detail`,
                method: 'POST',
                body: employeePersonalDetail.formData,
            }),
            invalidatesTags: [{ type: 'EmployeePersonalDetails', id: 'LIST' }],
        }),
        getSingleEmployeePersonalDetail: builder.query({
            query: (employee) => ({
                url: `/api/employee-personal-detail/${employee.company}/${employee.id}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 600,
            providesTags: (result, error, id) => [{ type: 'EmployeePersonalDetails', id: id.id }],
        }),
        updateEmployeePersonalDetail: builder.mutation({
            query: (employee) => ({
                url: `/api/employee-personal-detail/${employee.globalCompany}/${employee.id}`,
                method: 'PATCH',
                body: employee.formData,
            }),
            invalidatesTags: (result, error, id) => [
                { type: 'EmployeePersonalDetails', id: id.id },
                { type: 'EmployeePersonalDetails', id: 'LIST' },
            ],
        }),
        deleteEmployee: builder.mutation({
            query: (employee) => ({
                url: `/api/employee-personal-detail/${employee.company}/${employee.id}`,
                method: 'DELETE',
            }),
            invalidatesTags: (result, error, id) => [
                { type: 'EmployeePersonalDetails', id: id.id },
                { type: 'EmployeePersonalDetails', id: 'LIST' },
            ],
        }),

        // Visibilty of employees in sub user account
        updateVisibleEmployees: builder.mutation({
            query: (body) => ({
                url: `/api/employee-visible`,
                method: 'PATCH',
                body: body,
            }),
            invalidatesTags: [{ type: 'EmployeePersonalDetails', id: 'LIST' }],
        }),

        // Professional Details
        getSingleEmployeeProfessionalDetail: builder.query({
            query: (employee) => ({
                url: `/api/employee-professional-detail/${employee.company}/${employee.id}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 600,
            providesTags: (result, error, id) => [{ type: 'EmployeeProfessionalDetails', id: id.id }],
        }),
        addEmployeeProfessionalDetail: builder.mutation({
            query: (employeeProfessionalDetail) => ({
                url: `/api/employee-professional-detail`,
                method: 'POST',
                body: employeeProfessionalDetail,
            }),
            invalidatesTags: [{ type: 'EmployeePersonalDetails', id: 'LIST' }, 'EmployeeShifts'],
        }),
        updateEmployeeProfessionalDetail: builder.mutation({
            query: (employee) => ({
                url: `/api/employee-professional-detail/${employee.globalCompany}/${employee.employee}`,
                method: 'PATCH',
                body: employee,
            }),
            invalidatesTags: (result, error, id) => [
                { type: 'EmployeeProfessionalDetails', id: id.employee },
                { type: 'EmployeePersonalDetails', id: 'LIST' },
                'EmployeeShifts',
            ],
        }),

        // Salary Earning
        getSingleEmployeeSalaryEarning: builder.query({
            query: (employee) => ({
                url: `/api/employee-salary-earning/${employee.company}/${employee.id}/${employee.year}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 10,
            providesTags: ['SingleEmployeeSalaryEarning'],
        }),
        addEmployeeSalaryEarning: builder.mutation({
            query: (body) => ({
                url: `/api/employee-salary-earning/${body.company}/${body.employee}`,
                method: 'POST',
                body: body,
            }),
            invalidatesTags: ['AllEmployeeSalaryEarnings'],
        }),
        updateEmployeeSalaryEarning: builder.mutation({
            query: (employee) => ({
                url: `/api/employee-salary-earning-update/${employee.globalCompany}/${employee.employee}`,
                method: 'PUT',
                body: employee,
            }),
            invalidatesTags: ['SingleEmployeeSalaryEarning', 'AllEmployeeSalaryEarnings'],
        }),

        // Salary Detail
        getSingleEmployeeSalaryDetail: builder.query({
            query: (employee) => ({
                url: `/api/employee-salary-detail/${employee.company}/${employee.id}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 600,
            providesTags: (result, error, id) => [{ type: 'EmployeeSalaryDetails', id: id.id }],
        }),
        addEmployeeSalaryDetail: builder.mutation({
            query: (employeeSalaryDetail) => ({
                url: `/api/employee-salary-detail/${employeeSalaryDetail.company}`,
                method: 'POST',
                body: employeeSalaryDetail,
            }),
            invalidatesTags: ['AllEmployeeSalaryDetail'],
        }),
        updateEmployeeSalaryDetail: builder.mutation({
            query: (employee) => ({
                url: `/api/employee-salary-detail/${employee.company}/${employee.employee}`,
                method: 'PUT',
                body: employee,
            }),
            invalidatesTags: (result, error, id) => [
                { type: 'EmployeeSalaryDetails', id: id.employee },
                'AllEmployeeSalaryDetail',
            ],
        }),

        //Pf Esi Detail
        getSingleEmployeePfEsiDetail: builder.query({
            query: (employee) => ({
                url: `/api/employee-pf-esi-detail/${employee.company}/${employee.id}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 600,
            providesTags: (result, error, id) => [{ type: 'EmployeePfEsiDetails', id: id.id }],
        }),
        addEmployeePfEsiDetail: builder.mutation({
            query: (employeePfEsiDetail) => ({
                url: `/api/employee-pf-esi-detail`,
                method: 'POST',
                body: employeePfEsiDetail,
            }),
            invalidatesTags: ['AllEmployeePfEsiDetail', { type: 'EmployeePersonalDetails', id: 'LIST' }],
        }),
        updateEmployeePfEsiDetail: builder.mutation({
            query: (employee) => ({
                url: `/api/employee-pf-esi-detail/${employee.globalCompany}/${employee.employee}`,
                method: 'PATCH',
                body: employee,
            }),
            invalidatesTags: (result, error, id) => [
                { type: 'EmployeePfEsiDetails', id: id.employee },
                { type: 'EmployeeFamilyNomineeDetails', id: id.employee },
                'AllEmployeePfEsiDetail',
                { type: 'EmployeePersonalDetails', id: 'LIST' },
            ],
        }),

        //Family Nomineee Detail
        getEmployeeFamilyNomineeDetails: builder.query({
            query: (employee) => ({
                url: `/api/employee-family-nominee-detail/${employee.company}/${employee.id}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 600,
            providesTags: (result, error, id) => {
                console.log(id);
                return [{ type: 'EmployeeFamilyNomineeDetails', id: id.id }];
            },
        }),
        addEmployeeFamilyNomineeDetail: builder.mutation({
            query: (body) => ({
                url: `/api/employee-family-nominee-detail`,
                method: 'POST',
                body: body,
            }),
            invalidatesTags: (result, error, id) => {
                console.log(id);
                return [
                    {
                        type: 'EmployeeFamilyNomineeDetails',
                        id: id.familyNomineeDetail[0].employee,
                    },
                ];
            },
        }),
        updateEmployeeFamilyNomineeDetail: builder.mutation({
            query: (employee) => ({
                url: `/api/employee-family-nominee-detail-update/${employee.globalCompany}/${employee.employee}`,
                method: 'PUT',
                body: employee,
            }),
            invalidatesTags: (result, error, id) => {
                console.log(id);
                return [{ type: 'EmployeeFamilyNomineeDetails', id: id.employee }];
            },
        }),
        deleteEmployeeFamilyNomineeDetail: builder.mutation({
            query: (employee) => ({
                url: `/api/employee-family-nominee-detail-delete/${employee.company}/${employee.employee}/${employee.id}`,
                method: 'DELETE',
            }),
            invalidatesTags: (result, error, id) => {
                console.log(id);
                return [{ type: 'EmployeeFamilyNomineeDetails', id: id.employee }];
            },
        }),
    }),
});

export const {
    useDeleteEmployeeMutation,
    useGetEmployeePersonalDetailsQuery,
    useAddEmployeePersonalDetailMutation,
    useAddEmployeeProfessionalDetailMutation,
    useLazyGetSingleEmployeePersonalDetailQuery,
    useUpdateEmployeePersonalDetailMutation,
    useUpdateEmployeeProfessionalDetailMutation,
    useLazyGetSingleEmployeeProfessionalDetailQuery,
    useAddEmployeeSalaryEarningMutation,
    useGetSingleEmployeeSalaryEarningQuery,
    useLazyGetSingleEmployeeSalaryEarningQuery,
    useUpdateEmployeeSalaryEarningMutation,
    useAddEmployeeSalaryDetailMutation,
    useLazyGetSingleEmployeeSalaryDetailQuery,
    useGetSingleEmployeeSalaryDetailQuery,
    useUpdateEmployeeSalaryDetailMutation,
    useAddEmployeeFamilyNomineeDetailMutation,
    useAddEmployeePfEsiDetailMutation,
    useLazyGetSingleEmployeePfEsiDetailQuery,
    useUpdateEmployeePfEsiDetailMutation,
    useLazyGetEmployeeFamilyNomineeDetailsQuery,
    useGetSingleEmployeePfEsiDetailQuery,
    useUpdateEmployeeFamilyNomineeDetailMutation,
    useDeleteEmployeeFamilyNomineeDetailMutation,
    useGetSingleEmployeePersonalDetailQuery,
    useGetSingleEmployeeProfessionalDetailQuery,
    useUpdateVisibleEmployeesMutation,
} = employeeEntryApiSlice;
