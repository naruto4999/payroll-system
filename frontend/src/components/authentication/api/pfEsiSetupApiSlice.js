import { apiSlice } from "./apiSlice";

export const pfEsiSetupApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        getPfEsiSetup: builder.query({
            query: (globalCompany) => ({
                url: `/api/pf-esi-setup/${globalCompany}`,
                method: "GET",
            }),
            keepUnusedDataFor: 600,
            providesTags: ["PfEsiSetup"],
        }),
        addPfEsiSetup: builder.mutation({
            query: (body) => ({
                url: `/api/pf-esi-setup-create`,
                method: "POST",
                body: body,
            }),
            invalidatesTags: ["PfEsiSetup"],
        }),
        updatePfEsiSetup: builder.mutation({
            query: (body) => ({
                url: `/api/pf-esi-setup/${body.company}`,
                method: "PUT",
                body: body,
            }),
            invalidatesTags: ["PfEsiSetup"],
        }),
    }),
});

export const {
    useGetPfEsiSetupQuery,
    useAddPfEsiSetupMutation,
    useUpdatePfEsiSetupMutation,
} = pfEsiSetupApiSlice;
