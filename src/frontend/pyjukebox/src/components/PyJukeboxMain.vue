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

        <b-button type="submit" variant="primary" @click="$bvModal.show('bv-modal-example')">
            Add content
        </b-button>

        <b-modal id="bv-modal-example" hide-footer ref='fileModal'>
            <template #modal-title>
                Upload new file
            </template>

            <!-- accept=".mp3, .m4a" -->
            <b-form-file
                v-model="files"
                :state="Boolean(file1)"
                placeholder="Choose an audio file..."
                drop-placeholder="Or drop file here..."
                multiple
            ></b-form-file>
            <p>{{ files ? files.names : ''}}</p>
            <b-button class="mt-3" color='primary' block @click="uploadFiles()">
                Upload
            </b-button>
            <b-button class="mt-3" block @click="$bvModal.hide('bv-modal-example')">
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

    constructor(){
        super();
    }

    mounted(){
        DBProvider.requestDB().then( result => {

            this.jukeboxDB = JBFolder.JBFolderGenerator(result.data);

        });
    }

    public formatFileName(fileName: string){
        const parts: string[] = fileName.split('/');
        return parts[parts.length - 1];
    }

    public addFileToFolder(dataIndex: number){
        const jbItem: JBFolder = this.jukeboxDB[dataIndex];

        this.$refs['fileModal'].show();
    }

    public addFileToNewFolder(){
        this.createNewFolder('test');
    }

    public uploadFiles(){
        console.log(this.files);
    }

    private createNewFolder(folderName: string){
        DBProvider.createNewFolder(folderName);
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
