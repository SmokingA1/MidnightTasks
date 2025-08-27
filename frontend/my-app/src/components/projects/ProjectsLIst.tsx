'use client'

import { api } from "@/api";
import React, { use, useEffect, useState } from "react";

interface ProjectInterface {
    id: string;
    name: string;
    owner_id: string;

}

const ProjectList = () => {
    const [projects, setProjects] = useState<ProjectInterface[]>([]);

    const fetchMyProjects = async () => {
     
        try {
            const response = await api.get("/project-participant/my")
            console.log(response.data);
            setProjects(response.data);
        } catch (error: any) {
            if (error.response) {
                console.error("Server error: ", error.response);
            } else {
                console.error("Network or other error: ", error);
            }
        }

    }

    useEffect(() => {
        fetchMyProjects();
    }, [])

    return(
        <ul>
            {projects && projects.map((project) => (
                <li key={project.id}>
                    {project.name}
                </li>
            ))}
        </ul>
    )
}