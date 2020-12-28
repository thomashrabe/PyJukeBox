<template>
    <div>
        <b-table striped hover :items="jukeboxDB" :fields="['container', 'card_id', 'show_details']">
            <template #cell(show_details)="row">
                <b-button variant="outline-primary" size="sm" @click="row.toggleDetails" class="mr-2">
                    <b-icon-chevron-expand v-if=" !row.detailsShowing "></b-icon-chevron-expand>
                    <b-icon-chevron-contract v-if=" row.detailsShowing "></b-icon-chevron-contract>
                </b-button>
                &nbsp;
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

        <b-button type="submit" variant="primary" v-on:click="addFileToNewFolder()">
            Add new item
        </b-button>

    </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { DBProvider} from "../providers/dbProvider";
import { JBFolder, PATH_SEPERATOR  } from "../classes/JukeboxDB"; 

@Component
export default class PyJukeboxMain extends Vue {

    public jukeboxDB: JBFolder[];

    public data = function() {
        return {counter: 4};
    };

    constructor(){
        super();
        this.jukeboxDB = [];
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

        console.log(jbItem);
    }

    public addFileToNewFolder(){
        this.createNewFolder('test');
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
