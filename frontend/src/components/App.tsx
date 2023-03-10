import Sidebar from "./menu/Sidebar";
import { Routes, Route } from "react-router-dom";
// import CompanyEntryForm from "./menu/MasterEntry/forms/CompanyEntryForm";
// import BankEntryForm from "./menu/MasterEntry/forms/BankEntryForm";
// import CategoryEntryForm from "./menu/MasterEntry/forms/CategoryEntryForm";
// import DepartmentEntryForm from "./menu/MasterEntry/forms/DepartmentEntryForm";
// import DesignationEntryForm from "./menu/MasterEntry/forms/DesignationEntryForm";
// import EmployeeEntryForm from "./menu/MasterEntry/forms/EmployeeEntryForm";
// import HolidayEntryForm from "./menu/MasterEntry/forms/HolidayEntryForm";
// import SalaryGradeEntryForm from "./menu/MasterEntry/forms/SalaryGradeEntryForm";
// import ShiftEntryForm from "./menu/MasterEntry/forms/ShiftEntryForm";
import LoginForm from "./authentication/Login";
import Profile from "./authentication/Profile";
import RegisterForm from "./authentication/Register";
import NewCompanyEntryForm from "./menu/MasterEntry/forms/NewCompanyEntryForm/NewCompanyEntryForm";
import SelectCompany from "./menu/MasterEntry/forms/SelectCompany/SelectCompany";
import CompanyEntryForm from "./menu/MasterEntry/forms/CompanyEntryForm/CompanyEntryForm";
import DepartmentEntryForm from "./menu/MasterEntry/forms/DepartmentEntryForm/DepartmentEntryForm";

// import store, { persistor } from "./authentication/store/index"
// import { PersistGate } from "redux-persist/integration/react";
// import { Provider } from "react-redux";
import ProtectedRouteProps from "./authentication/routes/ProtectedRoute";
import ProtectedRoute from "./authentication/routes/ProtectedRoute";
import { RootState } from "./authentication/store/index";
import { useSelector } from "react-redux";
import { useState, useEffect } from "react";
import SwitchToggle from "./UI/ToggleSwitch";

function App() {
    const [theme, setTheme] = useState("");

    useEffect(() => {
        if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
            setTheme("dark");
        } else {
            setTheme("light");
        }
    }, []);

    useEffect(() => {
        if (theme == "dark") {
            document.documentElement.classList.add("dark");
        } else {
            document.documentElement.classList.remove("dark");
        }
    }, [theme]);

    const themeSwitch = () => {
        setTheme(theme === "dark" ? "light" : "dark");
    };

    return (
        <div className="min-h-screen bg-zinc-100 text-gray-900 font-sans dark:bg-zinc-900 dark:text-slate-100">
            
            <div className="absolute top-0 right-0 m-3 sm:m-4 dark:text-slate-100 dark:text-opacity-70 flex flex-row items-center text-xs sm:text-base gap-2 z-20">
                Dark
                <SwitchToggle theme={theme} switch={themeSwitch} />
            </div>
            
            <Routes>
                <Route path="home" element={<ProtectedRoute><Sidebar /></ProtectedRoute>}>
                    <Route path="new-company-entry" element={<NewCompanyEntryForm />} />
                    <Route path="select-company" element={<SelectCompany/>} />
                    <Route path="company-entry" element={<CompanyEntryForm/>} />
                    <Route path="department-entry" element={<DepartmentEntryForm/>} />
                    {/* <Route path="bank-entry" element={<BankEntryForm />} />
                    <Route path="category-entry" element={<CategoryEntryForm />} />
                    <Route path="department-entry" element={<DepartmentEntryForm />} />
                    <Route path="designation-entry" element={<DesignationEntryForm />} />
                    <Route path="employee-entry" element={<EmployeeEntryForm />} />
                    <Route path="holiday-entry" element={<HolidayEntryForm />} />
                    <Route path="salary-grade-entry" element={<SalaryGradeEntryForm />} />
                    <Route path="shift-entry" element={<ShiftEntryForm />} /> */}
                    
                </Route>
                <Route path="login" element={<LoginForm />} />
                <Route path="register" element={<RegisterForm />} />
            </Routes>
        </div>
    );
}

export default App;
