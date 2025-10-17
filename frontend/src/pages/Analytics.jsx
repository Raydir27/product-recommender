import { useEffect, useState } from "react";

export default function Analytics(){
  const [summary, setSummary] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/analyze/summary")
      .then(r => r.json())
      .then(setSummary)
      .catch(console.error);
  }, []);

  return (
    <div style={{padding:20}}>
      <h2>Analytics</h2>
      <pre>{JSON.stringify(summary, null, 2)}</pre>
    </div>
  );
}
