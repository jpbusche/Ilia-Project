import {FiUser, FiShoppingCart} from "react-icons/fi";
import "../css/App.css";
import { useNavigate } from "react-router-dom";

function Header() {
    const navigate = useNavigate();

    const handleMenuClick = () => {
        navigate('/');
    }

    const handleUserClick = () => {
        navigate('/login');
    }

    return (
        <header className="header">
            <div className="logo" onClick={handleMenuClick}>Fake Store</div>
            <div className="icons">
                <FiUser className="icon" onClick={handleUserClick}/>
                <FiShoppingCart className="icon"/>
            </div>
        </header>
    );
}

export default Header;