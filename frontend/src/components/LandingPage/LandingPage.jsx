import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import InitialLoader from './InitialLoader';
import CalendarFeature from './calenderFeature';
import './LandingPage.css';

const LandingPage = () => {
    const [isVisible, setIsVisible] = useState(false);
    const [showLoader, setShowLoader] = useState(true);
    const [showButtonLoader, setShowButtonLoader] = useState(false);

    useEffect(() => {
        // Show loader for 2 seconds
        const loaderTimer = setTimeout(() => {
            setShowLoader(false);
        }, 500);

        // Start main content animation after loader
        const contentTimer = setTimeout(() => {
            setIsVisible(true);
        }, 500);

        return () => {
            clearTimeout(loaderTimer);
            clearTimeout(contentTimer);
        };
    }, []);

    const handleButtonClick = (path) => {
        setShowButtonLoader(true);
        
        // Navigate after 2 seconds
        setTimeout(() => {
            window.location.href = path;
        }, 500);
    };

    // Show loader for first 2 seconds or when button is clicked
    if (showLoader || showButtonLoader) {
        return <InitialLoader />;
    }

    return (
        <div className="landing-page">
            {/* Animated Background Elements */}
            <div className="background-container">
                {/* Floating Circles */}
                <div className="floating-circle-1"></div>
                <div className="floating-circle-2"></div>
                <div className="floating-circle-3"></div>
                <div className="floating-circle-4"></div>
                
                {/* Grid Pattern */}
                <div className="grid-pattern">
                    <div className="grid-pattern-bg"></div>
                </div>
            </div>

            {/* Calendar Feature */}
            <div className="calendar-feature-container">
                <CalendarFeature />
            </div>

            {/* Main Content */}
            <div className="main-content">
                {/* Hero Section */}
                <div className={`hero-section ${isVisible ? 'visible' : 'hidden'}`}>
                    {/* Logo/Icon */}
                    <div className="logo-container">
                        <Link to="/">
                            <img
                                src={`${import.meta.env.VITE_PUBLIC_URL}logo_full_dark.svg`}
                                alt="LOGO"
                                className="logo-image"
                            />
                        </Link>
                    </div>

                    {/* Main Heading */}
                    <h1 className="main-heading">
                        Payroll Management System
                    </h1>
                
                    {/* Subtitle */}
                    <p className="subtitle">
                        Professional Payroll Management System
                    </p>
                    
                    {/* Description */}
                    <p className="description">
                        Streamline your payroll operations with our comprehensive solution. 
                        Automate employee management, salary calculations, and generate detailed reports effortlessly.
                    </p>

                    {/* Action Buttons */}
                    <div className="action-buttons">
                        <button 
                            className="primary-button"
                            onClick={() => handleButtonClick('/login')}
                        >
                            <span className="primary-button-text">Get Started</span>
                            <div className="primary-button-overlay"></div>
                        </button>
                        <button 
                            className="secondary-button"
                            onClick={() => handleButtonClick('/register')}
                        >
                            Create Account
                        </button>
                    </div>
                </div>

                {/* Features Section */}
                <div className={`features-section ${isVisible ? 'visible' : 'hidden'}`}>
                    {/* Feature 1 */}
                    <div className="feature-card">
                        <div className="feature-icon green">
                            <svg className="feature-icon-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <h3 className="feature-title">Automated Calculations</h3>
                        <p className="feature-description">Effortlessly calculate salaries, taxes, and deductions with precision and accuracy.</p>
                    </div>

                    {/* Feature 2 */}
                    <div className="feature-card">
                        <div className="feature-icon blue">
                            <svg className="feature-icon-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                        </div>
                        <h3 className="feature-title">Comprehensive Reports</h3>
                        <p className="feature-description">Generate 38+ detailed reports with just a click for complete payroll insights.</p>
                    </div>

                    {/* Feature 3 */}
                    <div className="feature-card">
                        <div className="feature-icon pink">
                            <svg className="feature-icon-svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z" />
                            </svg>
                        </div>
                        <h3 className="feature-title">Mobile Ready</h3>
                        <p className="feature-description">Access your payroll system anywhere, anytime with full mobile compatibility.</p>
                    </div>
                </div>

                {/* Stats Section */}
                <div className={`stats-section ${isVisible ? 'visible' : 'hidden'}`}>
                    <div className="stat-item">
                        <div className="stat-number blue">38+</div>
                        <div className="stat-label">Reports</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-number purple">100%</div>
                        <div className="stat-label">Automated</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-number pink">24/7</div>
                        <div className="stat-label">Support</div>
                    </div>
                    <div className="stat-item">
                        <div className="stat-number teal">Mobile</div>
                        <div className="stat-label">Ready</div>
                    </div>
                </div>
            </div>

            {/* Floating Elements */}
            <div className="floating-element-1"></div>
            <div className="floating-element-2"></div>
            <div className="floating-element-3"></div>
            <div className="floating-element-4"></div>
        </div>
    );
};

export default LandingPage;