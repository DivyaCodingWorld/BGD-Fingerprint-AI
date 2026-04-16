import React, { useEffect, useState } from "react";
import axios from "axios";

function History() {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/history")
      .then(res => setData(res.data));
  }, []);

  return (
    <div>
      <h2>Prediction History</h2>
      {data.map((item, index) => (
        <p key={index}>
          {item.filename} → {item.prediction}
        </p>
      ))}
    </div>
  );
}

export default History;