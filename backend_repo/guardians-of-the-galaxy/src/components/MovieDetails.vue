<template>
  <div class="movie-container">
    <!-- Logo - Clickable at the top-left corner -->
    <div class="logo-container">
      <img src="@/assets/logo.png" alt="Logo" class="logo" @click="goToHomePage" />
    </div>

    <!-- Movie Header: Poster and Title -->
    <div class="movie-header" :style="{ backgroundImage: `url(${movieData.Poster})` }">
      <div class="overlay">
        <h1>{{ movieData.Title }}</h1>
        <p>{{ movieData.Year }} | {{ movieData.Genre }}</p>
        <p class="movie-tagline">{{ movieData.Plot }}</p>
      </div>
    </div>

    <!-- Movie Details Section -->
    <div class="movie-details">
      <p><strong>Director:</strong> {{ movieData.Director }}</p>
      <p><strong>Actors:</strong> {{ movieData.Actors }}</p>
      <p><strong>IMDb Rating:</strong> {{ movieData.imdbRating }} / 10</p>
    </div>

    <!-- Displaying Posts and Comments -->
    <div class="posts-container">
      <div v-for="post in posts" :key="post.id" class="post">
        <!-- Post Header -->
        <div class="post-header">
          <h3>{{ post.author }} | {{ formatDate(post.timestamp) }}</h3>
          <p>{{ post.text }}</p>
        </div>

        <!-- Comments Section -->
        <div class="comments" v-if="post.comments.length > 0">
          <div v-for="comment in post.comments" :key="comment.id" class="comment">
            <p><strong>{{ comment.author }}:</strong> {{ comment.text }}</p>
            <p><small>{{ formatDate(comment.timestamp) }}</small></p>
          </div>
        </div>
        <p v-else>No comments yet.</p>

        <!-- Like Button for each Post -->
        <button @click="likePost(post.id)" class="like-button">Like</button>
      </div>

      <!-- Infinite Scroll Loading Indicator -->
      <div v-if="loading" class="loading">Loading...</div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      movieData: {}, // Movie data from OMDb API
      posts: [], // Posts fetched from the backend
      page: 1, // Pagination for posts
      loading: false, // Loading state for infinite scroll
      hasMorePosts: true, // Flag to check if more posts are available
    };
  },
  created() {
    this.fetchMovieData(); // Fetch movie details on component creation
    this.fetchPosts(); // Fetch posts from backend API
    window.addEventListener("scroll", this.handleScroll); // Infinite scrolling
  },
  methods: {
    // Fetch movie data from OMDb API
    async fetchMovieData() {
      const apiUrl = "http://www.omdbapi.com/?i=tt3896198&apikey=d2132124"; // Guardians of the Galaxy Vol. 2
      try {
        const response = await axios.get(apiUrl);
        this.movieData = response.data;
      } catch (error) {
        console.error("Error fetching movie data", error);
      }
    },

    // Fetch posts from the backend API
    async fetchPosts() {
      if (this.loading || !this.hasMorePosts) return; // Prevent multiple requests

      this.loading = true;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/api/posts/?page=${this.page}`);
        const newPosts = response.data.results;
        this.posts = [...this.posts, ...newPosts]; // Append new posts to the existing list
        this.hasMorePosts = response.data.next !== null; // Check if there are more posts to fetch
        this.page++; // Increment the page number for the next request
      } catch (error) {
        console.error("Error fetching posts:", error);
      } finally {
        this.loading = false;
      }
    },

    // Infinite scroll handler
    handleScroll() {
      const scrollPosition = window.innerHeight + window.scrollY;
      const bottomPosition = document.documentElement.offsetHeight;

      if (scrollPosition >= bottomPosition - 200 && !this.loading && this.hasMorePosts) {
        this.fetchPosts(); // Fetch more posts when scrolling near the bottom
      }
    },

    // Format date for display
    formatDate(timestamp) {
      const date = new Date(timestamp);
      return `${date.toLocaleDateString()} ${date.toLocaleTimeString()}`;
    },

    // Handle "Like" button click for each post
    likePost(postId) {
      alert(`Liked post with ID: ${postId}`);
    },

    // Handle logo click - redirect to homepage or any desired route
    goToHomePage() {
      this.$router.push("/"); // Assuming you have Vue Router setup
    },
  },
  beforeUnmount() {
    // Remove the scroll event listener when the component is destroyed
    window.removeEventListener("scroll", this.handleScroll);
  },
};
</script>

<style scoped>
.movie-container {
  color: white;
  font-family: Arial, sans-serif;
  background-color: #121212; /* Dark background for the container */
}

/* Logo - clickable in the upper left corner */
.logo-container {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 1000;
}

.logo {
  width: 50px;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.1);
}

/* Movie Header Section */
.movie-header {
  height: 300px; /* Reduced size for the poster */
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5); /* Subtle shadow effect */
}

.overlay {
  text-align: center;
  padding: 20px;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 10px;
  width: 80%;
}

.movie-header h1 {
  font-size: 3em;
  text-shadow: 2px 2px 8px rgba(0, 0, 0, 0.7);
  margin-bottom: 15px;
}

.movie-header p {
  font-size: 1.2em;
  text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.7);
}

.movie-tagline {
  font-size: 1.5em;
  font-style: italic;
  margin-top: 10px;
}

/* Movie Details Section */
.movie-details {
  padding: 20px;
  font-size: 1.2em;
  background-color: #1a1a1a; /* Darker background for the details section */
  border-radius: 10px;
  margin-top: -40px; /* Pull up the details section */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* Light shadow for separation */
}

/* Posts Section */
.posts-container {
  padding: 20px;
}

.post {
  margin-bottom: 30px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 20px;
  background-color: #2c3e50;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.post-header {
  font-size: 1.2em;
  margin-bottom: 10px;
}

.comment {
  background-color: #34495e;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 10px;
  color: white;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.comment p {
  margin: 5px 0;
}

.comment:hover {
  background-color: #3b4a60;
}

.like-button {
  background-color: #ff6347;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 1.2em;
  cursor: pointer;
}

.like-button:hover {
  background-color: #ff4500;
}

.loading {
  text-align: center;
  font-size: 1.2em;
  margin-top: 20px;
}

@media (max-width: 600px) {
  .movie-header {
    height: 300px;
  }

  .movie-header h1 {
    font-size: 2em;
  }

  .movie-details {
    font-size: 1em;
  }

  .post-header {
    font-size: 1em;
  }

  .comments {
    font-size: 0.9em;
  }
}
</style>
