import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
    return (
        <div className="relative flex min-h-screen flex-col items-center justify-center bg-gray-900 bg-opacity-80 text-white">
            <svg
                className="absolute inset-0 h-full w-full opacity-20"
                viewBox="0 0 100 100"
                preserveAspectRatio="xMidYMid slice"
                fill="currentColor"
            >
                <circle cx="50" cy="50" r="40" />
            </svg>
            <header className="mb-8 text-center">
                <h1 className="animate__animated animate__fadeIn text-5xl font-extrabold dark:text-blueAccent-500">
                    Welcome to Pay-Per
                </h1>
                <p className="animate__animated animate__fadeIn mt-4 text-lg">
                    Automate employee management and salary generation with ease. Generate 38 comprehensive reports at
                    the press of a button. Fully compatible for use on mobile devices.
                </p>
            </header>
            <div className="flex space-x-4">
                <Link to="/login">
                    <button className="transform rounded bg-teal-500 px-6 py-2 text-lg font-medium transition duration-300 hover:scale-105 hover:bg-teal-600">
                        Login
                    </button>
                </Link>
                <Link to="/register">
                    <button className="transform rounded bg-blue-500 px-6 py-2 text-lg font-medium transition duration-300 hover:scale-105 hover:bg-blue-600">
                        Register
                    </button>
                </Link>
            </div>
        </div>
    );
};

export default LandingPage;
