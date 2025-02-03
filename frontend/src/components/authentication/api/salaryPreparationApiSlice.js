import { apiSlice } from './apiSlice';

export const salaryPreparationApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        getAllEmployeeMonthlyAttendanceDetails: builder.query({
            query: (body) => ({
                url: `/api/all-employee-monthly-attendance-details/${body.company}/${body.year}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 500,
            providesTags: ['AllEmployeeMonthlyAttendanceDetails'],
        }),
        getAllEmployeeSalaryEarnings: builder.query({
            query: (body) => ({
                url: `/api/all-employee-salary-earning/${body.company}/${body.year}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 500,
            providesTags: ['AllEmployeeSalaryEarnings'],
        }),
        getAllEmployeePfEsiDetails: builder.query({
            query: (body) => ({
                url: `/api/all-employee-pf-esi-detail/${body.company}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 500,
            providesTags: ['AllEmployeePfEsiDetail'],
        }),

        // all-employee-salary-earning/<int:company_id>/<int:year>

        addEmployeeSalaryPrepared: builder.mutation({
            query: (body) => ({
                url: `/api/employee-salary-prepared`,
                method: 'POST',
                body: body,
            }),
            invalidatesTags: [
                'AdvancePayments',
                'PreparedSalaries',
                'EarnedAmountPreparedSalary',
                'EmployeesForYearlyAdvanceReport',
                'EmployeePreparedSalary',
            ],
        }),
        employeeBulkSalaryPrepared: builder.mutation({
            query: (body) => ({
                url: `/api/employee-bulk-salary-prepared`,
                method: 'POST',
                body: body,
            }),
            invalidatesTags: [
                'AdvancePayments',
                'PreparedSalaries',
                'EarnedAmountPreparedSalary',
                'EmployeesForYearlyAdvanceReport',
                'EmployeePreparedSalary',
            ],
        }),
        calculateOtAttendanceUsingTotalEarned: builder.mutation({
            query: (body) => ({
                url: `/api/calculate-ot-attendance-using-total-earned`,
                method: 'POST',
                body: body,
            }),
            //Check this invalidates Tags later on
            invalidatesTags: [
                'AdvancePayments',
                'PreparedSalaries',
                'EarnedAmountPreparedSalary',
                'EmployeesForYearlyAdvanceReport',
                'EmployeePreparedSalary',
                'AllEmployeeMonthlyAttendanceDetails',
            ],
        }),
        getEmployeePreparedSalary: builder.query({
            query: (body) => ({
                url: `/api/prepared-salaries/${body.company_id}/${body.employee_id}/${body.year}/${body.month}`,
                method: 'GET',
            }),
            keepUnusedDataFor: 500,
            providesTags: ['EmployeePreparedSalary'],
        }),

        // updateEmployeeAdvancePayments: builder.mutation({
        // 	query: (body) => ({
        // 		url: `/api/employee-advance-payment-update/${body.company}/${body.employee}`,
        // 		method: 'PUT',
        // 		body: body,
        // 	}),
        // 	invalidatesTags: ['AdvancePayments'],
        // }),
        // deleteEmployeeAdvancePayments: builder.mutation({
        // 	query: (params) => ({
        // 		url: `/api/employee-advance-payment-delete/${params.company}/${
        // 			params.employee
        // 		}/${params.detailsToDelete.join(',')}`,
        // 		method: 'DELETE',
        // 	}),
        // 	invalidatesTags: ['AdvancePayments'],
        // }),
    }),
});

export const {
    useGetAllEmployeeMonthlyAttendanceDetailsQuery,
    useGetAllEmployeeSalaryEarningsQuery,
    useGetAllEmployeePfEsiDetailsQuery,
    useAddEmployeeSalaryPreparedMutation,
    useEmployeeBulkSalaryPreparedMutation,
    useCalculateOtAttendanceUsingTotalEarnedMutation,
    useGetEmployeePreparedSalaryQuery,
} = salaryPreparationApiSlice;
