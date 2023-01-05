import { apiSlice } from "./apiSlice";

export const registerApiSlice = apiSlice.injectEndpoints({
    endpoints: builder => ({
        register: builder.mutation({
            query: credentials => ({
                url: "/api/auth/register/",
                method: 'POST',
                body: credentials
            })
        })
    })
})

export const {
    useRegisterMutation
} = registerApiSlice