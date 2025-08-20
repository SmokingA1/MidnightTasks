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
                {children}
            </div>
        </main>
    );
}






