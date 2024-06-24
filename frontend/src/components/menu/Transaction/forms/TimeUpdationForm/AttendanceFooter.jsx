import React, { useMemo, useCallback, useEffect, useState } from 'react';
import {
  useGetAllEmployeeLeaveOpeningQuery
} from '../../../../authentication/api/timeUpdationApiSlice';
import { useGetSingleEmployeeSalaryDetailQuery } from '../../../../authentication/api/employeeEntryApiSlice';
import { useSelector } from 'react-redux';
const classNames = (...classes) => {
  return classes.filter(Boolean).join(' ');
};

const AttendanceFooter = React.memo(
  ({
    attendance,
    absent,
    weeklyOffSkip,
    holidayOffSkip,
    missPunch,
    present,
    onDuty,
    weeklyOff,
    holidayOff,
    leaveGrades,
    updateEmployeeId,
    globalCompany,
    compensationOff
  }) => {
    const [attendanceFooterData, setAttendanceFooterData] = useState({
      workingDays: 0,
      weeklyOff: 0,
      holiday: 0,
      leave: 0,
      paidDays: 0,
      absent: 0,
      totalOvertime: 0,
      totalLate: 0,
    });
    const auth = useSelector((state) => state.auth);
    const {
      data: employeeSalaryDetails,
      isLoading: isLoadingEmployeeSalaryDetails,
      isSuccess: isEmployeeSalaryDetailsSuccess,
      isFetching: isFetchingEmployeeSalaryDetails,
    } = useGetSingleEmployeeSalaryDetailQuery(
      {
        company: globalCompany?.id,
        id: updateEmployeeId,
      },
      {
        skip: globalCompany === null || globalCompany === '' || updateEmployeeId == null,
      }
    );
    const filteredLeaveGradesWithGenerateFrequency = useMemo(
      () => (leaveGrades ? leaveGrades.filter((grade) => grade.generateFrequency !== null) : []),
      [leaveGrades]
    );

    const calculateAttendanceFooter = useCallback(() => {
      const initialData = {
        workingDays: 0,
        weeklyOff: 0,
        holiday: 0,
        leave: 0,
        paidDays: 0,
        absent: 0,
        totalOvertime: 0,
        totalLate: 0,
      };

      // Iterate over the attendance keys
      Object.keys(attendance).forEach((key) => {
        const entry = attendance[key];
        // Check for firstHalf
        if (
          entry.firstHalf === absent.id ||
          entry.firstHalf == weeklyOffSkip.id ||
          entry.firstHalf == holidayOffSkip.id ||
          entry.firstHalf == missPunch.id
        ) {
          initialData.absent += 1;
        } else if (entry.firstHalf === present.id || entry.firstHalf == onDuty.id) {
          initialData.workingDays += 1;
          initialData.paidDays += 1;
        } else if (entry.firstHalf === weeklyOff.id) {
          initialData.weeklyOff += 1;
          initialData.paidDays += 1;
        } else if (entry.firstHalf === holidayOff.id) {
          initialData.holiday += 1;
          initialData.paidDays += 1;
        } else if (entry.firstHalf === compensationOff.id) {
          initialData.leave += 1;
          initialData.paidDays += 1;
        } else if (
          filteredLeaveGradesWithGenerateFrequency.some((grade) => grade.id === parseInt(entry.firstHalf))
        ) {
          initialData.leave += 1;
          initialData.paidDays += 1;
        } else {
          initialData.absent += 1;
        }

        // Check for secondHalf
        if (
          entry.secondHalf === absent.id ||
          entry.secondHalf == weeklyOffSkip.id ||
          entry.secondHalf == holidayOffSkip.id ||
          entry.secondHalf == missPunch.id
        ) {
          initialData.absent += 1;
        } else if (entry.secondHalf === present.id || entry.secondHalf == onDuty.id) {
          initialData.workingDays += 1;
          initialData.paidDays += 1;
        } else if (entry.secondHalf === weeklyOff.id) {
          initialData.weeklyOff += 1;
          initialData.paidDays += 1;
        } else if (entry.secondHalf === holidayOff.id) {
          initialData.holiday += 1;
          initialData.paidDays += 1;
        } else if (entry.secondHalf === compensationOff.id) {
          initialData.leave += 1;
          initialData.paidDays += 1;
        } else if (
          filteredLeaveGradesWithGenerateFrequency.some((grade) => grade.id === parseInt(entry.secondHalf))
        ) {
          initialData.leave += 1;
          initialData.paidDays += 1;
        } else {
          initialData.absent += 1;
        }

        // Check for overtime
        if (entry.otMin) {
          initialData.totalOvertime += parseInt(entry.otMin);
        }
        if (entry.lateMin) {
          initialData.totalLate += parseInt(entry.lateMin);
        }

        // You can add more logic here for other keys like workingDays, holiday, etc.
      });

      return initialData;
    }, [attendance]);
    useEffect(() => {
      setAttendanceFooterData(calculateAttendanceFooter());
    }, [attendance]);

    return (
      <div className="flex flex-row justify-between gap-2 pt-2 text-sm">
        <div>
          {' '}
          W Days: <span className="font-bold">{attendanceFooterData.workingDays / 2}</span>
        </div>
        <div>
          WO: <span className="font-bold">{attendanceFooterData.weeklyOff / 2}</span>
        </div>
        <div>
          HD: <span className="font-bold">{attendanceFooterData.holiday / 2}</span>
        </div>
        <div>
          LV: <span className="font-bold">{attendanceFooterData.leave / 2}</span>
        </div>
        <div>
          P Days: <span className="font-bold">{attendanceFooterData.paidDays / 2}</span>
        </div>
        <div className="dark:text-red-600">
          AB: <span className="font-bold">{attendanceFooterData.absent / 2}</span>
        </div>
        <div>
          OT:{' '}
          <span className="font-bold">
            {Math.max(
              attendanceFooterData.totalOvertime -
              (employeeSalaryDetails?.lateDeduction == true && auth.account.role == 'OWNER'
                ? Math.floor(attendanceFooterData.totalLate / 30) * 30 +
                (attendanceFooterData.totalLate % 30 >= 20 ? 30 : 0)
                : 0),
              0
            ) / 60}
            {/* {`${String(
							Math.max(
								attendanceFooterData.totalOvertime -
									(Math.floor(attendanceFooterData.totalLate / 30) * 30 +
										(attendanceFooterData.totalLate % 30 >= 20 ? 30 : 0)),
								0
							) / 60
						).padStart(2, '0')}:${String(
							Math.max(
								attendanceFooterData.totalOvertime -
									(Math.floor(attendanceFooterData.totalLate / 30) * 30 +
										(attendanceFooterData.totalLate % 30 >= 20 ? 30 : 0)),
								0
							) % 60
						).padStart(2, '0')}`} */}
            {/* {attendanceFooterData.totalOvertime -
							(Math.floor(attendanceFooterData.totalLate / 30) * 30 +
								(attendanceFooterData.totalLate % 30 >= 20 ? 30 : 0))} */}
          </span>
        </div>
        <div className="dark:text-red-600">
          Late:
          <span className="font-bold">
            {`${String(Math.floor(attendanceFooterData.totalLate / 60)).padStart(2, '0')}:${String(
              attendanceFooterData.totalLate % 60
            ).padStart(2, '0')}`}
          </span>
        </div>
      </div>
    );
  }
);
export default AttendanceFooter;
