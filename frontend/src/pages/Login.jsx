import {useState} from "react";
import Header from "../components/Header";
import "../css/Login.css";

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [emailModal, setEmailModal] = useState('');
    const [passwordModal, setPasswordModal] = useState('');
    const [name, setName] = useState('');
    const [showModal, setVisibility] = useState(false);
    const apiUrl = import.meta.env.API_URL || "http://localhost:8000";

    const handleLogin = async (e) => {
        e.preventDefault();
        const response = await fetch(`${apiUrl}/costumers/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                email: email,
                password: password
            })
        });
        const data = await response.json();
        if (data.success) {
            localStorage.setItem("token", data.token);
            window.location.href = '/';
        } else {
            alert(data.message);
            setEmail('');
            setPassword('');
        }
    }

    const resetField = () => {
        setEmailModal('');
        setPasswordModal('');
        setName('')
        setVisibility(false);
    }

    const handleCreate = async (e) => {
        e.preventDefault();
        const response = await fetch(`${apiUrl}/costumers/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                email: emailModal,
                password: passwordModal,
                name: name
            })
        });
        const data = await response.json();
        if (data.success) {
            alert('Usuário criado com sucesso!');
            resetField();
        } else {
            alert(data.message);
            resetField();
        }
    }

    return (
        <div className="login">
            <Header />
            <main>
                <form onSubmit={handleLogin} className="login-form">
                    <h2>Login</h2>
                    <input type="email" placeholder="E-mail" value={email} onChange={(e) => setEmail(e.target.value)} required />
                    <input type="password" placeholder="Senha" value={password} onChange={(e) => setPassword(e.target.value)} required />
                    <button type="submit">Login</button>
                    <button type="button" onClick={() => setVisibility(true)}>Sign In</button>
                </form>

                {showModal && (
                    <div className="modal">
                        <div className="modal-content">
                            <h3>Cadastrar Usuário</h3>
                            <form onSubmit={handleCreate} className="modal-form">
                                <input type="name" placeholder="Nome" value={name} onChange={(e) => setName(e.target.value)} required />
                                <input type="email" placeholder="E-mail" value={emailModal} onChange={(e) => setEmailModal(e.target.value)} required />
                                <input type="password" placeholder="Senha" value={passwordModal} onChange={(e) => setPasswordModal(e.target.value)} required />
                                <button type="submit">Cadastrar</button>
                            </form>
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}

export default Login;