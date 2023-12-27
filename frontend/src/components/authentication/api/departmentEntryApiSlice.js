import { apiSlice } from './apiSlice';

export const departmentEntryApiSlice = apiSlice.injectEndpoints({
	endpoints: (builder) => ({
		getDepartments: builder.query({
			query: (globalCompany) => ({
				url: `/api/department/${globalCompany.id}`,
				method: 'GET',
			}),
			keepUnusedDataFor: 500,
			providesTags: ['Departments'],
		}),
		addDepartment: builder.mutation({
			query: (department) => ({
				url: `/api/department/${department.company}`,
				method: 'POST',
				body: department,
			}),
			invalidatesTags: ['Departments'],
		}),
		updateDepartment: builder.mutation({
			query: (department) => ({
				url: `/api/department/${department.company}/${department.id}`,
				method: 'PUT',
				body: department,
			}),
			invalidatesTags: ['Departments'],
		}),
		deleteDepartment: builder.mutation({
			query: (department) => ({
				url: `/api/department/${department.company}/${department.id}`,
				method: 'DELETE',
			}),
			invalidatesTags: ['Departments'],
		}),
	}),
});

export const {
	useGetDepartmentsQuery,
	useAddDepartmentMutation,
	useDeleteDepartmentMutation,
	useUpdateDepartmentMutation,
} = departmentEntryApiSlice;
