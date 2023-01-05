import { FaUserTie, FaPlus, FaPen, FaHome } from "react-icons/fa";

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
                title: "Anime",
                children: [
                    {
                        title: "Naruto",
                        path: "/home"
                    },
                ],
            },
        ],
    },
];
export default items;
