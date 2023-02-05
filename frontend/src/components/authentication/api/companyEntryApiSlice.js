import { apiSlice } from "./apiSlice";

export const companyEntryApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        getCompanyDetails: builder.query({
            query: (id) => `/api/company-details/${id}`,
            keepUnusedDataFor: 5,
            providesTags: ['CompanyDetails']
        }),
        updateCompanyDetails: builder.mutation({
            query: ({details, id}) => ({
                url: `/api/company-details/${id}`,
                method: 'PUT',
                body: details,
            }),
            invalidatesTags: ['CompanyDetails']
        }),
        postCompanyDetails: builder.mutation({
            query: details => ({
                url: "/api/company-details",
                method: 'POST',
                body: details,
            }),
            invalidatesTags: ['CompanyDetails']
        }),
    })
});

export const {
    useGetCompanyDetailsQuery,
    useUpdateCompanyDetailsMutation,
    usePostCompanyDetailsMutation,
} = companyEntryApiSlice