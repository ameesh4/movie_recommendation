import { useLocation } from 'react-router-dom';
import { response } from '../components/search';
import { useEffect, useState } from 'react';
import axios from 'axios';
import NavBar from '../components/NavBar';
import star from '../assets/star.png';

export default function Recommend() {
    const location = useLocation();
    const data = location.state as response[];
    const [now, setNow] = useState({} as response);
    const [counter, setCounter] = useState(0);
    const [error, setError] = useState("");
    const [responseData, setResponseData] = useState([] as response[]);
    let confirmed = {} as response;

    useEffect(() =>{
        axios.post('http://localhost:8000/recommend', data)
        .then(res=>{
            return res.data;
        })
        .then(data=>{
            setResponseData(data.data);
            setNow(data.data[0]);
            setCounter(0);
        })
    }, [])

    function next(){
        if(counter === responseData.length - 1){
            setError("No more recommendations");
            return;
        }
        setCounter(counter + 1);
        setNow(responseData[counter]);
    }

    function handleClick(e: any){
        e.preventDefault();
        if(e.target.id === "next"){
            next();
        }
        if (e.target.id === "select"){
            confirmed = now;
        }
    }

    return (
        <>
            <NavBar />
            <div className="flex justify-center items-center bg-white">
                <div className='block h-full w-3/5 text-left shadow-lg p-4 rounded-md mt-10'>
                    <p className='my-10 text-5xl font-bold font-sans text-blue-500'>Recommendations:</p>
                    <div className='flex h-full'>
                        <img className="block w-96 rounded-md shadow-2xl" src={`https://image.tmdb.org/t/p/w1280/${now.poster_path}`} alt="" />
                        <div className='p-4 text-left ml-4'>
                            <div className='mb-10 full'>
                                <p className='font-bold text-5xl text-blue-950'>{now.title}</p>
                                <p className='text-xl mt-4 opacity-80'>{now.overview}</p>
                                <div className='flex text-xl text-yellow-800 mt-4'>
                                    <img className="h-7 mr-3" src={star} alt="" />
                                    <p>{now.vote_average}</p>
                                </div>
                                <div className='flex text-xl text-green-800 mt-4'>
                                    <p className='italic mr-2'>Release Data:</p>
                                    <p>{now.release_date}</p>
                                </div>
                            </div>
                            <div dangerouslySetInnerHTML={
                                {__html: `<div class='block bg-clip-content mb-2 text-red-600'>${error}</div>`}
                            }>
                            </div>
                            <div className='content-end'>
                                <div className='w-full'>
                                    <button id='next' onClick={handleClick} className='bg-blue-500 text-white rounded-md p-2 mt-4 hover:bg-blue-600 w-full'>Next</button>
                                </div>
                                <div className='w-full'>
                                    <button id='select' onClick={handleClick} key={now.id} className='bg-green-500 text-white rounded-md p-2 mt-4 hover:bg-green-600 w-full'>Select</button>
                                </div>
                                <div className='w-full'>
                                    <button id='next' onClick={handleClick} className='bg-red-500 text-white rounded-md p-2 mt-4 hover:bg-red-600 w-full'>Already Watched</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
        
    );
}