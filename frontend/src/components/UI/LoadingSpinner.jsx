import React from 'react';
import { FaCircleNotch } from 'react-icons/fa';

const LoadingSpinner = () => (
    <div>
        <div className="mx-auto flex h-fit w-fit items-center rounded bg-blueAccent-600 p-2 dark:bg-blueAccent-700">
            <FaCircleNotch className="mr-2 animate-spin text-gray-900 dark:text-slate-100" />
            <p className="text-gray-900 dark:text-slate-100">Processing...</p>
        </div>
    </div>
);

export default LoadingSpinner;
