import {useEffect, useState} from "react";
import Header from "../components/Header";
import "../css/History.css"

function History() {

    const [hist, setHistory] = useState([]);
    const apiUrl = import.meta.env.API_URL || "http://localhost:8000";

    const formatDate = (isoString) => {
        const date = new Date(isoString);
        return date.toLocaleString("pt-BR", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        });
    }

    const handleLogout = async () => {
        localStorage.removeItem("token");
        window.location.href = '/';
    }
    
    useEffect(() => {
        fetch(`${apiUrl}/orders`, {headers: {"Token": localStorage.getItem("token")}})
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                setHistory(data.history);
            } else {
                alert(data.message);
            }
        })
        .catch((err) => console.error("Erro ao buscar o historico", err))
    })

    return (
        <div>
            <Header/>
            {hist.length === 0 ? (
                <p>Sem historico de compras</p>
            ) : (
                <div className="history-container">
                    <h1>Historico de Compras:</h1>
                    {hist.map((order) => (
                        <div className="order-container">
                            <h3>Compra ID: {order.id}</h3>
                            <h3>Data da compra: {formatDate(order.order_date)}</h3>
                            <h3>Total da Compra: R$ {order.total_price.toFixed(2)}</h3>
                            <h3>Produtos:</h3>
                            <table className="history-table">
                                <thead>
                                    <tr>
                                        <th>Nome Produto</th>
                                        <th>Qtd</th>
                                        <th>Preço</th>
                                        <th>Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {order.products.map((product) => (
                                        <tr>
                                            <td>{product.name}</td>
                                            <td>{product.quantity}</td>
                                            <td>R$ {product.price.toFixed(2)}</td>
                                            <td>R$ {(product.price * product.quantity).toFixed(2)}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    ))}         
                </div>
            )}
            <button className="logout" onClick={handleLogout}>Logout</button>  
        </div>
    )
}

export default History