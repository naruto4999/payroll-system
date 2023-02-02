import React from "react";
import { useSelector } from "react-redux";

// COnver Tin Number to GST in backend
const CompanyEntryForm = () => {
    const globalCompany = useSelector((state) => state.globalCompany);

    if (globalCompany.id == null) {
        return (
            <section className="flex flex-col items-center">
                <h4 className="mt-10 text-x text-redAccent-500 dark:text-redAccent-600 font-bold">Please Select a Company First</h4>
            </section>
        );
    }
    return (
        <section className="mx-6 mt-2">
            <div className="flex flex-row place-content-between flex-wrap gap-4">
                <div>
                    <h1 className="text-3xl font-medium">Company Details</h1>
                    <p className="text-sm my-2">Add/Edit details of selected company here</p>
                </div>
                <div className="">
                    <button
                        type="submit"
                        form="company-entry-form"
                        className="dark:bg-teal-700 w-20 rounded p-2 text-base font-medium bg-teal-500 hover:bg-teal-600 dark:hover:bg-teal-600 mr-4"
                    >
                        Save
                    </button>
                    <button className="bg-zinc-400 hover:bg-zinc-500 dark:bg-zinc-700 dark:hover:bg-zinc-600 w-20 rounded p-2 text-base font-medium">
                        Edit
                    </button>
                </div>
            </div>
            <form id="company-entry-form" className="mt-2">
                <div className="flex flex-col w-full gap-2">
                    <div>
                        <label
                            for="name"
                            className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                        >
                            Name
                        </label>
                        <input
                            type="text"
                            name="name"
                            id="name"
                            className="dark:bg-zinc-800 bg-slate-200 dark:text-slate-400 text-slate-500 rounded p-2 w-full lg:w-fit"
                            value={globalCompany.name}
                            disabled
                            size={globalCompany.name.length}
                        />
                    </div>
                    <div>
                        <label
                            for="address"
                            className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                        >
                            Address1
                        </label>
                        <input
                            type="text"
                            name="address"
                            id="address"
                            className="dark:bg-zinc-800 bg-slate-200 col-span-3 rounded p-2 w-full lg:w-3/4"
                        />
                    </div>
                    <div>
                        <label
                            for="key-person"
                            className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                        >
                            Key Person
                        </label>
                        <input
                            type="text"
                            name="key-person"
                            id="key-person"
                            className="dark:bg-zinc-800 bg-slate-200 col-span-2 rounded p-2 min-w-fit w-1/3"
                        />
                    </div>
                    <div>
                        <label
                            for="involving-industry"
                            className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                        >
                            Involving Industry
                        </label>
                        <input
                            type="text"
                            name="involving-industry"
                            id="involving-industry"
                            className="dark:bg-zinc-800 bg-slate-200 col-span-2 rounded p-2 w-1/3 min-w-fit"
                        />
                    </div>

                    <div>
                        <label
                            for="number"
                            className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                        >
                            Phone Number
                        </label>
                        <input
                            type="tel"
                            maxLength="10"
                            minLength="10"
                            name="number"
                            id="number"
                            className="dark:bg-zinc-800 bg-slate-200 col-span-1 rounded p-2"
                            size="10"
                        />
                    </div>

                    <div>
                        <label
                            for="email"
                            className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                        >
                            Email
                        </label>
                        <input
                            type="email"
                            name="email"
                            id="email"
                            className="dark:bg-zinc-800 bg-slate-200 col-span-2 rounded p-2 w-1/4 min-w-fit"
                            size="30"
                        />
                    </div>
                    <div>
                        <label
                            for="pf-number"
                            className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                        >
                            P.F Number
                        </label>
                        <input
                            type="text"
                            name="pf-number"
                            id="pf-number"
                            className="dark:bg-zinc-800 bg-slate-200 col-span-2 rounded p-2"
                            minLength="22"
                            maxLength="22"
                            size="22"
                        />
                    </div>
                    <div>
                        <label
                            for="esi-number"
                            className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                        >
                            E.S.I Number
                        </label>
                        <input
                            type="number"
                            name="esi-number"
                            id="esi-number"
                            className="dark:bg-zinc-800 bg-slate-200 col-span-2 rounded p-2"
                            maxLength="17"
                            minLength="17"
                            size="17"
                        />
                    </div>

                    <div>
                        <label
                            for="head-office-address"
                            className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                        >
                            Head Office Address
                        </label>
                        <input
                            type="text"
                            name="head-office-address"
                            id="head-office-address"
                            className="dark:bg-zinc-800 bg-slate-200 col-span-3 rounded p-2 w-full lg:w-3/4"
                        />
                    </div>

                    <div>
                        <label
                            for="pan-number"
                            className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                        >
                            Pan Number
                        </label>
                        <input
                            type="text"
                            maxLength="10"
                            minLength="10"
                            name="pan-number"
                            id="pan-number"
                            className="dark:bg-zinc-800 bg-slate-200 rounded p-2"
                            size="10"
                        />
                    </div>

                    <div>
                        <label
                            for="gst-number"
                            className="my-auto dark:text-blueAccent-400 text-blueAccent-700 font-medium block"
                        >
                            GST Number
                        </label>
                        <input
                            type="text"
                            maxLength="15"
                            minLength="15"
                            name="gst-number"
                            id="gst-number"
                            className="dark:bg-zinc-800 bg-slate-200 col-span-1 rounded p-2"
                            size="15"
                        />
                    </div>
                </div>
            </form>
        </section>
    );
};
export default CompanyEntryForm;
