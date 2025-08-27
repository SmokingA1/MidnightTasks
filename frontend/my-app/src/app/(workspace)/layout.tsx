'use client'

import SideBar from "@/components/SideBar";



export default function WorkSpaceRoot({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {


    return (
        <main id="dashboard-layout" className="h-full flex">
            <SideBar />
            <div className="flex justify-center w-full bg-gray-100">
                <div id="dashboard-container" className="flex flex-col gap-5 pt-5 px-2.5 w-full  xl:w-11/12 bg-white">
                    {children}
                </div>
            </div>
        </main>
    );
}






