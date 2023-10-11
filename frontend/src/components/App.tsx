import Sidebar from './menu/Sidebar';
import { Routes, Route, useParams } from 'react-router-dom';
import LoginForm from './authentication/Login';
import Profile from './authentication/Profile';
import RegisterForm from './authentication/Register';
import ForgotPassform from './authentication/ForgotPassform';
import PassConfirmForm from './authentication/PassConfirmForm';
import NewCompanyEntryForm from './menu/MasterEntry/forms/NewCompanyEntryForm/NewCompanyEntryForm';
import SelectCompany from './menu/MasterEntry/forms/SelectCompany/SelectCompany';
import CompanyEntryForm from './menu/MasterEntry/forms/CompanyEntryForm/CompanyEntryForm';
import DepartmentEntryForm from './menu/MasterEntry/forms/DepartmentEntryForm/DepartmentEntryForm';
import DesignationEntryForm from './menu/MasterEntry/forms/DesignationEntryForm/DesignationEntryForm';
import SalaryGradeEntryForm from './menu/MasterEntry/forms/SalaryGradeEntryForm/SalaryGradeEntryForm';
import RegularRegisterForm from './menu/AdminControlsForm/RegularRegisterForm';
import VisibleCompaniesForm from './menu/AdminControlsForm/VisibleCompaniesForm';
import CategoryEntryForm from './menu/MasterEntry/forms/CategoryEntryForm/CategoryEntryForm';
import BankEntryForm from './menu/MasterEntry/forms/BankEntryForm/BankEntryForm';
import LeaveGradeEntryForm from './menu/MasterEntry/forms/LeaveGradeEntryForm/LeaveGradeEntryForm';
import ShiftEntryForm from './menu/MasterEntry/forms/ShiftEntryForm/ShiftEntryForm';
import HolidayEntryForm from './menu/MasterEntry/forms/HolidayEntryForm/HolidayEntryForm';
import EarningsHeadEntry from './menu/MasterEntry/forms/EarningsHeadEntryForm/EarningsHeadEntry';
// import DeductionsHeadEntryForm from './menu/MasterEntry/forms/DeductionsHeadEntryForm/DeductionsHeadEntryForm';
import EmployeeEntryForm from './menu/MasterEntry/forms/EmployeeEntryForm/EmployeeEntryForm';
import EmployeeSalaryForm from './menu/MasterEntry/forms/EmployeeSalaryForm/EmployeeSalaryForm';
import WeeklyOffHolidayOffForm from './menu/MasterEntry/forms/WeeklyOffHolidayOffForm/WeeklyOffHolidayOffForm';
import PfEsiSetupForm from './menu/MasterEntry/forms/PfEsiSetup/PfEsiSetupForm';
import CalculationsForm from './menu/MasterEntry/forms/CalculationsForm/CalculationsForm';
import EmployeeShiiftsEntryForm from './menu/Transaction/forms/EmployeeShiftsEntry/EmployeeShiiftsEntryForm';
import TimeUpdationForm from './menu/Transaction/forms/TimeUpdationForm/TimeUpdationForm';
import AdvanceUpdationForm from './menu/Transaction/forms/AdvanceUpdationForm/AdvanceUpdationForm';
import SalaryPreparationForm from './menu/Transaction/forms/SalaryPreparationForm/SalaryPreparationForm';
import SalaryOvertimeSheet from './menu/Reports/forms/SalaryOvertimeSheet';

// import store, { persistor } from "./authentication/store/index"
// import { PersistGate } from "redux-persist/integration/react";
// import { Provider } from "react-redux";
import ProtectedRouteProps from './authentication/routes/ProtectedRoute';
import ProtectedRoute from './authentication/routes/ProtectedRoute';
// import { RootState } from './authentication/store/index';
import { useSelector } from 'react-redux';
import { useState, useEffect } from 'react';
import SwitchToggle from './UI/ToggleSwitch';
import Alert from './UI/Alert';

function App() {
	document.documentElement.classList.add('scrollbar');
	// const [theme, setTheme] = useState("");

	// useEffect(() => {
	//     if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
	//         setTheme("dark");
	//     } else {
	//         setTheme("light");
	//     }
	// }, []);

	// useEffect(() => {
	//     if (theme == "dark") {
	//         document.documentElement.classList.add("dark");

	//     } else {
	//         document.documentElement.classList.remove("dark");
	//     }
	// }, [theme]);

	// const themeSwitch = () => {
	//     setTheme(theme === "dark" ? "light" : "dark");
	// };

	return (
		<div className="scroll-pt-50 scrollbar max-h-[100dvh] min-h-[100dvh] overflow-y-auto bg-zinc-100 font-sans text-gray-900 dark:bg-zinc-900 dark:text-slate-100">
			{/* <div className="absolute top-0 right-0 m-3 sm:m-4 dark:text-slate-100 dark:text-opacity-70 flex flex-row items-center text-xs sm:text-base gap-2 z-20">
                Dark
                <SwitchToggle theme={theme} switch={themeSwitch} />
            </div> */}
			<Alert />

			<Routes>
				<Route
					path="home"
					element={
						<ProtectedRoute>
							<Sidebar />
						</ProtectedRoute>
					}
				>
					<Route path="select-company" element={<SelectCompany />} />
					<Route path="master-entry">
						<Route path="new-company-entry" element={<NewCompanyEntryForm />} />

						<Route path="company-entry" element={<CompanyEntryForm />} />
						<Route path="department-entry" element={<DepartmentEntryForm />} />
						<Route path="designation-entry" element={<DesignationEntryForm />} />
						<Route path="salary-grade-entry" element={<SalaryGradeEntryForm />} />
						<Route path="category-entry" element={<CategoryEntryForm />} />
						<Route path="bank-entry" element={<BankEntryForm />} />
						<Route path="leave-grade-entry" element={<LeaveGradeEntryForm />} />
						<Route path="shift-entry" element={<ShiftEntryForm />} />
						<Route path="holiday-entry" element={<HolidayEntryForm />} />
						<Route path="earnings-heads-entry" element={<EarningsHeadEntry />} />
						{/* <Route path="deductions-heads-entry" element={<DeductionsHeadEntryForm />} /> */}
						<Route path="employee-entry" element={<EmployeeEntryForm />} />
						<Route path="employee-salary" element={<EmployeeSalaryForm />} />
						<Route path="weekly-off-holiday-off" element={<WeeklyOffHolidayOffForm />} />
						<Route path="pf-esi-setup" element={<PfEsiSetupForm />} />
						<Route path="calculations" element={<CalculationsForm />} />
					</Route>
					<Route path="transaction">
						<Route path="employee-shifts" element={<EmployeeShiiftsEntryForm />} />
						<Route path="time-updation" element={<TimeUpdationForm />} />
						<Route path="advance-updation" element={<AdvanceUpdationForm />} />
						<Route path="salary-preparation" element={<SalaryPreparationForm />} />
					</Route>
					<Route path="reports">
						<Route path="salary-overtime-sheet" element={<SalaryOvertimeSheet />} />
					</Route>

					{/* <Route path="bank-entry" element={<BankEntryForm />} />
                    <Route path="category-entry" element={<CategoryEntryForm />} />
                    <Route path="employee-entry" element={<EmployeeEntryForm />} />
                    <Route path="holiday-entry" element={<HolidayEntryForm />} />
                    <Route path="shift-entry" element={<ShiftEntryForm />} /> */}
				</Route>

				<Route
					path="admin-controls"
					element={
						<ProtectedRoute>
							<Sidebar />
						</ProtectedRoute>
					}
				>
					<Route path="regular-registration" element={<RegularRegisterForm />} />
					<Route path="visible-companies" element={<VisibleCompaniesForm />} />
				</Route>
				<Route path="login" element={<LoginForm />} />
				<Route path="register" element={<RegisterForm />} />
				<Route path="forgot-password" element={<ForgotPassform />} />
				<Route path="pass-confirm/:uid/:token" element={<PassConfirmForm />} />
			</Routes>
		</div>
	);
}

export default App;
