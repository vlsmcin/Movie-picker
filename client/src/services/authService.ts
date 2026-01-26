import axios from 'axios';

class authService {
    static apiUrl = 'http://localhost:8000/api/v1/auth';

    static async login(username: string, email: string, password: string) {
        const { data } = await axios.post(`${this.apiUrl}/login`, {
            username,
            email,
            password,
        });

        return data.token;
    }
}

export default authService;