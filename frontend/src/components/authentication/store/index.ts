import { configureStore } from "@reduxjs/toolkit";
import { combineReducers } from "redux";
import { FLUSH, PAUSE, PERSIST, persistReducer, persistStore, PURGE, REGISTER, REHYDRATE } from "redux-persist";
import storage from "redux-persist/lib/storage";
import { apiSlice } from "../api/apiSlice";
import reducer from "./slices/auth";
import globalCompanyReducer from "./slices/globalCompany";
import alertSliceReducer from "./slices/alertSlice"




const appReducer = combineReducers({
    [apiSlice.reducerPath]: apiSlice.reducer,
    auth: reducer,
    globalCompany: globalCompanyReducer,
    alert: alertSliceReducer,
});

export type RootState = ReturnType<typeof appReducer>;
const rootReducer = (state: RootState | undefined, action: any) => {
    if (action.type === 'RESET') {
      // Reset the entire Redux store to its initial state
      state = undefined;
    }
    
    return appReducer(state, action);
  };

const persistConfig = {
    key: "root",
    version: 1,
    storage: storage,
    blacklist: ['alert', apiSlice.reducerPath], 
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
// export type RootState = ReturnType<typeof appReducer>;
export default store;
