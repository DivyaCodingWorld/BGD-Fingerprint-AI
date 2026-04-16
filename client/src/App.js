import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);

  // File upload handler
  const handleUpload = (e) => {
    setFile(e.target.files[0]);
  };

  // Submit to backend
  const handleSubmit = async () => {
    if (!file) {
      alert("Please upload a fingerprint image");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);

      const res = await axios.post(
        "http://127.0.0.1:8000/predict",
        formData
      );

      setResult(res.data.blood_group);
      setLoading(false);
    } catch (err) {
      console.error(err);
      alert("Error in prediction");
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        height: "100vh",
        background: "linear-gradient(to right, #4facfe, #00f2fe)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          background: "white",
          padding: "30px",
          borderRadius: "15px",
          boxShadow: "0 10px 30px rgba(0,0,0,0.2)",
          textAlign: "center",
          width: "350px",
        }}
      >
        <h1 style={{ color: "#333" }}>
          🧠 AI Blood Group Detection System
        </h1>

        <input type="file" onChange={handleUpload} />
        <br />
        <br />

        <button
          onClick={handleSubmit}
          style={{
            padding: "12px 25px",
            background: "#4facfe",
            color: "white",
            border: "none",
            borderRadius: "10px",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          {loading ? "Processing..." : "Predict"}
        </button>

        {/* Result */}
        {result && (
          <h2 style={{ marginTop: "20px", color: "green" }}>
            Result: {result}
          </h2>
        )}
      </div>
    </div>
  );
}

export default App;



