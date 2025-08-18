'use client';

import useUserStore from "@/store/user";
import { use, useEffect, useState } from "react";
import user_def_icon from "@/assets/user-def-icon.ico"
import Image from "next/image";
import { LayoutDashboard, AppWindow, Bookmark, ClipboardList, ClipboardClock, FolderClosed, List, ListPlus} from 'lucide-react';
import Input from "./Input";


const SideBar = () => {
    
    const user = useUserStore();
    const mainMenu = ["dashboard", "my to-do", "request from", "reports"]
    const mainMenuIcons = [<LayoutDashboard />, <AppWindow/>, <Bookmark />, <ClipboardList />]
    const [searchValue, setSearchValue] = useState<string>("");
    useEffect(() => {
        console.log(user.username);
        document.body.style.overflow = "hidden"; // отключаем скролл
        return () => {
            document.body.style.overflow = ""; // возвращаем при размонтировании
    };
    }, [])



    return (
        <div className="hidden md:flex border-r-1 border-gray-300 w-[300px] flex-col text-gray-600 h-full" >
            <article className="flex flex-col h-full"> 
                <div className="flex gap-2 p-2 m-2.5 border-1 border-gray-200 rounded-md ">
                    <Image src={!user.avatar_url ? user_def_icon :  user.avatar_url.startsWith("static") ? `http://localhost:8000/${user.avatar_url}` : `${user.avatar_url}`} alt="User icon" width={48} />
                    <div>
                        <h2 className="text-xl text-black font-medium">{user.username}</h2>
                        <p className="text-sm font-light text-gray-500 ">{user.email}</p>
                    </div>
                    
                </div>
                <div className="flex justify-center items-center mb-2.5 mx-2.5 border-1 h-10 rounded-sm border-gray-300">
                    <Input 
                        typeStyle="secondary"    
                        type="text"
                        value={searchValue}
                        onChange={(e) => setSearchValue(e.target.value)}
                        width="w-3/4"
                        id="main-search-field"
                    />
                    <ListPlus className="mr-2.5" size={30}/>

                </div>
                <nav className="flex flex-col nav-block px-2 overflow-y-auto max-h-full">

                    <section>
                        <h2 >MAIN MENU</h2>
                        <ul className="flex flex-col gap-2.5 px-2 py-3">
                            { mainMenu.map((el, id) => (
                                        <li 
                                            key={id}
                                            className="
                                                flex items-center gap-1 p-2 hover:bg-gray-200/90 cursor-pointer duration-100 rounded-md
                                            " >
                                    {mainMenuIcons[id]} {el.charAt(0).toUpperCase() + el.slice(1)}
                                </li>
                                )
                            )}

                        </ul>
                    </section>
                    <hr className="border-t-1 w-full my-7 border-gray-100"></hr>
                    <section>
                        <h2>INCOMING DEADLINE</h2>
                        <ul className="flex flex-col gap-2.5 px-2 py-3">
                            <li key={"1101010101001"} className="flex items-center gap-1"><ClipboardClock /> Some task</li>
                        </ul>
                    </section>
                    <hr className="border-t-1 w-full my-7 border-gray-100"></hr>
                    <section>
                        <h2> MY PROJECTS</h2>
                        <ul className="flex flex-col gap-2.5 px-2 py-3">
                            <li key={"010101010101010101010"} className="flex items-center gap-1"><FolderClosed /> Some project </li>
                        </ul>
                    </section>

                </nav>
            </article>
        </div>
    )
}

export default SideBar;