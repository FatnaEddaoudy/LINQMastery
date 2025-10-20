

export default function Home({Aboutinfo}){
    return(
        <>
        {Aboutinfo.map((a,i)=> (
        <div key={i}>
        <h2 >{a.naam}</h2>
        <h1>{a.role}</h1>
        </div>
      )
      )}
       <img src="./images/Gt_21DF.jpg" alt=""/>
       </>
    );
}
