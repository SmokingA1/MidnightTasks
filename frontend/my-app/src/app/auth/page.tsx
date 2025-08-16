"use client"

import LoginForm from "@/components/LoginForm";
import RegistrationForm from "@/components/RegistrationForm";
import { useEffect, useRef, useState } from "react";
import Image from "next/image";
import backphoto from "../../../public/10589.jpg"

const LoginPage = () => {
    const [selectedForm, setSelectedForm] = useState<"login" | "registration">("login")
    const firstRender = useRef(true);

    useEffect(() => {
        console.log("heelo")
    }, [])


    const handleSwitchForm = (form: "login" | "registration") => {
        setSelectedForm(form)
        firstRender.current = false
    }

    return (
        <div id="auth-frame" className="bg-white flex w-[1200px] h-[800px] shadow-lg relative">
            <div className="flex flex-col w-[600px] justify-center items-center border-r-1 p-2.5 z-1">
                <h1 className="self-start text-xl font-medium text-teal-900">MT-Midnight Tasks</h1>
                <LoginForm switchForm={() => handleSwitchForm("registration")} />
            </div>

            <div className="flex flex-col w-[600px] justify-center items-center p-2.5 z-1">
                <h1 className="self-start text-xl font-medium text-teal-900">MT-Midnight Tasks</h1>
                <RegistrationForm switchForm={() => handleSwitchForm("login")} />
            </div>
            <div className={`
                absolute flex w-[600px] h-full bg-teal-900 z-5  border-1
                ${
                    firstRender.current
                    ? "right-0"
                    : selectedForm === "login"
                        ? "animate-to-right"
                        : "animate-to-left"
                }`
            }>
                <Image src={backphoto}  alt="cover-background"/>
            </div>

        </div>
    )
}

export default LoginPage;