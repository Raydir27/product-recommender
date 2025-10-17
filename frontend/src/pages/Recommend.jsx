import { useState } from "react";

export default function Recommend(){
  const [prompt, setPrompt] = useState("modern wooden chair");
  const [res, setRes] = useState(null);

  async function runQuery(){
    const r = await fetch("http://localhost:8000/api/recommend/query", {
      method: "POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({ user_prompt: prompt, top_k: 3 })
    });
    const j = await r.json();
    setRes(j);
  }

  return (
    <div style={{padding:20}}>
      <h2>Recommendations</h2>
      <textarea value={prompt} onChange={e=>setPrompt(e.target.value)} rows={4} cols={60}/>
      <br/>
      <button onClick={runQuery}>Get recommendations</button>
      <pre>{JSON.stringify(res, null, 2)}</pre>
    </div>
  );
}
