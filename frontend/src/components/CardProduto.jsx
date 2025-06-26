import {useState} from "react";
import "../css/CardProduto.css"

function CardProduto({ product, onProductAdded }) {
    const [quantity, setQuantity] = useState(1);
    const increment = () => setQuantity((q) => q + 1);
    const decrement = () => setQuantity((q) => Math.max(1, q - 1));
    const handleChange = (e) => {
        const value = parseInt(e.target.value, 10);
        setQuantity(isNaN(value) || value < 1 ? 1 : value);
    };
    const apiUrl = import.meta.env.API_URL || "http://localhost:8000";

    const handleAddProduct = async (e) => {
        const response = await fetch(`${apiUrl}/orders/add`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Token": localStorage.getItem("token")
            },
            body: JSON.stringify({
                id: product.id,
                quantity: quantity
            })
        });
        const data = await response.json();
        if (data.success) {
            alert("Item inserido com sucesso");
            onProductAdded();
        } else {
            alert(data.message);
        }
    }

    return (
        <div className="card">
            <img src={product.image_link} alt={product.name} className={`card-img ${product.quantity === 0 ? 'out-of-stock': ''}`} />
            <div classnName="card-info">
                <div className="card-price">
                    <span className="card-price">R$ {product.price.toFixed(2)}</span>
                    <span classname="card-price">Qtd Estoque: {product.quantity}</span>
                </div>
                <div className="card-actions">
                    <div className="quantity-control">
                        <input type="number" min="1" value={quantity} onChange={handleChange} />
                        <div className="arrow-buttons">
                            <button onClick={increment}>▲</button>
                            <button onClick={decrement}>▼</button>
                        </div>
                    </div>
                    <button className="btn-add" onClick={handleAddProduct}>LISTA DE COMPRAS</button>
                </div>
            </div>
        </div>
    );
}

export default CardProduto;