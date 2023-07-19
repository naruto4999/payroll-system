import { configureStore } from "@reduxjs/toolkit";
import { combineReducers } from "redux";
import { FLUSH, PAUSE, PERSIST, persistReducer, persistStore, PURGE, REGISTER, REHYDRATE } from "redux-persist";
import storage from "redux-persist/lib/storage";
import { apiSlice } from "../api/apiSlice";
import reducer from "./slices/auth";
import globalCompanyReducer from "./slices/globalCompany";
import alertSliceReducer from "./slices/alertSlice"


const rootReducer = combineReducers({
    [apiSlice.reducerPath]: apiSlice.reducer,
    auth: reducer,
    globalCompany: globalCompanyReducer,
    alert: alertSliceReducer,
});

const persistConfig = {
    key: "root",
    version: 1,
    storage: storage,
    blacklist: ['alert'], 
    // Use this to blacklist a slice/reducer the data of blacklisted slice will not be persisted
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

const store = configureStore({
    reducer: persistedReducer,
    middleware: (getDefaultMiddleware) =>
        getDefaultMiddleware({
            serializableCheck: {
                ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
            },
        }).concat(apiSlice.middleware),
    devTools: true, //turn off in production
});

export const persistor = persistStore(store);
export type RootState = ReturnType<typeof rootReducer>;
export default store;
