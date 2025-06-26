import {useState, useEffect} from "react";
import Header from "../components/Header";
import "../css/Cart.css"


function Cart() {
    const [order, setOrder] = useState({products: []});
    const [loading, setLoading] = useState(false)
    
    const apiUrl = import.meta.env.API_URL || "http://localhost:8000";
    const fetchCart = async (e) => {
        try {
            const response = await fetch(`${apiUrl}/orders/cart`, { 
                headers: {"Token": localStorage.getItem("token")}
            });
            const data = await response.json();
            if (data.success) {
                setOrder(data.order);
            } else {
                setOrder({products: []});
            }
        } catch (err) {
            console.error("Erro ao buscar o carrinho:", err);
        } finally {
            setLoading(false);
        }    
    }

    const handleRemove = async (productId) => {
        const response = await fetch(`${apiUrl}/orders/remove`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Token": localStorage.getItem("token")
            },
            body: JSON.stringify({
                id: productId
            })
        });
        const data = await response.json();
        if (data.success) {
            fetchCart();
        } else {
            alert(data.message);
        }
    };

    const handleSubmit = async (e) => {
        const response = await fetch(`${apiUrl}/orders/submit`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Token": localStorage.getItem("token")
            },
            body: JSON.stringify({
                id: order.id
            })
        });
        const data = await response.json();
        if (data.success) {
            fetchCart();
            alert("Compra finalizada!");
        } else {
            alert(data.message);
        }
    }

    useEffect(() => {
        fetchCart();
    }, [])

    if (loading) return <p>Carregando carrinho...</p>;
    else {
        return (
            <div>
                <Header />
                <div className="cart-container">
                    <h2>Carrinho de Compras</h2>
                    {order.products.length === 0 ? (
                        <p>Seu carrinho está vazio</p>
                    ): (
                        <div>
                            <table className="cart-table">
                                <thead>
                                    <tr>
                                        <th>Nome Produto</th>
                                        <th>Qtd</th>
                                        <th>Preço</th>
                                        <th>Total</th>
                                        <th></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {order.products.map((product) => (
                                        <tr>
                                            <td>{product.name}</td>
                                            <td>{product.quantity}</td>
                                            <td>R$ {product.price.toFixed(2)}</td>
                                            <td>R$ {(product.price * product.quantity).toFixed(2)}</td>
                                            <td>
                                                <button className="remove-btn" onClick={() => handleRemove(product.id)}>🗑️</button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                            <div className="cart-footer">
                                <strong>Total da Compra: R$ {order.total_price.toFixed(2)}</strong>
                                <button className="submit-btn" onClick={handleSubmit}>Finalizar Pedido</button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        )
    }
}

export default Cart;