import axios from 'axios';

class usersService {
    static apiUrl = 'http://localhost:8000/api/v1';

    static async login(email: string, password: string) {
        const { data } = await axios.post(`${this.apiUrl}/auth/login/`, {
            email,
            password,
        });

        return data.token;
    }

    static async register(name: string, email: string, password: string) {
        const { data } = await axios.post(`${this.apiUrl}/users/register/`, {
            name,
            email,
            password,
        });

        return data;
    }
}

export default usersService;