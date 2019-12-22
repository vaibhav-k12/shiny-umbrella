<template>
  <div id="app grid-container">
    <div class="header grid-x align-center">header</div>
    <div class="grid-x main align-center">
      <div class="image-container grid-y">
        <div class="grid-x">
          <img alt="Vue logo" class="grid-x" src="./assets/logo.png">
        </div>
      <HelloWorld msg="Welcome to Your Vue.js App"/>
      </div>
    </div>
    <div class="footer grid-x align-center">footer</div>
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'app',
  components: {
    // add more components here
    HelloWorld
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
