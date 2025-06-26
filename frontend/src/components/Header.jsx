import {FiUser, FiShoppingCart} from "react-icons/fi";
import "../css/App.css";
import { useNavigate } from "react-router-dom";

function Header() {
    const navigate = useNavigate();

    const handleMenuClick = () => {
        navigate('/');
    }

    const handleUserClick = () => {
        if (!localStorage.getItem("token")) {
            navigate('/login');
        } else {
            navigate('/history');
        }
    }

    const handleCartClick = () => {
        if (localStorage.getItem("token")) {
            navigate('/cart');
        } else {
            alert("Para acessar o carinho necessita estar logado");
            navigate('/login')
        }
    }

    return (
        <header className="header">
            <div className="logo" onClick={handleMenuClick}>Fake Store</div>
            <div className="icons">
                <FiUser className="icon" onClick={handleUserClick}/>
                <FiShoppingCart className="icon" onClick={handleCartClick}/>
            </div>
        </header>
    );
}

export default Header;