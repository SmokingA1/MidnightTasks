import { create } from "zustand"
import { persist } from "zustand/middleware"
type UserState = {
    id: string;
    username: string;
    full_name?: string | null;
    avatar_url?: string | null;
    email: string;
    phone_number?: string | null;
}

type UserActions = {
    setUser: (data: UserState) => void;
    clearUser: () => void;
} 

type UserStore = UserState & UserActions;

const useUserStore = create(
    persist<UserStore>(
        (set) => ({
            id: "",
            username: "",
            full_name: null,
            avatar_url: null,
            email: "",
            phone_number: null,
            setUser: (data) => set(() => ({ ...data })),
            clearUser: () => set(() => ({
                id: "", username: "", full_name: null, avatar_url: null, email: "", phone_number: null
            })),
        }),
        {
            name: "user-store"
        }
    )
)

export default useUserStore