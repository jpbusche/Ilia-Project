import ReactDOM from "react-dom/client";
import App from "./App";
import Login from "./pages/Login"
import Cart from "./pages/Cart"
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import History from "./pages/History";

ReactDOM.createRoot(document.getElementById("root")).render(
  <BrowserRouter>
    <Routes>
        <Route path="/" element={<App />} />
        <Route path="/login" element={<Login />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/history" element={<History />} />
    </Routes>
  </BrowserRouter>
);