
import type { Metadata } from "next";
import "./globals.css";
import useUserStore from "@/store/user";
import AuthChecker from "@/components/AuthChecker";

export const metadata: Metadata = {
    title: "Midnight-Tasks",
    description: "SmokingA1 is developer.",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {


    return (
        <html lang="en">
            <body
                className={`font-rb-normal antialiased bg-white`}
            >
                <AuthChecker>
                    {children}
                </AuthChecker>
            </body>
        </html>
    );
}
