<template>
    <div>
        <b-table striped hover :items="jukeboxDB" :fields="['container', 'card_id', 'show_details']">
            <template #cell(show_details)="row">
                <b-button variant="outline-primary" size="sm" @click="row.toggleDetails" class="mr-2">
                    <b-icon-chevron-expand v-if=" !row.detailsShowing "></b-icon-chevron-expand>
                    <b-icon-chevron-contract v-if=" row.detailsShowing "></b-icon-chevron-contract>
                </b-button>
                <b-button variant="outline-primary" size="sm" @click="addFileToFolder(row.index)">
                    <b-icon-file-plus></b-icon-file-plus>
                </b-button>
            </template>

            <template #row-details="row">
                <b-list-group v-for="aFile in row.item.files" :key="aFile">
                    <b-list-group-item>
                        {{ formatFileName(aFile) }}
                        <b-button variant="outline-primary" size="sm">
                            <b-icon-file-minus></b-icon-file-minus>
                        </b-button>
                    </b-list-group-item>
                </b-list-group>
            </template>
        </b-table>

        <b-button type="submit" variant="primary" @click="$bvModal.show('bv-modal-folder')">
            Add content
        </b-button>

        <b-modal id="bv-modal-files" hide-footer ref='fileModal'>
            <template #modal-title>
                Upload new file
            </template>

            <!-- accept=".mp3, .m4a" -->
            <b-form-file
                v-model="files"
                :state="Boolean(files)"
                placeholder="Choose an audio file..."
                drop-placeholder="Or drop file here..."
                multiple
            ></b-form-file>
            <p>{{ files ? files.names : ''}}</p>
            <b-button class="mt-3" color='primary' block @click="uploadFiles()">
                Upload
            </b-button>
            <b-button class="mt-3" block @click="$bvModal.hide('bv-modal-files')">
                Close Me
            </b-button>
        </b-modal>

        <b-modal id="bv-modal-folder" hide-footer ref='folderModal'>
            <template #modal-title>
                Add new folder
            </template>
            <b-form-input v-model="newFolderName" placeholder="Enter your name"></b-form-input>
            <b-button class="mt-3" color='primary' block @click="createNewFolder()">
                Add
            </b-button>
            <b-button class="mt-3" block @click="$bvModal.hide('bv-modal-folder')">
                Close Me
            </b-button>
        </b-modal>

    </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { DBProvider} from "../providers/dbProvider";
import { JBFolder, PATH_SEPERATOR  } from "../classes/JukeboxDB"; 

@Component
export default class PyJukeboxMain extends Vue {

    public jukeboxDB: JBFolder[] = [];
    public files: string[] = undefined;
    public newFolderName: string = undefined;
    public addFileToFolderIndex: number = undefined;

    constructor(){
        super();
    }

    mounted(){
        DBProvider.requestDB().then( (result) => {

            this.jukeboxDB = JBFolder.JBFolderGenerator(result.data);

        });
    }

    public formatFileName(fileName: string){
        const parts: string[] = fileName.split('/');
        return parts[parts.length - 1];
    }

    public addFileToFolder(dataIndex: number){
        this.addFileToFolderIndex = dataIndex;
        this.$refs['fileModal'].show();
    }

    public addFileToNewFolder(){
        this.$refs['fileModal'].show();
    }

    public uploadFiles(){
        if ( this.newFolderName){
            console.log('Upload files to new folder');
            console.log('Finish with swipe card');
            this.newFolderName = undefined;
        } else {
            console.log('Upload files to existing folder');
            const jbFolder: JBFolder = this.jukeboxDB[this.addFileToFolderIndex];
            DBProvider
        }
    }

    public createNewFolder(){

        DBProvider.createNewFolder(this.newFolderName).then(() => {

            this.addFileToNewFolder();

        }).catch((error) => {

        });
    }

}
</script>

<style scoped>
h3 {
  margin: 40px 0 0;
}
tr {
  list-style-type: none;
  padding: 0;
}
tl {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
