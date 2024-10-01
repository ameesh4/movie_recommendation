import NavBar from "../components/NavBar";
import Search from "../components/search";


export default function Home() {
  return (
    <div className="flex justify-center items-center bg-white min-h-screen">
      <div className="main w-2/5 text-center transition-transform">
        <h1 className="block text-blue-900 font-serif font-bold text-8xl" >Movies.io</h1>
        <h1 className="block text-blue-700 text-xl mb-10" >The Movie Recommendation system</h1>
        <h1 className="block text text-xl mb-2" >Please add your favorite movies. Atleast two. Atmost Five</h1>
        <Search />
      </div>
    </div>
  );
}