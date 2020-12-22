import axios from "axios";
export class DBProvider {
    static config = {
        baseURL: "http://localhost:8000"
    }

    static requestDB() {
        const client = axios.create(DBProvider.config);
        return client.get("/db");
    }
}
