"use client"

import { Plus } from "lucide-react";
import React, { ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    typeStyle: "primary" | "secondary" | "tertiary" | "primary-plus" | "secondary-import";
    onClick: () => void;
    text: string;
    width?: string;
    height?: string;
}

const types = {
    "primary": "px-16 bg-teal-900 border-1 border-teal-900 hover:bg-teal-700 hover:border-teal-700 text-white rounded-sm",
    "secondary": "px-16 bg-transparent border-2 border-teal-800 hover:bg-teal-800 hover:text-white 800 text-teal-800 font-semibold rounded-sm",
    "tertiary": "px-16 bg-transparent hover:underline text-teal-800 font-semibold",
    "primary-plus": "px-6 bg-linear-to-br from-teal-900 to-teal-600 text-white rounded-2xl transition-colors hover:from-teal-600 hover:to-teal-900 duration-500",
    "secondary-import": "px-8 border-1 bg-trasnparent text-black rounded-2xl border-teal-800 hover:bg-teal-800 hover:text-white duration-300"

         
  
}

const Button: React.FC<ButtonProps> = ({typeStyle, onClick, text, width, height}) => {
    return (
        <button className={`flex duration-200 cursor-pointer py-2.5 gap-2 items-center justify-center ${types[typeStyle]} ${width} ${height} `} onClick={onClick}>
            {typeStyle === "primary-plus" && <Plus className="" />}
            <span className="whitespace-nowrap">{text}</span>
        </button>
    )
}

export default Button;