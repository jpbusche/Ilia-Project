import React, {useState} from "react";
import "../css/CardProduto.css"

function CardProduto({ product }) {
    const [quantity, setQuantity] = useState(1);
    const increment = () => setQuantity((q) => q + 1);
    const decrement = () => setQuantity((q) => Math.max(1, q - 1));
    const handleChange = (e) => {
        const value = parseInt(e.target.value, 10);
        setQuantity(isNaN(value) || value < 1 ? 1 : value);
    };
    return (
        <div className="card">
            <img src={product.image_link} alt={product.name} className={`card-img ${product.quantity === 0 ? 'out-of-stock': ''}`} />
            <div classnName="card-info">
                <p className="card-price">R$ {product.price.toFixed(2)}</p>
                <div className="card-actions">
                    <div className="quantity-control">
                        <input type="number" min="1" value={quantity} onChange={handleChange} />
                        <div className="arrow-buttons">
                            <button onClick={increment}>▲</button>
                            <button onClick={decrement}>▼</button>
                        </div>
                    </div>
                    <button className="btn-add">LISTA DE COMPRAS</button>
                </div>
            </div>
        </div>
    );
}

export default CardProduto;