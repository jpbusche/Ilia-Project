import ReactDOM from "react-dom/client";
import App from "./App";
import Login from "./pages/Login"
import {BrowserRouter, Routes, Route} from 'react-router-dom';

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
        <Route path="/" element={<App />} />
        <Route path="/login" element={<Login />} />
    </Routes>
  </BrowserRouter>
);