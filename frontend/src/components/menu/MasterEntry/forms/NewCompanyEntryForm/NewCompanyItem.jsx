// Delete this component cuz not in use now or check
import React from "react";
import { FaRegTrashAlt, FaPen } from "react-icons/fa";
import { useState } from "react"

const NewCompanyItem = ({item, deleteButtonClicked}) => {
    const [selectedCompany, setSelectedCompany] = useState("");

    const trashClicked = (event) => {
        setSelectedCompany(event.currentTarget.id)
        console.log(selectedCompany)
        // deleteButtonClicked(selectedCompany)
    }

    // console.log(item)
    return (
        <tr className="dark:hover:bg-zinc-800 hover:bg-zinc-200">
            <td className="px-6 py-4 font-normal">
                <div className="text-sm">
                    <div className="font-medium">{item.id}</div>
                </div>
            </td>
            <td className="px-6 py-4 font-normal">
                <div className="text-sm">
                    <div className="font-medium">{item.name}</div>
                </div>
            </td>
            <td className="px-6">
                <div className="flex justify-end gap-4">
                    <FaRegTrashAlt className="h-4 dark:hover:text-redAccent-600 hover:text-redAccent-500" id={item.id} onClick={trashClicked}/>
                    <FaPen className="h-4 dark:hover:text-teal-600 hover:text-teal-500"/>
                </div>
            </td>
        </tr>
    );
};

export default NewCompanyItem;
