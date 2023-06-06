import React from "react";
import { useGetCompaniesQuery } from "../../../../authentication/api/newCompanyEntryApiSlice";
import { globalCompanyActions } from "../../../../authentication/store/slices/globalCompany";
import { useSelector, useDispatch } from "react-redux";
import { useOutletContext } from "react-router-dom";
import { useEffect } from "react";
import { FaCheck } from "react-icons/fa";

const classNames = (...classes) => {
    return classes.filter(Boolean).join(" ");
};

const SelectCompany = () => {
    const { data: fetchedData, isLoading, isSuccess, isError, error } = useGetCompaniesQuery();
    const [showLoadingBar, setShowLoadingBar] = useOutletContext();
    // console.log(fetchedData);
    const globalCompany = useSelector((state) => state.globalCompany);
    const dispatch = useDispatch();
    // console.log(globalCompany);

    const val = 1;
    const handler = (company) => {
        // console.log(company);
        dispatch(globalCompanyActions.setCompany({ id: company.id, name: company.name }));
    };

    useEffect(() => {
        setShowLoadingBar(isLoading);
    }, [isLoading]);

    if (isLoading) {
        return <div></div>;
    } else {
        return (
            <section className="mx-6 mt-2">
                <div className="">
                    <h1 className="text-3xl font-medium">Select a Company</h1>
                    <p className="text-sm my-2">Select a company to work on</p>
                    <div className="mt-6 flex flex-row flex-wrap gap-14 md:gap-20 justify-center ">
                        {fetchedData.map((data) => {
                            return (
                                <button
                                    key={data.id}
                                    className={classNames(
                                        globalCompany.id == data.id
                                            ? "dark:bg-blueAccent-700 bg-blueAccent-600 scale-125"
                                            : "dark:hover:bg-teal-700 hover:bg-teal-600 md:hover:scale-125 dark:bg-zinc-800 bg-zinc-200",
                                        "h-32 w-60 p-6 md:h-40 md:w-96 md:p-10 rounded cursor-pointer transition-transform relative"
                                    )}
                                    onClick={() => handler(data)}
                                    value={val}
                                >
                                    {globalCompany.id == data.id ? (
                                        <FaCheck className="absolute scale-150 left-1/2 -translate-y-5 -translate-x-1/2" />
                                    ) : (
                                        ""
                                    )}
                                    <h1 className="text-xl">{data.name}</h1>
                                </button>
                            );
                        })}
                    </div>
                </div>
            </section>
        );
    }
};
export default SelectCompany;
