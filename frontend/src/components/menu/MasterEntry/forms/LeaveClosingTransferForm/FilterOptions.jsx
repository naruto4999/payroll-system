
import React from 'react';
import { Field, ErrorMessage, FieldArray } from 'formik';
import { FaCircleNotch } from 'react-icons/fa';
import { useGetLeaveGradesQuery } from '../../../../authentication/api/leaveGradeEntryApiSlice';
import CustomCheckbox from './CustomCheckbox';

const classNames = (...classes) => {
  return classes.filter(Boolean).join(' ');
};
const FilterOptions = ({ handleChange, values, setFieldValue, isValid, handleSubmit, isSubmitting, globalCompany }) => {
  console.log(values);
  const {
    data: leaveGrades,
    isLoading: isLoadingLeaveGrades,
    isSuccess: isSuccessLeaveGrades,
    isError: isErrorLeaveGrades,
  } = useGetLeaveGradesQuery(globalCompany);
  console.log(leaveGrades)
  console.log(values)
  // Function to select all checkboxes
  const selectAll = () => {
    const allIds = leaveGrades
      ?.filter((leaveGrade) => leaveGrade.generateFrequency !== null)
      .map((leaveGrade) => leaveGrade.id) || [];
    setFieldValue('leavesSelected', allIds);
  };

  // Function to deselect all checkboxes
  const deselectAll = () => {
    setFieldValue('leavesSelected', []);
  };

  return (
    <div className="flex flex-col gap-2">
      <table role="group" aria-labelledby="checkbox-group" classname="">
        <thead>
          {/* <tr className=''> */}
          {/*   <th className='rounded-lg py-1 px-4 border'>Deselect All</th> */}
          {/*   <th className='py-1 px-4'>Select All</th> */}
          {/* </tr> */}
          <tr className="">
            <th>
              <button onClick={deselectAll} className="bg-amber-800 hover:bg-amber-700 cursor-pointer rounded-md py-1 px-4 ">Deselect All</button>
            </th>
            <th>
              <button onClick={selectAll} className="bg-blueAccent-800 hover:bg-blueAccent-700 cursor-pointer rounded-md py-1 px-4 ">Select All</button>
            </th>
          </tr>
        </thead>
        <tbody>
          {leaveGrades
            ?.filter((leaveGrade) => leaveGrade.generateFrequency !== null)
            .map((leaveGrade) => (
              <tr className="border border-slate-300 border-opacity-70 group hover:bg-zinc-800" key={leaveGrade.id}>
                <td className="flex flex-col py-1 items-center justify-center">{leaveGrade.name}</td>
                <td className="">
                  <div className="flex flex-col py-1 justify-center overflow-hidden items-center">
                    <CustomCheckbox
                      name={`leavesSelected`}
                      checked={values.leavesSelected.includes(leaveGrade.id)}
                      onChange={() => {
                        const newSelected = values.leavesSelected.includes(leaveGrade.id)
                          ? values.leavesSelected.filter(id => id !== leaveGrade.id)
                          : [...values.leavesSelected, leaveGrade.id];
                        setFieldValue('leavesSelected', newSelected);
                      }}
                      value={leaveGrade.id}
                      checkColor="text-amber-600"
                      disabled={false}
                    />
                  </div>
                </td>
              </tr>
            ))}
        </tbody>

      </table >

      <section>
        <div className="mt-4 mb-2 flex w-fit flex-row gap-4">
          <button
            className={classNames(
              isValid ? 'hover:bg-teal-600  dark:hover:bg-teal-600' : 'opacity-40',
              'h-10 w-fit rounded bg-teal-500 p-2 px-4 text-base font-medium dark:bg-teal-700'
            )}
            type="submit"
            disabled={!isValid}
            onClick={handleSubmit}
          >
            Transfer
            {isSubmitting && (
              <FaCircleNotch className="my-auto ml-2 inline animate-spin text-xl text-amber-700 dark:text-amber-600 " />
            )}
          </button>
        </div>
      </section>
    </div >
  );
};

export default FilterOptions;
