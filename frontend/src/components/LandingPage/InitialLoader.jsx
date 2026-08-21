import React from 'react';
import './InitialLoader.css';

const InitialLoader = () => {
    return (
        <div className="initial-loader">
            <div className="loader-container">
                <div className="loader-logo">
                    <img
                        src={`${import.meta.env.VITE_PUBLIC_URL}logo_full_dark.svg`}
                        alt="Loading..."
                        className="loader-image"
                    />
                </div>
                <div className="loader-spinner">
                    <div className="spinner-ring"></div>
                </div>
                <div className="loader-text">
                    Loading...
                </div>
            </div>
        </div>
    );
};

export default InitialLoader;