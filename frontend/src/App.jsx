import { useEffect, useState } from "react";
import CardProduto from "./components/CardProduto";
import Header from "./components/Header"

function App() {
    const [products, setProducts] = useState([]);
    const apiUrl = import.meta.env.API_URL || "http://localhost:8000";

    const fetchProducts = async () => {
        const response = await fetch(`${apiUrl}/products`)
        const data = await response.json();
        if (data.success) {
            setProducts(data.products);
        } else {
            alert(data.message);
        }
    }

    const handleProductAdded = () => {
        fetchProducts();
    }

    useEffect(() => {
        fetchProducts();
    }, []);

    return (
        <div className="app">
            <Header />
            <main className="main">
                <div className="cards-grid">
                    {products.map((product) => (
                        <CardProduto key={product.id} product={product} onProductAdded={handleProductAdded}/>
                    ))}
                </div>
            </main>
        </div>
    );
}

export default App;