import { createSlice } from "@reduxjs/toolkit"

const initialState = {id: null, name: null}

const globalCompanySlice = createSlice({
    name: "globalCompany",
    initialState,
    reducers: {
        setCompany(state, action) {
            state.id = action.payload.id;
            state.name = action.payload.name;
        },
        deselectComapny(state) {
            state.id = null;
            state.name = null;
        }
    }
})

const globalCompanyReducer = globalCompanySlice.reducer;
export default globalCompanyReducer;
export const globalCompanyActions = globalCompanySlice.actions;