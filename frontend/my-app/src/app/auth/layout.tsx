import type { Metadata } from "next";

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
    <div className="bg-gray-200 flex justify-center items-center h-full w-full">
        {children}
    </div>
  );
}
