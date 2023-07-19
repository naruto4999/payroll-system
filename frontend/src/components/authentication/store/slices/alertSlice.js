import { createSlice } from "@reduxjs/toolkit";
// import { extraAction } from "../extraAction";
const alertSlice = createSlice({
    name: "alert",
    initialState: {
        alerts: [],
    },
    reducers: {
        // Accepted tyes are "error" "success" and "warning"
        createAlert: (state, action) => {
            state.alerts.push({
                message: action.payload.message,
                type: action.payload.type,
                duration: action.payload.duration,
            });
        },
    },
    // extraReducers: {
    //     [extraAction]: (state, action) => {
    //         state.alerts.push({ message: action.error.message, type: "error" });
    //     },
    // },
});

export const alertActions = alertSlice.actions;

// export default alertSlice;
const alertSliceReducer = alertSlice.reducer;
export default alertSliceReducer;
