import axios from 'axios';
import api from './axios';

class usersService {
    static async login(username: string, password: string) {
        const { data } = await api.post(`/auth/login/`, {
            username,
            password,
        });

        return {
            access: data.access,
            refresh: data.refresh,
        };
    }

    static async register(username: string, email: string, password: string) {
        const { data } = await api.post(`/users/`, {
            username,
            email,
            password,
        });

        return data;
    }
}

export default usersService;