import { Link } from "react-router-dom";

export default function NavBar() {
    return (
        <div className="shadow-2xl">
            <div className="flex justify-between items-center bg-white h-20">
                <div className="flex p-8 items-center w-full">
                    <button className="font-bold font-serif text-blue-500 hover:text-blue-300">
                        <Link to="/">MOVIE.IO</Link>
                    </button>
                </div>
            </div>
        </div>
    );
}