import React from "react";
import { useGetCompaniesQuery } from "../../../../authentication/api/newCompanyEntryApiSlice";

const SelectCompany = () => {
    const { data: fetchedData, isLoading, isSuccess, isError, error } = useGetCompaniesQuery();
    console.log(fetchedData);

    const val = 1;
    const handler = (id) => {
        console.log(id);
    };

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
                                className="h-32 w-60 p-6 md:h-40 md:w-96 md:p-10 bg-zinc-800 rounded hover:bg-teal-700 cursor-pointer hover:scale-125 transition-transform"
                                onClick={() => handler(data.id)}
                                value={val}
                            >
                                <h1 className="text-xl">{data.name}</h1>
                            </button>
                        );
                    })}
                </div>
            </div>
        </section>
    );
};
export default SelectCompany;
