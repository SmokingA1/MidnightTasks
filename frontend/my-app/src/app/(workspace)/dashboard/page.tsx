'use client';

import Button from "@/components/Button";
import SideBar from "@/components/SideBar";

const DashboardPage = () => {

    return(
        <div id="dashboard-container" className="flex flex-col gap-5 pt-5 px-2.5 w-full  xl:w-11/12 bg-white">
            <section className="flex justify-between w-full h-20 items-center bg-gray-50 p-2.5 rounded-lg">
                <span className="flex flex-col gap-2.5">
                    <h1 className="text-3xl font-medium">Dashbaord</h1>
                    <p className="text-gray-600 font-light">Plan, prioritize, and accomplish your tasks with ease!</p>
                </span>
                <span className="flex gap-2.5">
                    <Button
                        typeStyle="primary-plus"
                        text="Add Project"
                        onClick={() => console.log("clicked add proejct")}
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
                <div className="flex w-full justify-between gap-2.5">
                    <section className="flex flex-col gap-3 bg-linear-to-br from-teal-900 to-teal-700 w-1/4 border-1 border-gray-100 py-10  pl-5 rounded-lg text-white ">
                        <h2 className=" text-xl">Total projects</h2>
                        <span className="text-4xl mt-2.5  drop-shadow-teal-100 drop-shadow-[0_0_10px_rgba(0,0,0,0.1)] rounded-full  w-fit">0</span>
                        <p className="text-sm text-teal-100 font-light">Some future info</p>
                    </section>
                    <section className="flex flex-col gap-3 bg-white w-1/4 border-1 border-gray-100 py-10 pl-2.5 rounded-lg ">
                        <h2 className=" text-xl">Ended projects</h2>
                        <p className="text-4xl mt-2.5">0</p>
                        <p className="text-sm">Some future info</p>
                    </section>
                    <section className="flex flex-col gap-3 bg-white w-1/4 border-1 border-gray-100 py-10 pl-2.5 rounded-lg ">
                        <h2 className=" text-xl">Running projects</h2>
                        <p className="text-4xl mt-2.5">0</p>
                        <p className="text-sm">Some future info</p>
                    </section>
                    <section className="flex flex-col gap-3 bg-white w-1/4 border-1 border-gray-100 py-10 pl-2.5 rounded-lg ">
                        <h2 className=" text-xl">Pending projects</h2>
                        <p className="text-4xl mt-2.5">0</p>
                        <p className="text-sm">On discussion</p>
                    </section>
                </div>
                

            </section>
        </div>
    )
}

export default DashboardPage;