import { FaCheck } from 'react-icons/fa';

const CustomCheckbox = ({ name, checked, onChange, disabled, borderColor = "border-slate-300", checkColor = "text-slate-300", height = "h-6", width = "w-6", checkSize = "text-sm", bgColor = "bg-transparent", borderSize = "border" }) => {
  return (
    <>

      <input
        name={name}
        type="checkbox"
        checked={checked}
        onChange={onChange}
        disabled={disabled}
        className={`absolute ${disabled ? "cursor-not-allowed" : "cursor-pointer"} appearance-none m-6 ${width} ${height} ${borderSize} ${borderColor} rounded-lg custom-checkbox ${bgColor}`}
      />
      <FaCheck className={` check-1 text-opacity-0 ${checkColor} transition duration-100 ${checkSize}`} />
    </>
  );
};

export default CustomCheckbox;

