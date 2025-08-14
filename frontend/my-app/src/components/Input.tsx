"use client"

import React, { InputHTMLAttributes, useState } from "react";
import {Eye, EyeOff} from "lucide-react";

interface InputIntreface extends InputHTMLAttributes<HTMLInputElement> {
    typeStyle: "primary" | "hidden";
    label?: string;
    width: string;
    id: string;
}

const types = {
    "primary": "bg-slate-100 outline-none px-5 py-2.5 rounded-md ",
    "hidden": "bg-slate-100 outline-none px-5 py-2.5 rounded-md ",
}

const Input: React.FC<InputIntreface> = ({typeStyle, label, width, id, ...props}) => {
    const [isVisible, setIsVisible] = useState<boolean>(false);

    return (
        <div className="flex flex-col w-100 gap-2.5 my-3">
            <label htmlFor={id}>{label}</label>
            <div className="flex relative">
                <input
                    id={id}
                    className={`${types[typeStyle]} ${width}`}
                    {...props}
                    type={`${typeStyle == "hidden" && isVisible == false ? 'password' : 'text'}`}

                />
                {typeStyle == "hidden" && ( isVisible == false ? (
                    <Eye size={20} onClick={() => setIsVisible(true)} className="absolute top-1/2 -translate-y-1/2 right-2"/>
                    ) : (
                    <EyeOff size={20} onClick={() => setIsVisible(false)} className="absolute top-1/2 -translate-y-1/2 right-2"/>
                    ))
                }
            </div>
            
        </div>

    )
}


export default Input;