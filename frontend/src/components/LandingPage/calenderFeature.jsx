import React, { useState, useEffect } from 'react';
import './calenderFeature.css';

const CalendarFeature = () => {
  const [currentDate, setCurrentDate] = useState(new Date());
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false);
    }, 10000);

    return () => clearTimeout(timer);
  }, []);

  const daysInMonth = (date) => {
    return new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
  };

  const firstDayOfMonth = (date) => {
    return new Date(date.getFullYear(), date.getMonth(), 1).getDay();
  };

  const handlePrevMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, 1));
  };

  const handleNextMonth = () => {
    setCurrentDate(new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1));
  };

  const renderCalendar = () => {
    const totalDays = daysInMonth(currentDate);
    const startingDay = firstDayOfMonth(currentDate);
    const calendarDays = [];

    const dayNames = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];
    for (let i = 0; i < dayNames.length; i++) {
      calendarDays.push(<div key={`day-name-${i}`} className="calendar-day-name">{dayNames[i]}</div>);
    }

    for (let i = 0; i < startingDay; i++) {
      calendarDays.push(<div key={`empty-${i}`} className="empty-day"></div>);
    }

    for (let day = 1; day <= totalDays; day++) {
      const isCurrentDay = day === new Date().getDate() && currentDate.getMonth() === new Date().getMonth() && currentDate.getFullYear() === new Date().getFullYear();
      calendarDays.push(
        <div key={day} className={`calendar-day ${isCurrentDay ? 'current-day' : ''}`}>
          {day}
        </div>
      );
    }

    return calendarDays;
  };

  if (!visible) {
    return null;
  }

  return (
    <div className="calendar-container">
      <div className="calendar-header">
        <button onClick={handlePrevMonth} className="nav-button">‹</button>
        <h2>{currentDate.toLocaleString('default', { month: 'long', year: 'numeric' })}</h2>
        <div className="mobile-date">{currentDate.toLocaleDateString('default', { day: 'numeric' })}</div>
        <button onClick={handleNextMonth} className="nav-button">›</button>
      </div>
      <div className="calendar-grid">
        {renderCalendar()}
      </div>
    </div>
  );
};

export default CalendarFeature;
