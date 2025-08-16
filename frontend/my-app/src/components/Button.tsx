"use client"

import React, { ButtonHTMLAttributes } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
    typeStyle: "primary" | "secondary" | "tertiary";
    onClick: () => void;
    text: string;
    width?: string;
}

const types = {
    "primary": "bg-teal-900 border-1 border-teal-900 hover:bg-teal-700 hover:border-teal-700 text-white rounded-sm",
    "secondary": "bg-transparent border-2 border-teal-800 hover:bg-teal-800 hover:text-white 800 text-teal-800 font-semibold rounded-sm",
    "tertiary": "bg-transparent hover:underline text-teal-800 font-semibold"
}

const Button: React.FC<ButtonProps> = ({typeStyle, onClick, text, width}) => {
    return (
        <button className={`duration-200 cursor-pointer px-16 py-2.5 ${types[typeStyle]} ${width}`} onClick={onClick}>
            {text}
        </button>
    )
}

export default Button;