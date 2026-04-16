import React, { useState } from "react";
import axios from "axios";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const login = async () => {
    const res = await axios.post("http://127.0.0.1:8000/login", {
      email,
      password
    });

    alert(res.data.message);
  };

  return (
    <div>
      <h2>Login</h2>
      <input placeholder="Email" onChange={(e)=>setEmail(e.target.value)} />
      <br/>
      <input placeholder="Password" type="password" onChange={(e)=>setPassword(e.target.value)} />
      <br/>
      <button onClick={login}>Login</button>
    </div>
  );
}

export default Login;