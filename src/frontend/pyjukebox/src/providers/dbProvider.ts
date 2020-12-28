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
        return client.get("/addFolder/" + newFolderName);
    }

    /**
     * Call the backend to create a new folder
     * @param folderToRemove New folder name
     */
    static rmFolder(folderToRemove: string){
        const client = axios.create(DBProvider.config);
        return client.get("/rmFolder/" + folderToRemove);
    }

    /**
     * Call the backend to create a new folder
     * @param folder New folder name
     */
    static rmFile(folder: string, file_to_remove: string){
        const client = axios.create(DBProvider.config);
        return client.get("/rmFolder/" + folder + '/' + file_to_remove);
    }

    /**
     * Assign a RFID chip to a new folder
     * @param folder The new folder
     */
    static assignRFID(folder: string){
        const client = axios.create(DBProvider.config);
        return client.get("/assignRFID/" + folder);
    }
}
