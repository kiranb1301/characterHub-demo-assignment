<template>
  <div class="page" :class="{ 'is-loading': loading }" aria-busy="loading">
    <!-- ===== Top Nav ===== -->
    <header class="navbar" role="navigation" aria-label="Primary">
      <div class="nav-left">
        <button class="hamburger" aria-label="Open menu">☰</button>
        <span class="logo" @click="goHome" role="link" tabindex="0">TMDB-ish</span>
        <nav class="primary-links">
          <a href="#" aria-current="page">Movies</a>
          <a href="#">TV Shows</a>
          <a href="#">People</a>
          <a href="#">More</a>
        </nav>
      </div>
      <div class="nav-right">
        <button class="chip">EN</button>
        <button class="ghost">Login</button>
        <button class="cta">Join</button>
      </div>
    </header>

    <!-- ===== Tabs Row ===== -->
    <div class="tabs">
      <button class="tab active">Overview</button>
      <button class="tab">Media</button>
      <button class="tab">Fandom</button>
      <button class="tab">Share</button>
    </div>

    <!-- ===== Sticky Compact Header ===== -->
    <div class="sticky-mini" v-show="showMini">
      <div class="mini-title">
        {{ movie.Title }} <span>({{ movie.Year }})</span>
      </div>
      <div class="mini-actions">
        <button class="mini-btn">Like</button>
        <button class="mini-btn">✓ Watchlist</button>
        <button class="mini-cta">▶ Trailer</button>
      </div>
    </div>

    <!-- ===== HERO ===== -->
    <section
      class="hero"
      :style="{ backgroundImage: `url(${backdropUrl})` }"
      role="region"
      aria-label="Movie hero"
    >
      <div class="scrim">
        <!-- Poster -->
        <div class="poster">
          <div v-if="loading" class="poster-skel shimmer"></div>
          <img
            v-else
            :src="movie.Poster"
            :alt="`${movie.Title} poster`"
            loading="eager"
          />
          <div class="service-chip">
            Now Streaming
          </div>
        </div>

        <!-- Details -->
        <div class="details">
          <div class="title">
            <h1>
              {{ movie.Title }}
              <span class="year">({{ movie.Year }})</span>
            </h1>
          </div>

          <p class="meta">
            <span>{{ movie.Released }}</span>
            <span>•</span>
            <span>{{ movie.Runtime }}</span>
            <span>•</span>
            <span>{{ movie.Genre }}</span>
          </p>

          <!-- Actions row -->
          <div class="actions-row">
            <!-- Animated rating ring -->
            <div class="score">
              <div
                class="ring"
                :style="{
                  background: `conic-gradient(var(--ring-ok) ${scoreDeg}deg, var(--ring-muted) ${scoreDeg}deg)`
                }"
                aria-label="User score"
                role="img"
              >
                <div class="ring-inner">
                  <span>{{ scorePct }}</span>
                </div>
              </div>
              <span class="label">User Score</span>
            </div>

            <button class="pill">List</button>
            <button class="pill">Like</button>
            <button class="pill">Save</button>
            <button class="pill">★</button>

            <button class="trailer">
              ▶ Play Trailer
            </button>
          </div>

          <!-- Tagline -->
          <p class="tagline"><em>{{ movie.Plot }}</em></p>
          <!-- Credits -->

          <!-- Overview -->
          <h2 class="section-h">Overview</h2>
          <p class="overview">
            {{ movie.Plot }}
          </p>

          <!-- Credits -->
          <div class="credits">
            <!-- Director(s) -->
            <div class="credit">
              <span>Director(s):</span>
              <strong>{{ movie.Director ? movie.Director.split(', ').join(', ') : '—' }}</strong>
            </div>

            <!-- Writer(s) -->
            <div class="credit">
              <span>Writer(s):</span>
              <strong>{{ movie.Writer ? movie.Writer.split(', ').join(', ') : '—' }}</strong>
            </div>

            <!-- Actor(s) with toggle -->
           <div class="credit">
                <div class="credit">
                  <span>Main Cast:</span>
                  <span class="credit-value">
                    <span v-if="!showFullCast">
                      {{ movie.Actors ? movie.Actors.split(', ').slice(0, 3).join(', ') : '—' }}
                      <span v-if="movie.Actors && movie.Actors.split(', ').length > 3">
                        ... <a href="#" @click.prevent="showFullCast = true">more</a>
                      </span>
                    </span>
                    <span v-else>
                      {{ movie.Actors }}
                      <a href="#" @click.prevent="showFullCast = false">less</a>
                    </span>
                  </span>
                </div>


            </div>

          </div>

        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "MoviePage",
  data() {
    return {
      loading: true,
      movie: {},
      leadActor: "",
      writers: [],
      showMini: false,
      fallbackBackdrop:
        "https://image.tmdb.org/t/p/original/8Y43POKjjKDGI9MH89NW0NAzzp8.jpg",
    };
  },
  computed: {
    scorePct() {
      const n = Number(this.movie.imdbRating || 0);
      return `${Math.round(n * 10)}%`;
    },
    scoreDeg() {
      const n = Number(this.movie.imdbRating || 0);
      return Math.min(360, Math.max(0, (n / 10) * 360));
    },
    backdropUrl() {
      return this.movie?.Poster || this.fallbackBackdrop;
    },
  },
  async created() {
    try {
      const res = await fetch(
        "http://www.omdbapi.com/?i=tt3896198&apikey=d2132124"
      );
      const data = await res.json();
      this.movie = data;
      this.leadActor = (data.Actors || "").split(",")[0]?.trim() || "";
      this.writers = (data.Writer || "")
        .split(",")
        .map((w) => w.trim())
        .filter((w) => w);
    } catch (e) {
      console.error(e);
    } finally {
      this.loading = false;
    }

    window.addEventListener("scroll", this.onScroll, { passive: true });
  },
  beforeUnmount() {
    window.removeEventListener("scroll", this.onScroll);
  },
  methods: {
    onScroll() {
      this.showMini = window.scrollY > 220;
    },
    goHome() {
      if (this.$router) this.$router.push("/");
    },
  },
};
</script>

<style scoped>
/* ========== Base ========== */
:root {
  --nav: #032541;
  --nav-grad: linear-gradient(90deg, #032541, #064663);
  --ink: #f4f9fc;
  --ink-soft: #d7e5ef;
  --brand: #01b4e4;
  --ring-bg: #081c22;
  --ring-ok: #21d07a;
  --ring-muted: #204529;
}
* { box-sizing: border-box; transition: all .25s ease; }
.page {
  min-height: 100vh;
  color: var(--ink);
  background: #0a1626;
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
}

/* ========== Navbar ========== */
.navbar {
  position: sticky;
  top: 0;
  z-index: 50;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--nav-grad);
  color: #fff;
  padding: 14px 24px;
  box-shadow: 0 4px 10px rgba(0,0,0,.25);
}
.logo { font-weight: 800; letter-spacing: .5px; cursor: pointer; font-size: 18px; }
.primary-links { display: none; gap: 18px; }
.primary-links a {
  color: #e8f6fc;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  position: relative;
}
.primary-links a::after {
  content: "";
  position: absolute;
  left: 0; bottom: -3px;
  width: 0%; height: 2px;
  background: var(--brand);
  transition: width .3s ease;
}
.primary-links a:hover::after { width: 100%; }
.primary-links a[aria-current="page"] { color: #fff; }

/* ========== Tabs row ========== */
.tabs {
  display: flex;
  gap: 6px;
  align-items: center;
  background: #0d2136;
  border-bottom: 1px solid rgba(255,255,255,.06);
  padding: 8px 12px;
}
.tab {
  background: transparent;
  color: #cfe9f7;
  border: 0;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  position: relative;
}
.tab:hover { background: rgba(255,255,255,.08); }
.tab.active {
  color: #fff;
  background: rgba(1,180,228,.22);
  box-shadow: inset 0 -3px 0 var(--brand);
}

/* ========== Hero ========== */
.hero { background-size: cover; background-position: center; }
.scrim {
  background: linear-gradient(135deg, rgba(5,18,33,.88), rgba(5,18,33,.95));
  padding: 28px 18px;
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 26px;
}
.poster { position: relative; overflow: hidden; border-radius: 14px; }
.poster img {
  width: 100%;
  height: 390px;
  object-fit: cover;
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(0,0,0,.5);
}
.poster img:hover { transform: scale(1.05); }
.poster-skel { background: #10324a; border-radius: 14px; }
.service-chip {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background: linear-gradient(135deg, #ff7eb3, #ff758c); /* brighter gradient */
  color: #ffffff; /* white text for contrast */
  font-weight: 700;
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
}

/* Details */
.details { min-width: 0; color: #f1f7fc; }
.title h1 { font-size: clamp(26px, 3.2vw, 42px); line-height: 1.1; margin: 6px 0 2px; color: #ffffff; }
.year { color: var(--ink-soft); font-weight: 600; }
.meta { display: flex; flex-wrap: wrap; gap: 8px; color: #cde6f4; margin: 6px 0 14px; }

.actions-row { display: flex; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 16px; }
.pill {
  background: rgba(255,255,255,.14);
  color: #f3faff;
  border: 1px solid rgba(255,255,255,.22);
  padding: 10px 12px;
  border-radius: 999px;
  cursor: pointer;
}
.pill:hover { background: rgba(255,255,255,.25); transform: translateY(-2px); }
.trailer {
  background: linear-gradient(135deg, #1db954, #1ed760); /* fresh green gradient */
  color: #ffffff; /* white text for readability */
  border: 0;
  padding: 10px 16px;
  border-radius: 999px;
  font-weight: 800;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
  cursor: pointer;
  transition: transform 0.2s ease, background 0.3s ease;
}

.trailer:hover {
  transform: scale(1.08);
  background: linear-gradient(135deg, #17a34a, #1db954); /* darker on hover */
}

/* Rating ring */
.score { display: flex; align-items: center; gap: 10px; }
.ring-inner { color: #f4fff8; font-weight: 800; }
.label { font-weight: 700; color: #def5ea; }

/* Text sections */
.tagline { color: #c7ddec; margin: 6px 0 10px; font-size: 15px; }
.section-h { margin: 10px 0 6px; font-size: 20px; color: #ffffff; }
.overview {
  color: #f2f8fc;
  opacity: .96;
  line-height: 1.6;
}

/* Make credits a 2-column grid: label + value */
.credit {
  display: flex;
  align-items: flex-start;
  gap: 6px;
}

.credit span {
  color: #c5dbe9;
  font-size: 14px;
}

.cast-list {
  font-weight: 800;
  color: #fff;
  line-height: 1.6;
}
.credit strong,
.credit-value {
  font-weight: 600;
  color: #ffffff !important; /* force white */
}


/* ========== Sticky compact header ========== */
.sticky-mini {
  position: sticky;
  top: 52px; 
  z-index: 40;
  background: rgba(3,37,65,.92);
  backdrop-filter: saturate(120%) blur(6px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 14px;
  border-bottom: 1px solid rgba(255,255,255,.08);
}
.mini-title { font-weight: 700; color: #f1f9ff; }
.mini-title span { color: #b9d6e5; font-weight: 600; }
.mini-actions { display: flex; gap: 8px; align-items: center; }
.mini-btn { background: rgba(255,255,255,.14); color: #f9f9f9; border: 1px solid rgba(255,255,255,.18); border-radius: 6px; padding: 6px 10px; }
.mini-btn:hover { background: rgba(255,255,255,.25); }
.mini-cta { background: var(--brand); color: #042331; border: 0; border-radius: 6px; padding: 6px 12px; font-weight: 800; }
.mini-cta:hover { transform: scale(1.05); }

/* ========== Responsive breakpoints ========== */
@media (min-width: 1024px) {
  .primary-links { display: flex; }
  .scrim { padding: 34px 36px; gap: 34px; grid-template-columns: 320px 1fr; }
  .poster img { height: 470px; }
}
@media (min-width: 768px) and (max-width: 1023px) {
  .scrim { grid-template-columns: 260px 1fr; }
}
@media (max-width: 767px) {
  .tabs { overflow-x: auto; }
  .tabs::-webkit-scrollbar { display: none; }
  .scrim { grid-template-columns: 1fr; gap: 18px; padding: 18px 14px 26px; }
  .poster img { height: 340px; }
  .actions-row { gap: 10px; }
  .credits { grid-template-columns: 1fr 1fr; }
}
.credit span {
  color: #c5dbe9;
  font-size: 14px;
  margin-right: 4px; /* added spacing */
}
.credit strong {
  font-weight: 800;
  color: #ffffff;
}
</style>
