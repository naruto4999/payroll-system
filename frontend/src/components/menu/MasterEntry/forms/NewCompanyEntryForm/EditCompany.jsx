import React from "react";

const EditCompany = ({ editCompanyPopoverHandler, updatedCompanyChangeHandler, updateButtonClicked }) => {
    return (
        <div className="text-gray-900 dark:text-slate-100">
            <h1 className="font-medium text-2xl mb-2">Edit Company</h1>

            <form action="" className="flex flex-col gap-2 justify-center">
                <label
                    htmlFor="comapny-name"
                    className="text-black font-medium text-opacity-100 dark:text-white dark:text-opacity-70 text-sm"
                >
                    Company Name
                </label>
                <div className="relative">
                    <input
                        className="rounded bg-opacity-50 bg-zinc-50 dark:bg-zinc-700  border-2 border-gray-800 border-opacity-25 dark:border-opacity-25 dark:border-slate-100 p-1 outline-none focus:border-opacity-100 dark:focus:border-opacity-75 transition w-full"
                        type="text"
                        id="comapny-name"
                        name="comapny-name"
                        // value={newCompany}
                        placeholder=" "
                        onChange={updatedCompanyChangeHandler}
                    />
                </div>
            </form>
            <section className="flex flex-row gap-4 mt-4 mb-2">
                <button
                    className="bg-teal-500 hover:bg-teal-600 dark:bg-teal-700 rounded w-20 p-2 text-base font-medium dark:hover:bg-teal-600"
                    onClick={updateButtonClicked}
                >
                    Update
                </button>
                <button
                    className="bg-zinc-400 hover:bg-zinc-500 dark:bg-zinc-600 rounded w-20 p-2 text-base font-medium dark:hover:bg-zinc-700"
                    onClick={() => editCompanyPopoverHandler({id: "", name: ""})}
                >
                    Cancel
                </button>
            </section>
        </div>
    );
};

export default EditCompany;
