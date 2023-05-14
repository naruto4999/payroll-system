import { apiSlice } from "./apiSlice";

export const regularRegisterApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        getRegulars: builder.query({
            query: () => ({
                url: "/api/regular",
                method: "GET",
            }),
            keepUnusedDataFor: 1,
            providesTags: ["Regular"],
        }),
        deleteRegular: builder.mutation({
            query: () => ({
                url: `/api/regular`,
                method: "DELETE",
            }),
            invalidatesTags: ["Regular"],
        }),
        regularRegister: builder.mutation({
            query: (credentials) => ({
                url: "/api/auth/regular-register/",
                method: "POST",
                body: credentials,
            }),
            invalidatesTags: ["Regular"],
        }),
    }),
});

export const {
    useDeleteRegularMutation,
    useGetRegularsQuery,
    useRegularRegisterMutation,
} = regularRegisterApiSlice;
