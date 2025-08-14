"use client"

import React, { useState } from "react"
import Button from "./Button"
import Input from "./Input"
import facebookLogo from "../../public/facebook.svg"
import googleLogo from "../../public/google.svg"
import Image from "next/image"
import Link from "next/link"

interface RegistrationFormProps {
    switchForm: () => void;
}

const RegistrationForm: React.FC<RegistrationFormProps> = ({switchForm}) => {
    const [isVisiblePassword, setIsVisiblePassword] = useState<boolean>(false);


    return (
        <form className="w-100 h-full flex flex-col items-center py-5">
            <h2 className="text-xl mt-15 self-start font-semibold">Welcome here!</h2>
            <p className="self-start mb-5">Please enter sign up details below</p>
            <Input 
                typeStyle="primary"
                placeholder="Type username here"
                label="Username"
                width="w-full"
                type="email"
                id="registration-username"
                name="username"
                autoComplete="new-username"
                required
            />

            <Input 
                typeStyle="primary"
                placeholder="Type email here"
                label="Email"
                width="w-full"
                type="email"
                id="registration-email"
                name="email"
                required
            />
            
            <Input 
                typeStyle="hidden"
                placeholder="Type password here"
                label="Password"
                width="w-full"
                id="new-password"
                name="new-password"
                autoComplete="new-password"
                required
            />
            
            <div className="py-5"></div>
            <Button typeStyle="primary" onClick={() => console.log("hello")} text="LOG IN" width="w-full"/>


            <p className="mt-5 flex gap-1">Already have an account?
                <span onClick={switchForm} className="text-blue-900 hover:text-blue-700 duration-100 cursor-pointer">Sign up</span>
            </p>
            
        </form>
    )
}

export default RegistrationForm;