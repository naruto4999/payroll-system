import { apiSlice } from "./apiSlice";

export const forgotPassFormApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        forgotPassword: builder.mutation({
            query: body => ({
                url: "/api/auth/password/reset/",
                method: 'POST',
                body: body
            })
        })
    })
})

export const {
    useForgotPasswordMutation
} = forgotPassFormApiSlice