import { useEffect, useState } from "react";
import CardProduto from "./components/CardProduto";
import Header from "./components/Header"

function App() {
    const [products, setProducts] = useState([]);
    const apiUrl = import.meta.env.API_URL || "http://localhost:8000";

    useEffect(() => {
        fetch(`${apiUrl}/products`)
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
            <Header />
            <main className="main">
                <div className="cards-grid">
                    {products.map((product) => (
                        <CardProduto key={product.id} product={product}/>
                    ))}
                </div>
            </main>
        </div>
    );
}

export default App;