
export const PATH_SEPERATOR = '/';


export class JBFolder{

    public files: string[];
    public container: string;
    public card_id: string;

    static JBFolderGenerator(jsonData: any): JBFolder[]{
        const folders: JBFolder[] = [];

        Object.keys(jsonData).forEach((key: string) => {
            const files = jsonData[key];
            if ( 'STOP' === files || 'confirmation' === key){
                0;
            } else {
                folders.push(new JBFolder(files, key));
            }
        });

        return folders;
    }

    constructor(file_list: string[], card_id: string){
        this.files = file_list;
        const parts = file_list[0].split(PATH_SEPERATOR);
        this.container = parts[parts.length - 2];
        this.container = this.container.replaceAll('_', ' ');
        this.card_id = card_id;
    }

}