import { FaUserTie, FaPlus, FaPen, FaHome, FaThLarge, FaLevelUpAlt } from "react-icons/fa";

const items = [
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
            }
        ],
    },
];
export default items;
