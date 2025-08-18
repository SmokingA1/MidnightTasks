"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import useUserStore from "@/store/user";
import { api } from "@/api";

export default function AuthChecker({ children }: { children: React.ReactNode }) {
    const user = useUserStore();

    const checkAuth = async () => {
        try {
            const response = await api.get("/users/me");
            console.log(response.data);
        } catch (error) {
            user.clearUser();
        }
    }

    useEffect(() => {
        if (user.id) {
            checkAuth();
        }
    })

    return <>{children}</>;
}
