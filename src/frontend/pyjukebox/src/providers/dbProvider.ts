import axios from 'axios';

export class DBProvider{
    static requestDB(): any{
        return axios.get('http://localhost:8000/db');
    }
}
