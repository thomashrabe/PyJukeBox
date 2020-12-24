<template>
    <div>
        <b-table striped hover :items="jukeboxDB" :fields="['container', 'card_id']">
            <!-- <b-tr v-for="jbFolder in jukeboxDB" :key="jbFolder.card_id">
                <b-td>
                    {{ jbFolder.container }}
                </b-td>
            </b-tr> -->
        </b-table>
        <b-button type="submit" variant="primary">asdf</b-button>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { DBProvider} from "../providers/dbProvider";
import { JBFolder } from "../classes/JukeboxDB";

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
