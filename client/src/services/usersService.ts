import axios from 'axios';

class usersService {
    static apiUrl = 'http://localhost:8000/api/v1';

    static async login(username: string, password: string) {
        const { data } = await axios.post(`${this.apiUrl}/auth/login/`, {
            username,
            password,
        });

        return data.token;
    }

    static async register(username: string, email: string, password: string) {
        const { data } = await axios.post(`${this.apiUrl}/users/`, {
            username,
            email,
            password,
        });

        return data;
    }
}

export default usersService;