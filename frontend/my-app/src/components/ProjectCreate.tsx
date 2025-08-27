'use client'

import { Cross, X } from "lucide-react";
import Input from "./Input";
import { useState } from "react";
import Button from "./Button";
import { api } from "@/api";
import useUserStore from "@/store/user";

interface ProjectProps {
    name: string;
    description?: string;
    visibility: "public" | "private" | "team";
}

interface ProjectCreateInterface {
    onClose: () => void;

}

const ProjectCreate: React.FC<ProjectCreateInterface> = ({onClose}) => {
    const [projectCreate, setProjectCreate] = useState<ProjectProps>({
        name: "",
        description: "",
        visibility: "public",
    })
    const [isDropList, setIsDropList] = useState<boolean>(false);
    const user = useUserStore();
    const dropList: ["public", "private", "team"] = ["public", "private", "team"]

    const handleCreateProject = async (e: React.FormEvent) => {
        e.preventDefault();

        const formData = {
            "owner_id": user.id,
            "name": projectCreate.name,
            "description": projectCreate.description,
            "visibility": projectCreate.visibility,
        }

        try {
            const response = await api.post("/project/", formData)
            console.log(response.data);

        } catch (error: any) {
            if (error.response) {
                console.error("Server error: ", error.response);
            } else {
                console.error("Network or other error: ", error);
            }
        } finally {
            onClose();
        }

    }

    return (
        <>
        <div id="blur" className="fixed h-screen w-screen backdrop-blur-sm bg-gray-900/20  z-4 top-0 left-0" onClick={() => onClose()}></div>
        <section className="fixed top-1/2 left-1/2 border-1 border-gray-100 rounded-xl w-150 h-120 bg-white  -translate-y-1/2 -translate-x-1/2 z-5" >
            <div id="fake-header" className="flex justify-center items-center relative h-15 border-b-1 border-gray-100">
                <h2 className="font-medium">Create New Project</h2>   
                <X onClick={onClose} size={34} className="absolute border-1 m-1 p-2 rounded-md drop-shadow-md border-gray-100 top-1/2 -translate-y-1/2 right-0 hover:bg-gray-200 cursor-pointer " />            
            </div>
            <form onSubmit={handleCreateProject}>
                <div id="project-create-content" className="grid grid-cols-[200px_1fr] px-10 p-5 gap-2.5">
                    <label htmlFor="project-name-field" className="flex gap-2.5">
                        Project name
                    </label>
                    <input
                        className="outline-none px-5 py-2.5 rounded-md border-1 border-gray-300 w-full"
                        type="text"
                        id="project-name-field"
                        value={projectCreate.name}
                        onChange={(e) => setProjectCreate({ ...projectCreate, name: e.target.value})}
                        placeholder="Type project name here"
                        required
                        name="project-name"
                        autoComplete="project-name"

                    />

                    <label htmlFor="project-description-field">Project description</label>
                    <textarea
                        className="outline-none px-5 py-2.5 rounded-md border-1 border-gray-300 resize-none h-40"
                        id="project-description-field"
                        value={projectCreate.description}
                        onChange={(e) => setProjectCreate({ ...projectCreate, description: e.target.value})}
                        placeholder="Type description here"
                        required
                        name="project-name"
                        autoComplete="project-name"
                        
                    />
                    <label htmlFor="project-visibility-field">Project visibility</label>
                    <div className="relative cursor-pointer">
                        <input 
                            className="outline-none px-5 py-2.5 rounded-md border-1 border-gray-300 w-full cursor-pointer"
                            type="" 
                            value={projectCreate.visibility}
                            name="project-visibility"
                            readOnly
                            onClick={() => setIsDropList(!isDropList)}
                        />   
                        <span className="absolute top-1/2 -translate-1/2 right-1 cursor-pointer" onClick={() => setIsDropList(!isDropList)}>
                            <svg  height="15px" width="12px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" viewBox="0 0 185.343 185.343" xmlSpace="preserve" fill="#000000" transform="rotate(90)"><g id="SVGRepo_bgCarrier" strokeWidth="0"></g><g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <g> <path fill="#010002" d="M51.707,185.343c-2.741,0-5.493-1.044-7.593-3.149c-4.194-4.194-4.194-10.981,0-15.175 l74.352-74.347L44.114,18.32c-4.194-4.194-4.194-10.987,0-15.175c4.194-4.194,10.987-4.194,15.18,0l81.934,81.934 c4.194,4.194,4.194,10.987,0,15.175l-81.934,81.939C57.201,184.293,54.454,185.343,51.707,185.343z"></path> </g> </g> </g></svg>
                        </span>
                        { isDropList && (
                            <ul className="absolute flex flex-col h-fit bg-white border-gray-300 border-1 rounded-md w-full  top-13/12 left-0 z-6 ">
                                {dropList.map((item, id) => (
                                    <li 
                                        key={id}
                                        onClick={() => {
                                            setProjectCreate({...projectCreate, visibility: item});
                                            setIsDropList(false);
                                        }}  
                                        className={`flex w-full cursor-pointer ${projectCreate.visibility == item ? "bg-gray-200" : "hover:bg-gray-200"} px-5 py-2.5`}
                                    >
                                        {item}
                                    </li>
                                ))}
                                
                            </ul>
                        )}

                    </div>
                </div>
                <div className="flex justify-center p-5 gap-5 w-full">
                    <Button 
                        typeStyle="primary"
                        text="Cancel"
                        type="button"
                        onClick={onClose}
                        width="w-1/2"
                    />
                    <Button 
                        typeStyle="secondary"
                        text="Create"
                        type="submit"
                        width="w-1/2"
                    />

                </div>

            </form>
                    
        </section>
        </>

    )
}

export default ProjectCreate;