"use client"

import React, { use, useEffect, useState } from "react"
import Button from "./Button"
import Input from "./Input"
import facebookLogo from "../../public/facebook.svg"
import googleLogo from "../../public/google.svg"
import Image from "next/image"
import Link from "next/link"
import { api } from "@/api"

interface RegistrationFormProps {
    switchForm: () => void;
}

interface UserPropsInterface {
    username: string;
    email: string;
    password: string;   
}

const RegistrationForm: React.FC<RegistrationFormProps> = ({switchForm}) => {
    const [userProps, setUserProps] = useState<UserPropsInterface>({
        username: "",
        email: "",
        password: ""
    })

    const [error, setError] = useState<"username" | "email" | "pass-l" | null>(null);

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();

        if (userProps.password.length < 8) {setError("pass-l"); return null}

        const formData = {
            "username": userProps.username,
            "email": userProps.email,
            "password": userProps.password,
        }

        try {
            const response = await api.post("/users/", formData)
            console.log(response.data);
            setUserProps({
                username: "",
                email: "",
                password: ""
            })
        } catch (error: any) {
            if (error.response.data) {
                console.error("Server error: ", error.response.data);
                     
                const detail = error.response.data.detail;

                if (typeof detail === "string") {
                    if (/email/.test(detail)) {
                        setError("email");
                    } else if (/username/.test(detail)) {
                        setError("username");
                    } else {
                        console.log("Other server error:", detail);
                    }
                } else {
                    console.log("Unexpected error detail format:", detail);
                }
            } else {
                console.error("Network or other error: ", error);
            }
        }
    }

    useEffect(() => {
        console.log(userProps)
    }, [userProps]);
    
    useEffect(() => {
        if (error == "pass-l") {
            setError(null)
        } 
    }, [userProps.password])

    return (
        <form id="registration-form" className="w-100 h-full flex flex-col items-center py-5" onSubmit={handleRegister}>
            <h2 className="text-xl mt-15 self-start font-semibold">Welcome here!</h2>
            <p className="self-start mb-5">Please enter sign up details below</p>
            <Input 
                typeStyle="primary"
                placeholder="Type username here"
                label="Username"
                width="w-full"
                type="text"
                id="registration-username"
                name="username"
                autoComplete="new-username"
                required
                value={userProps.username}
                onChange={(e) => setUserProps({ ...userProps, username: e.target.value})}
            />
            {error == "username" && <span className="text-red-500 self-start">Such login already exists1</span>}
            <Input 
                typeStyle="primary"
                placeholder="Type email here"
                label="Email"
                width="w-full"
                type="email"
                id="registration-email"
                name="email"
                autoComplete="email"
                required
                value={userProps.email}
                onChange={(e) => setUserProps({ ...userProps, email: e.target.value})}
            />
            {error == "email" && <span className="text-red-500 self-start">Such email already exists!</span>}

            <Input 
                typeStyle="hidden"
                placeholder="Type password here"
                label="Password"
                width="w-full"
                id="registration-new-password"
                name="new-password"
                autoComplete="new-password"
                required
                value={userProps.password}
                onChange={(e) => setUserProps({ ...userProps, password: e.target.value})}
            />
            {error == "pass-l" && <span className="text-red-500 self-start">Password cannot be less than 8 characters!</span>}

            <div className="py-5"></div>
            <Button typeStyle="primary" onClick={() => console.log("hello")} text="SIGN UP" width="w-full" type="submit"/>


            <p className="mt-5 flex gap-1">Already have an account?
                <span onClick={switchForm} className="text-blue-900 hover:text-blue-700 duration-100 cursor-pointer">Log in</span>
            </p>
            
        </form>
    )
}

export default RegistrationForm;