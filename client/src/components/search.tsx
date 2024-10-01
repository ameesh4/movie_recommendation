import { useEffect, useState } from 'react';
import plus from '../assets/plus.png';
import axios from 'axios';
import {useNavigate } from 'react-router-dom';

export type response = {
    id: number,
    title: string,
    genre_name: string[],
    release_date: string,
    overview: string,
    poster_path: string,
    vote_average: number,
}


export default function Search() {
    const [search, setSearch] = useState("");
    const [data, setData] = useState([] as response[]);
    const [selected, setSelected] = useState([] as response[]);
    const selectedString = selected.map((item: response) => item.title).join(" | ");
    const [error, setError] = useState("");
    const navigate = useNavigate();

    if(selected.length === 5){
        try{
            axios.post('http://localhost:8000', selected)
        }catch(err){
            console.log(err);
        }
    }

    useEffect(() => {
        const delayDebounceFn = setTimeout(()=> {
            try{
                if (search.length > 0){
                    const temp = search.replace(" ", "+");
                console.log("requesting data")
                fetch(`http://127.0.0.1:8000/${temp}`)
                .then(res=>{
                    if(!res.ok){
                        console.log("error");
                    }

                    return res.json();
                })                
                .then(data=>{
                    if (data.error){
                        setError(data.error);
                        return;
                    }else{
                        setData(data.data);
                    }
                })
                .catch(err=>{
                    console.log(err);
                });
            }
            }catch(err){
                console.log(err);
            }
        }, 1000)

        return () => clearTimeout(delayDebounceFn);
    }, [search]);

    function handleSelect(item: response){
        if(selected.length === 5){
            setError("You can't select more than 5 movies");
            return;
        }

        if (selected.includes(item)){
            setError("You have already selected this movie");
            return;
        }

        if(selected.length === 0){
            setSelected([item]);
        }else{
            setSelected([...selected, item]);
        }
    }

    function handleClick(){
        if (selected.length < 2){
            setError("Please select atleast two movies");
            return;
        }
        navigate("/recommendations", {state: selected});
    }

    return (
        <div className="block w-full text-center transition-transform">
            { selectedString &&
                <div className="block h-full" dangerouslySetInnerHTML={
                    {__html: `<div class='block bg-clip-content mb-2'>Movies Selected: ${selectedString}</div>`}
                }>
            </div>
            }
            <div>
                <h1 className='text-red-800'>{error}</h1>
            </div>
            <input autoComplete='off' className="p-5 w-full h-full rounded-lg border-4" placeholder="Search..." type="text" onChange={(e)=> setSearch(e.target.value)} value={search}/>
            <div className='block bg-clip-content max-h-screen'>
                <ul>
                { 
                    data.map((item: any) => {
                        return (
                            <li className='flex border-2 border-t-0 border-gray-300 p-2 text-left' key={item.id}>
                                <img className='block h-20' src={`https://image.tmdb.org/t/p/w1280/${item.poster_path}`} alt={item.title}/>
                                <div className='main ml-2 w-full'>
                                    <div className='block' >
                                        <p className='font-bold text-blue-900 text-xl'>{item.title}</p>
                                    </div>
                                    <div className='block'>
                                        <p className='text-yellow-800'>Rating: {item.vote_average}</p>
                                    </div>
                                    <div className='block'>
                                        <p>Release Date: {item.release_date}</p>
                                    </div>
                                </div>
                                <button 
                                className='flex w-20 justify-center items-center rounded-md border-2 hover:bg-gray-200'
                                onClick={()=> handleSelect(item)}
                                >
                                    <div className='w-5'>
                                        <img src={plus} alt="plus" />
                                    </div>
                                </button>
                            </li>
                        );
                    })
                }
                </ul>
            </div>
            <div className='block h-10 m-2' >
                    <button className='h-full w-20 bg-blue-500 rounded-md text-white hover:bg-blue-600' onClick={handleClick}>Go</button>
            </div>
        </div>
    );
}