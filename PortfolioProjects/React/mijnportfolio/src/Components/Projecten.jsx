

export default function Projecten({ProjectenLijst}){
    return(
    <>
    <h1>Projecten</h1>
    {ProjectenLijst.map((o,index)=>
      <div  key={index} className="card">
             <h2>{o.title}</h2>
              {Array.isArray(o.description)?
             (<ul>{o.description.map((d,i)=><li key={i}>{d}</li>)}</ul>) : (<p>{o.description}</p>)} 
        </div>
    )}
    </>
    );
}