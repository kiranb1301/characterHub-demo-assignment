<template>
  <div id="app">
    <MovieDetails />
  </div>
</template>

<script>
// Import the MovieDetails component
import MovieDetails from './components/MovieDetails.vue';

export default {
  name: 'App',
  components: {
    MovieDetails // Register MovieDetails component
  }
};
</script>

<style>
#app {
  text-align: center;
  margin-top: 20px;
}

h1 {
  font-size: 2em;
  margin-bottom: 20px;
}

img {
  max-width: 200px;  /* Adjust the size of the logo */
  margin-bottom: 20px;
}
</style>
