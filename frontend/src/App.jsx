import React, { useEffect, useState } from "react";
import "./css/App.css";
import CardProduto from "./components/CardProduto";
import {FiUser, FiShoppingCart} from "react-icons/fi";

function App() {
    const [products, setProducts] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/products")
            .then((res) => res.json())
            .then((data) => {
                if (data.success) {
                    setProducts(data.products);
                } else {
                    alert(data.message);
                }
            })
            .catch((err) => console.error("Erro ao buscar produtos", err))
    }, []);

    return (
        <div className="app">
            <header className="header">
                <div className="logo">Fake Store</div>
                <div className="icons">
                    <FiUser className="icon"/>
                    <FiShoppingCart className="icon"/>
                </div>
            </header>
            <main className="main">
                <div className="cards-grid">
                    {products.map((product) => (
                        <CardProduto key={product.product_id} product={product}/>
                    ))}
                </div>
            </main>
        </div>
    );
}

export default App;