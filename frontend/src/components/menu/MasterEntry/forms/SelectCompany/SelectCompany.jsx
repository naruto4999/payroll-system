import React from "react";

const SelectCompany = () => {
    const handler = (event) => {
        console.log(event.target)
        console.log(event.target.value)
    }

    return (
        <section>
            <div className="mx-5 mt-2">
                <h1 className="text-3xl font-medium">Select a Company</h1>
                <p className="text-sm my-2">Select a company to work on</p>

                <button className="flex flex-row flex-wrap"  onClick={handler}>
                    <div className="p-10 bg-zinc-800 rounded hover:bg-teal-700 cursor-pointer" value='2'>
                        <h1 className="text-xl">Neelambarai Pvt. Ltd.</h1>
                    </div>
                </button>
            </div>
        </section>
    );
};
export default SelectCompany;
