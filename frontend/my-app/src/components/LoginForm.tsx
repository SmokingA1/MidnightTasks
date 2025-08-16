"use client"

import React, { useEffect, useState } from "react"
import Button from "./Button"
import Input from "./Input"
import facebookLogo from "../../public/facebook.svg"
import googleLogo from "../../public/google.svg"
import Image from "next/image"
import Link from "next/link"
import { api } from "@/api"

interface LoginFormProps {
    switchForm: () => void;
}

interface UserPropsInterface {
    email: string;
    password: string;
}

const LoginForm: React.FC<LoginFormProps> = ({switchForm}) => {
    const [userProps, setUserProps] = useState<UserPropsInterface>({
        email: "",
        password: "",
    })
    const [error, setError] = useState<"pass-l" | "incorrect" | "many-attempts" | null>(null);

    useEffect(() => {
        console.log(userProps)
    }, [userProps]);

    useEffect(() => {
        if (error == "pass-l") {
            setError(null)
        } 
    }, [userProps.password])


    useEffect(() => {
        if (error == "incorrect") {
            setError(null);
        }
    }, [userProps])

    const handleLogin = async (e: React.FormEvent) => {
        e.preventDefault();

        if (userProps.password.length < 8) {setError("pass-l"); return null};

        const formData = {
            "username": userProps.email,
            "password": userProps.password,
        }

        try {
            const response = await api.post("/login/", formData, {
                headers: {"COntent-Type": "application/x-www-form-urlencoded"}
            })
            console.log(response.data);
        } catch (error: any) {
            if (error.response) {
                console.error("Server error: ", error.response);
                if (error.response.status == 403) {
                    setError("incorrect")
                } else if (error.response.status == 429) {
                    setError("many-attempts")
                }
            } else {
                console.error("Network or other error: ", error);
            }
        }
    }

    return (
        <form id="login-form" className="w-100 h-full flex flex-col items-center py-5" onSubmit={handleLogin}>
            <h2 className="text-xl mt-15 self-start font-semibold">Welcome back!</h2>
            <p className="self-start mb-5">Please enter log in details below</p>
            <Input 
                typeStyle="primary"
                placeholder="Type email here"
                label="Email"
                width="w-full"
                type="email"
                id="login-email"
                name="email"
                autoComplete="email"
                required
                value={userProps.email}
                onChange={(e) => setUserProps({ ...userProps, email: e.target.value },)}
            />
            <Input 
                typeStyle="hidden"
                placeholder="Type password here"
                label="Password"
                width="w-full"
                id="login-password"
                name="current-password"
                autoComplete="current-password"
                required
                value={userProps.password}
                onChange={(e) => setUserProps({ ...userProps, password: e.target.value })}
            />
            {error == "incorrect" && <span className="text-red-500 self-start">Incorrect email or password!</span>}
            {error == "pass-l" && <span className="text-red-500 self-start">Password cannot be smaller than 8!</span>}
            {error == "many-attempts" && <span className="text-red-500 self-start">Too many failed login attempts, please try again later.</span>}
            <div id="remeber-n-link" className="flex w-full justify-between">
                <div className="flex gap-2">
                    <input 
                        type="checkbox" 
                    />
                    Remember me
                </div>

                <Link href={"#"} className="text-blue-900 hover:text-blue-700 duration-100">Forgot password?</Link>
            </div>
                
            <div className="py-5"></div>
            <Button typeStyle="primary" onClick={() => console.log("hello")} text="LOG IN" width="w-full" type="submit"/>
            <div className="flex items-center w-full gap-2.5 my-7.5">
                <hr className="border-t border-gray-300 w-full"></hr>
                <h2>OR</h2>
                <hr className="border-t border-gray-300 w-full"></hr>

            </div>

            <div id="o-auth" className="flex justify-evenly w-full gap-2.5">
                
                <section className="flex items-center justify-center rounded-md border w-full py-2.5 gap-2.5 border-gray-300 shadow-[0_0_4px_rgba(0,0,0,0.1)] hover:bg-gray-100 cursor-pointer duration-100 ">
                    <Image src={googleLogo} alt="google-icon to open authorization" width={20}></Image>
                    <p>Google</p>
                </section>
                <section className="flex items-center justify-center rounded-md border w-full py-2.5 gap-2.5 border-gray-300 shadow-[0_0_4px_rgba(0,0,0,0.1)] hover:bg-gray-100 cursor-pointer duration-100 ">
                    <Image src={facebookLogo} alt="facebook-icon to open authorization" width={20}></Image>
                    <p>Facebook</p>
                </section>

            </div>

            <p className="mt-5 flex gap-1">Don't have an account?
                <span onClick={switchForm} className="text-blue-900 hover:text-blue-700 duration-100 cursor-pointer"> Sign up</span>
            </p>
            
        </form>
    )
}

export default LoginForm;