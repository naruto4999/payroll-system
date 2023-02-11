import { FaUserTie, FaPlus, FaPen, FaHome, FaThLarge } from "react-icons/fa";

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
        ],
    },
];
export default items;
