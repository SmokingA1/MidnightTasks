'use client';

import Button from "@/components/Button";
import ProjectCreate from "@/components/ProjectCreate";
import { useRouter } from "next/navigation";
import { useState } from "react";

const DashboardPage = () => {
    const [showProjectCreate, setShowProjectCreate] = useState<boolean>(false);
    const router = useRouter();
    
    return(
        <>
        
            <section className="flex justify-between w-full h-20 items-center bg-gray-50 p-2.5 rounded-lg">
                <span className="flex flex-col gap-2.5">
                    <h1 className="text-3xl font-medium">Dashboard</h1>
                    <p className="text-gray-600 font-light">Plan, prioritize, and accomplish your tasks with ease!</p>
                </span>
                <span className="flex gap-2.5">
                    <Button
                        typeStyle="primary-plus"
                        text="Add Project"
                        onClick={() => setShowProjectCreate(true)}
                        height="h-11"
                    />
                    <Button
                        typeStyle="secondary-import"
                        text="Import Data"
                        onClick={() => console.log("clicked import data")}
                        height="h-11"                    
                        />
                </span>
            </section>
            <section className="flex-col bg-gray-50 h-full p-2.5 rounded-lg">
                <div className="grid grid-cols-3 w-full  gap-2.5">
                    <section className="flex flex-col items-center">
                        <h2>My projects</h2>
                    </section>
                    <section className="flex flex-col items-center">
                        <h2>My tasks</h2>
                    </section>
                    <section className="flex flex-col items-center">
                        <h2>Statictics</h2>
                    </section>
                </div>
                
                {showProjectCreate && <ProjectCreate onClose={() => setShowProjectCreate(false)}    />}
            </section>
            
        </>
    )
}

export default DashboardPage;


{/* <section className="flex flex-col gap-3 bg-linear-to-br from-teal-900 to-teal-700 w-1/4 border-1 border-gray-100 py-12 pl-5 rounded-lg text-white ">
                        <h2 className=" text-xl mb-3">Total projects</h2>
                        <span className="text-4xl mb-2  drop-shadow-teal-100 drop-shadow-[0_0_10px_rgba(0,0,0,0.1)] rounded-full w-fit">0</span>
                        <p className="text-sm text-teal-100 font-light">Some future info</p>
                    </section>
                    <section className="flex flex-col gap-3 bg-white w-1/4 border-1 border-gray-100 py-12 pl-5 rounded-lg ">
                        <h2 className=" text-xl mb-3">Ended projects</h2>
                        <p className="text-4xl mb-2">0</p>
                        <p className="text-sm">Some future info</p>
                    </section>
                    <section className="flex flex-col gap-3 bg-white w-1/4 border-1 border-gray-100 py-12 pl-5 rounded-lg">
                        <h2 className=" text-xl mb-3">Running projects</h2>
                        <p className="text-4xl mb-2">0</p>
                        <p className="text-sm">Some future info</p>
                    </section>
                    <section className="flex flex-col gap-3 bg-white w-1/4 border-1 border-gray-100 py-12 pl-5 rounded-lg">
                        <h2 className=" text-xl mb-3">Pending projects</h2>
                        <p className="text-4xl mb-2">0</p>
                        <p className="text-sm">On discussion</p>
                    </section> */}