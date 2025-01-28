import React from 'react';
import ReactModal from 'react-modal';
import { useOutletContext } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { alertActions } from '../../../../authentication/store/slices/alertSlice';
import { authActions } from '../../../../authentication/store/slices/auth';

const classNames = (...classes) => {
    return classes.filter(Boolean).join(' ');
};

const AddEditEmployeeUsingExcel = ({
    showAddEditEmployeeUsingExcel,
    setShowAddEditEmployeeUsingExcel,
    downloadTemplate,
    handleFileUpload,
    uploadEmployees,
}) => {
    const [showLoadingBar, setShowLoadingBar] = useOutletContext();
    const globalCompany = useSelector((state) => state.globalCompany);
    const auth = useSelector((state) => state.auth);
    const dispatch = useDispatch();

    const generateTemplate = async (values, formikBag) => {
        setShowLoadingBar(true);

        // Prepare file name for the template
        const fileName = 'employee_template.xlsx'; // Static filename for the template

        // Fetch options
        const requestOptions = {
            method: 'POST', // Use GET for downloading templates
            headers: {
                Authorization: `Bearer ${auth.token}`,
                'Content-Type': 'application/json', // Set Content-Type if needed
            },
            body: JSON.stringify({ company: globalCompany.id }),
        };

        const downloadTemplate = async () => {
            try {
                const response = await fetch(
                    `${import.meta.env.VITE_BACKEND_URL}api/download-employee-excel-template`,
                    requestOptions
                );

                if (response.status === 401) {
                    console.log('Received a 401 status, attempting to refresh the token...');

                    // Refresh token
                    const refreshResponse = await fetch(`${import.meta.env.VITE_BACKEND_URL}api/auth/refresh/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ refresh: auth.refreshToken }),
                    });

                    if (refreshResponse.status === 200) {
                        const refreshData = await refreshResponse.json();

                        if (refreshData.access && refreshData.refresh) {
                            dispatch(
                                authActions.setAuthTokens({
                                    token: refreshData.access,
                                    refreshToken: refreshData.refresh,
                                })
                            );

                            // Retry template download with refreshed token
                            const refreshedResponse = await fetch(
                                `${import.meta.env.VITE_BACKEND_URL}api/download-employee-template/`,
                                {
                                    ...requestOptions,
                                    headers: {
                                        Authorization: `Bearer ${refreshData.access}`,
                                    },
                                }
                            );

                            if (refreshedResponse.status === 200) {
                                const excelData = await refreshedResponse.blob();
                                const downloadUrl = URL.createObjectURL(excelData);

                                const downloadLink = document.createElement('a');
                                downloadLink.href = downloadUrl;
                                downloadLink.download = fileName;
                                document.body.appendChild(downloadLink);

                                downloadLink.click(); // Trigger download
                                document.body.removeChild(downloadLink); // Remove element

                                dispatch(
                                    alertActions.createAlert({
                                        message: 'Template downloaded successfully!',
                                        type: 'Success',
                                        duration: 8000,
                                    })
                                );
                            } else {
                                console.log('Error downloading template after token refresh');
                                dispatch(
                                    alertActions.createAlert({
                                        message: 'Error occurred while downloading template',
                                        type: 'Error',
                                        duration: 5000,
                                    })
                                );
                            }
                        }
                    } else {
                        console.log('Error refreshing token');
                        dispatch(
                            alertActions.createAlert({
                                message: 'Session expired. Please log in again.',
                                type: 'Error',
                                duration: 5000,
                            })
                        );
                        dispatch(authActions.logout());
                    }
                } else if (response.status !== 200) {
                    console.error('Request failed with status:', response.status);
                    response.json().then((data) => {
                        console.log('Error:', data.detail);
                        dispatch(
                            alertActions.createAlert({
                                message: data.detail || 'Error occurred while downloading template',
                                type: 'Error',
                                duration: 5000,
                            })
                        );
                    });
                } else if (response.status === 200) {
                    const excelData = await response.blob();
                    const downloadUrl = URL.createObjectURL(excelData);

                    const downloadLink = document.createElement('a');
                    downloadLink.href = downloadUrl;
                    downloadLink.download = fileName;
                    document.body.appendChild(downloadLink);

                    downloadLink.click(); // Trigger download
                    document.body.removeChild(downloadLink); // Remove element

                    dispatch(
                        alertActions.createAlert({
                            message: 'Template downloaded successfully!',
                            type: 'Success',
                            duration: 8000,
                        })
                    );
                }
            } catch (error) {
                console.error('Fetch error:', error);
                dispatch(
                    alertActions.createAlert({
                        message: 'Error occurred while downloading template',
                        type: 'Error',
                        duration: 5000,
                    })
                );
            }
            console.log('about to turn off loading bar');

            setShowLoadingBar(false); // Hide loading bar
        };

        // Initiate template download
        downloadTemplate();
    };

    return (
        <ReactModal
            className="items-left scrollbar fixed inset-0 mx-2 my-auto flex h-fit max-h-[100dvh] w-fit flex-col gap-4 overflow-y-scroll rounded bg-zinc-300 p-4 shadow-xl dark:bg-zinc-800 sm:mx-auto sm:max-w-lg"
            isOpen={showAddEditEmployeeUsingExcel}
            onRequestClose={() => setShowAddEditEmployeeUsingExcel(false)}
            style={{
                overlay: {
                    backgroundColor: 'rgba(0, 0, 0, 0.75)',
                },
            }}
        >
            <div className="text-gray-900 dark:text-slate-100">
                <h2 className="mb-2 text-2xl font-medium">Upload Employees via Excel</h2>
                <p className="mb-2 text-sm">Please follow the instructions below to upload employees:</p>
                <ul className="text-sm">
                    <li>1. Download the template using the button below.</li>
                    <li>2. Fill in the required details for each employee.</li>
                    <li>3. Upload the completed Excel file.</li>
                </ul>
                <button
                    //className="mt-4 rounded bg-green-500 p-2 text-base font-medium hover:bg-green-600"
                    className="mt-4 rounded bg-blueAccent-400 p-2 text-sm font-medium hover:bg-blueAccent-500 dark:bg-blueAccent-700 dark:hover:bg-blueAccent-600"
                    onClick={generateTemplate}
                >
                    Download Template
                </button>
                <input
                    type="file"
                    accept=".xlsx, .xls"
                    onChange={handleFileUpload}
                    className="mt-4 block w-full cursor-pointer rounded border border-gray-300 bg-gray-50 text-sm file:border-0 file:bg-zinc-600 file:py-1 file:px-4 file:text-sm file:font-semibold file:text-white hover:file:cursor-pointer hover:file:bg-zinc-700 focus:outline-none dark:border-gray-600 dark:bg-zinc-900 dark:placeholder-gray-400"
                />
                <button
                    //className="mt-4 rounded bg-teal-500 p-2 text-base font-medium hover:bg-teal-600"
                    className={classNames(
                        true && !false ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
                        'mt-4 w-24 rounded bg-teal-500 p-2 text-sm font-medium dark:bg-teal-700'
                    )}
                    onClick={uploadEmployees}
                >
                    Upload
                </button>
            </div>
        </ReactModal>
    );
};

export default AddEditEmployeeUsingExcel;
