<template>
  <div class="home">
    <PyJukeboxMain/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator"
import PyJukeboxMain from "@/components/PyJukeboxMain.vue" // @ is an alias to /src

@Component({
    components: {
        PyJukeboxMain
    }
})
export default class Main extends Vue {}
</script>
