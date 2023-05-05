import { apiSlice } from "./apiSlice";

export const regularRegisterApiSlice = apiSlice.injectEndpoints({
    endpoints: (builder) => ({
        regularRegister: builder.mutation({
            query: (credentials) => ({
                url: "/api/auth/regular-register/",
                method: "POST",
                body: credentials,
            }),
        }),
    }),
});

export const { useRegularRegisterMutation } = regularRegisterApiSlice;
