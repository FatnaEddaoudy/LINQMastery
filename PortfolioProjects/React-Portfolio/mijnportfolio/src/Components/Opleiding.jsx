

export default function Opleiding({OpleingLijst}){

    return(
        <>
        <h1>Opleiding en Education</h1>
        {OpleingLijst.map((o,index)=>(
          <div  key={index} className="card">
             <h2>{o.title}</h2>
             <p><strong>{o.school}</strong> – {o.location}</p>
             <p>{o.startYear} tot {o.endYear}</p>
             {Array.isArray(o.description)?
             (<ul>{o.description.map((d,i)=><li key={i}>{d}</li>)}</ul>):(<p>{o.description}</p>)}
          </div>       
          ))}
        </>
    );
}