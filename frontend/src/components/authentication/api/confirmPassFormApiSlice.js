import { apiSlice } from "./apiSlice";

export const confirmPassFormApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        confirmPassword: builder.mutation({
            query: details => {
                console.log(details);
                return {
                url: `/api/auth/password/reset-confirm/${details.uidb64}/${details.token}`,
                method: "POST",
                body: details,
            }},
        }),
    }),
});

export const { useConfirmPasswordMutation } = confirmPassFormApiSlice;
