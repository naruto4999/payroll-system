import { FaUserTie, FaPlus, FaPen, FaHome, FaThLarge, FaLevelUpAlt, FaMoneyCheckAlt, FaCogs,FaUserShield , FaUsersCog, FaEye, FaBusinessTime} from "react-icons/fa";

const menuItems = [
    {
        title: "Master Entry",
        icon: FaUserTie,
        children: [
            {
                title: "Add New Company",
                icon: FaPlus,
                path: "/home/new-company-entry",
            },
            {
                title: "Company Entry",
                icon: FaPen,
                path: "/home/company-entry",
            },
            {
                title: "Department Entry",
                icon: FaThLarge,
                path: "/home/department-entry"
            },
            {
                title: "Designation Entry",
                icon: FaLevelUpAlt,
                path: "/home/designation-entry"
            },
            {
                title: "Salary Grade Entry",
                icon: FaMoneyCheckAlt,
                path: "/home/salary-grade-entry"
            },
            {
                title: "Category Entry",
                icon: FaMoneyCheckAlt,
                path: "/home/category-entry"
            },
            {
                title: "Bank Entry",
                icon: FaMoneyCheckAlt,
                path: "/home/bank-entry"
            },
            {
                title: "Leave Grade Entry",
                icon: FaMoneyCheckAlt,
                path: "/home/leave-grade-entry"
            },
            {
                title: "Shift Entry",
                icon: FaBusinessTime,
                path: "/home/shift-entry"
            },
        ],
    },
    {
        title: "Settings",
        icon: FaCogs,
        children: [
            
        ]
    },
    {
        title: "Admin Controls",
        icon: FaUserShield,
        children: [
            {
                title: "Create / Manage SubUser",
                icon: FaUsersCog,
                path: "/admin-controls/regular-registration"
            },
            {
                title: "Visible Companies",
                icon: FaEye,
                path: "/admin-controls/visible-companies"
            }
        ]
    }
];
export default menuItems;
