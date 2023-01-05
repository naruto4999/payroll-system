import React from "react";
import { useState } from "react";
import { FaChevronUp } from "react-icons/fa";
import { NavLink } from "react-router-dom";

const classNames = (...classes) => {
    // console.log(classes)
    return classes.filter(Boolean).join(" ");
};

const SidebarItem = ({ item }) => {
    const [upArrow, setUpArrow] = useState(false);
    const [showDiv, setShowDiv] = useState(false);
    const submenuHandler = () => {
        setUpArrow(!upArrow);
        setShowDiv(!showDiv);
    };

    if (item.children) {
        return (
            <div>
                <div
                    className="z-50 p-2.5 mt-3 flex items-center rounded-md px-4 duration-300 cursor-pointer hover:bg-teal-500 dark:hover:bg-teal-600"
                    id="masterEntry"
                    onClick={submenuHandler}
                >
                    {item.icon ? <item.icon /> : ""}
                    <div className="flex justify-between w-full items-center">
                        <span className="text-[15px] ml-4 font-bold">{item.title}</span>
                        <span className="text-sm rotate-180" id="arrow">
                            <FaChevronUp
                                className={classNames(
                                    upArrow == true ? "rotate-180" : "rotate-0",
                                    "transition-transform"
                                )}
                            />
                        </span>
                    </div>
                </div>
                <div
                    className={classNames(
                        showDiv == false ? "hidden" : "",
                        "text-left text-sm mt-2 w-4/5 mx-auto font-bold"
                    )}
                    id="submenu"
                >
                    {item.children.map((child, index) => (
                        <SidebarItem key={index} item={child} />
                    ))}
                </div>
            </div>
        );
    } else {
        return (
            <div>
                <NavLink
                    className="z-50 p-2.5 mt-3 flex items-center rounded-md px-4 duration-300 cursor-pointer hover:bg-teal-500 dark:hover:bg-teal-600"
                    id="masterEntry"
                    to={item.path}
                >
                    {item.icon ? <item.icon /> : ""}
                    <div className="flex justify-between w-full items-center">
                        <span className="text-[15px] ml-4 font-bold">{item.title}</span>
                    </div>
                </NavLink>
            </div>
        );
    }
};

export default SidebarItem;
