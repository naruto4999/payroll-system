import {
	FaUserTie,
	FaPlus,
	FaPen,
	FaHome,
	FaThLarge,
	FaLevelUpAlt,
	FaMoneyCheckAlt,
	FaCogs,
	FaUserShield,
	FaUsersCog,
	FaEye,
} from 'react-icons/fa';
import {
	FaMountainSun,
	FaMoneyBill1,
	FaDollarSign,
	FaArrowTrendDown,
	FaPerson,
	FaCalendarCheck,
	FaBoxesStacked,
	FaCircleArrowRight,
	FaCalculator,
	FaTableList,
	FaBusinessTime,
	FaNewspaper,
	FaFilePdf,
	FaChalkboardUser,
	FaMoneyBillTrendUp,
} from 'react-icons/fa6';

const menuItems = [
	{
		title: 'Master Entry',
		icon: FaUserTie,
		children: [
			{
				title: 'Add New Company',
				icon: FaPlus,
				path: '/home/master-entry/new-company-entry',
			},
			{
				title: 'Company Entry',
				icon: FaPen,
				path: '/home/master-entry/company-entry',
			},
			{
				title: 'Department Entry',
				icon: FaThLarge,
				path: '/home/master-entry/department-entry',
			},
			{
				title: 'Designation Entry',
				icon: FaLevelUpAlt,
				path: '/home/master-entry/designation-entry',
			},
			{
				title: 'Salary Grade Entry',
				icon: FaMoneyCheckAlt,
				path: '/home/master-entry/salary-grade-entry',
			},
			{
				title: 'Category Entry',
				icon: FaMoneyCheckAlt,
				path: '/home/master-entry/category-entry',
			},
			{
				title: 'Bank Entry',
				icon: FaMoneyCheckAlt,
				path: '/home/master-entry/bank-entry',
			},
			{
				title: 'Leave Grade Entry',
				icon: FaMoneyCheckAlt,
				path: '/home/master-entry/leave-grade-entry',
			},
			{
				title: 'Shift Entry',
				icon: FaBusinessTime,
				path: '/home/master-entry/shift-entry',
			},
			{
				title: 'Holiday Entry',
				icon: FaMountainSun,
				path: '/home/master-entry/holiday-entry',
			},
			{
				title: 'Heads Entry',
				icon: FaMoneyBill1,
				children: [
					{
						title: 'Earnings',
						icon: FaDollarSign,
						path: '/home/master-entry/earnings-heads-entry',
					},
					// {
					// 	title: 'Deductions',
					// 	icon: FaDollarSign,
					// 	path: '/home/master-entry/deductions-heads-entry',
					// },
				],
			},
			{
				title: 'Employee Entry',
				icon: FaPerson,
				path: '/home/master-entry/employee-entry',
			},
			{
				title: 'Employee Salary',
				icon: FaDollarSign,
				path: '/home/master-entry/employee-salary',
			},
			{
				title: 'Weekly / Holiday Off',
				icon: FaCalendarCheck,
				path: '/home/master-entry/weekly-off-holiday-off',
			},
			{
				title: 'Setup Entry',
				icon: FaBoxesStacked,
				children: [
					{
						title: 'ESI/PF Setup',
						icon: FaCircleArrowRight,
						path: '/home/master-entry/pf-esi-setup',
					},
					{
						title: 'Calculations',
						icon: FaCalculator,
						path: '/home/master-entry/calculations',
					},
				],
			},
		],
	},
	{
		title: 'Transaction',
		icon: FaTableList,
		children: [
			{
				title: 'Employee Shifts Entry',
				icon: FaBusinessTime,
				path: '/home/transaction/employee-shifts',
			},
			{
				title: 'Time Updation',
				icon: FaBusinessTime,
				path: '/home/transaction/time-updation',
			},
			{
				title: 'Advance Updation',
				icon: FaMoneyBill1,
				path: '/home/transaction/advance-updation',
			},
			{
				title: 'Salary Preparation',
				icon: FaMoneyBill1,
				path: '/home/transaction/salary-preparation',
			},
			{
				title: 'Bonus Calculation',
				icon: FaMoneyBillTrendUp,
				path: '/home/transaction/bonus-calculation',
			},
			{
				title: 'Resignation',
				icon: FaChalkboardUser,
				path: '/home/transaction/resignation',
			},
		],
	},
	{
		title: 'Reports',
		icon: FaNewspaper,
		children: [
			{
				title: 'Personnel File Forms',
				icon: FaFilePdf,
				path: '/home/reports/personnel-file-forms',
			},
			{
				title: 'Salary/Overtime Sheet',
				icon: FaFilePdf,
				path: '/home/reports/salary-overtime-sheet',
			},
			{
				title: 'Attendance/Bonus',
				icon: FaFilePdf,
				path: '/home/reports/attendance-reports',
			},
			{
				title: 'PF/ESI Reports',
				icon: FaFilePdf,
				path: '/home/reports/pf-esi-reports',
			},
		],
	},

	{
		title: 'Settings',
		icon: FaCogs,
		children: [],
	},
	{
		title: 'Admin Controls',
		icon: FaUserShield,
		children: [
			{
				title: 'Create / Manage SubUser',
				icon: FaUsersCog,
				path: '/admin-controls/regular-registration',
			},
			{
				title: 'Visible Companies',
				icon: FaEye,
				path: '/admin-controls/visible-companies',
			},
		],
	},
];
export default menuItems;
