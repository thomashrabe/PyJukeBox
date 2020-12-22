<template>
  <div class="hello">
    {{ }}
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import { DBProvider} from "../providers/dbProvider";

@Component
export default class PyJukeboxMain extends Vue {

    constructor(){
        super();
        DBProvider.requestDB().then( result => {
            console.log(result);
        });
    }
}
</script>

<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
