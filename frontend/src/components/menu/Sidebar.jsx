import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { useSelector } from "react-redux";
import { authActions } from "../authentication/store/slices/auth";
import { globalCompanyActions } from "../authentication/store/slices/globalCompany";
import { FaRegWindowClose, FaRegBuilding, FaChevronDown, FaBars, FaSignOutAlt } from "react-icons/fa";
import SidebarItem from "./SidebarItem";
import menuItems from "./SidebarData";
import { Outlet } from "react-router-dom";
import { NavLink } from "react-router-dom";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const Sidebar = () => {
    const dispatch = useDispatch();
    const handleLogout = () => {
        dispatch(authActions.logout());
        dispatch(globalCompanyActions.deselectComapny());
    };
    const auth = useSelector((state) => state.auth);
    let items = menuItems.filter((item) => item.title !== "Admin Controls")
    console.log(auth)
    if (auth.account.role == "OWNER" && auth.account.is_staff == true) {
        items = menuItems
        // const items = itemsWithoutAdminControl
    }
    const [showSidebar, setShowSidebar] = useState(true);
    const [showLoadingBar, setShowLoadingBar] = useState(false);
    const sidebarHandler = () => {
        setShowSidebar(!showSidebar);
    };
    console.log();

    return (
        <section className="flex flex-row gap-0 relative">
            <div>
                {/* <button
                className="absolute bottom-0 right-0 bg-teal-700 h-10 rounded-lg p-2 hover:bg-teal-600"
                onClick={handleLogout}
            >
                Bish me Logout uwu
            </button> */}

                <div
                    className={classNames(
                        showSidebar == false ? "" : "hidden",
                        "absolute text-4xl top-3 left-3 cursor-pointer z-40"
                    )}
                    onClick={sidebarHandler}
                >
                    <FaBars className="h-6" />
                </div>
                <div
                    className={classNames(
                        showSidebar == false ? "-ml-80" : "md:flex-shrink-0",
                        "md:sticky fixed h-screen top-0 bottom-0 p-2 w-[300px] overflow-y-auto dark:bg-black md:dark:bg-opacity-40 dark:bg-opacity-90 bg-zinc-200 bg-opacity-70 transition-all duration-300 z-20"
                    )}
                >
                    <div className="text-xl">
                        <div className="p-2.5 mt-1 flex items-center">
                            <h1 className="font-bold text-xl ml-3">PAY-PER</h1>
                            <FaRegWindowClose
                                className="cursor-pointer absolute right-0 mx-4"
                                onClick={sidebarHandler}
                            />
                        </div>

                        {/* Line Divide */}
                        <div className="my-2 bg-gray-600 h-[1px]"></div>
                    </div>

                    <NavLink
                        className="p-2.5 mt-3 flex items-center rounded-md px-4 duration-300 cursor-pointer hover:bg-teal-500 dark:hover:bg-teal-600"
                        to="/home/select-company"
                    >
                        <FaRegBuilding />
                        <span className="text-[15px] ml-4 font-bold">Select Company</span>
                    </NavLink>

                    <div className="my-4 bg-gray-600 h-[1px]"></div>

                    {/* Sidebar Items go here */}
                    {items.map((item, index) => (
                        <SidebarItem key={index} item={item} />
                    ))}

                    <div
                        className="p-2.5 mt-3 flex items-center rounded-md px-4 duration-300 cursor-pointer hover:bg-teal-500 dark:hover:bg-teal-600"
                        onClick={handleLogout}
                    >
                        <FaSignOutAlt />
                        <span className="text-[15px] ml-4 font-bold">Logout</span>
                    </div>
                </div>
            </div>
            <div
                className={classNames(
                    showLoadingBar == true ? "" : "hidden",
                    "fixed w-10 sm:w-14 top-0 h-1 bg-orange-700 dark:bg-orange-200 md:animate-loading-bar animate-[loading-bar_1s_infinite_linear] sm:animate-[loading-bar_1.5s_infinite_linear] overflow-x:hidden z-50"
                )}
            ></div>

            <div className="grow relative">
                <div className="top-0 h-[40px]"></div>
                <Outlet context={[showLoadingBar, setShowLoadingBar]} />
            </div>
        </section>
    );
};

export default Sidebar;
