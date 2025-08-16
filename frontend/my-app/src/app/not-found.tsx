'use client'
import { useEffect } from "react";


export const NotFound = () => {
    
    useEffect(() => {
        document.body.style.overflow = 'hidden'

        return () => {
        document.body.style.overflow = '';
        };
    }, [])

    return (
        <div className="relative flex justify-center font-glitch-md gap-2">
            <h2 className="relative text-5xl animate-drop-word-1 ">404</h2>
            <h2 className="relative text-5xl animate-drop-word-2">-</h2>
            <h2 className="relative text-5xl animate-drop-word-3">Page</h2>
            <h2 className="relative text-5xl animate-drop-word-4">Not</h2>
            <h2 className="relative text-5xl animate-drop-word-5">Found</h2>
            <h2 className="relative text-5xl animate-drop-word-6">!</h2>
            {/* <p className="text-lg">Page which you are searching does not exists!</p> */}
        </div>
    )

}

export default NotFound;