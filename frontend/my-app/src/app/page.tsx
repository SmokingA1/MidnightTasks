
import { LogIn } from 'lucide-react';
import Link from 'next/link';

const Home = () => {
    return (
        <div id="home" className="font-rb-md">
            <header className=" w-full flex justify-between p-2.5">
                <span className='text-2xl text-teal-900'>Midnight Tasks</span>
                <div className="flex gap-2.5 font-medium">
                    <Link href={"/auth"} className='flex items-center hover:underline cursor-pointer'>
                        Sign in <LogIn size={22}/>
                    </Link>
                </div>
                
            </header>
            <main className='flex justify-center items-center flex-col'>
                Welcome to midnight tasks please log in
            </main>
        </div>
    );
}

export default Home;