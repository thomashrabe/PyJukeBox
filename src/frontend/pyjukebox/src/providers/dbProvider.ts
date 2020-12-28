import axios from "axios";
export class DBProvider {
    static config = {
        baseURL: "http://localhost:8000"
    }

    /**
     * Request DB JSON from backend
     */
    static requestDB() {
        const client = axios.create(DBProvider.config);
        return client.get("/db");
    }

    /**
     * Call the backend to create a new folder
     * @param newFolderName New folder name
     */
    static createNewFolder(newFolderName: string){
        const client = axios.create(DBProvider.config);
        return client.post("/addFolder/" + newFolderName);
    }
}
