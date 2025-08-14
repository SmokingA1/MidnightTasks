import type { Metadata } from "next";
import "./globals.css";


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
        className={`font-rb-md antialiased bg-white`}
      >
        {children}
      </body>
    </html>
  );
}
