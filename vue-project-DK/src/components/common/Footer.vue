<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-text">
          <p>© 2025 NEWS_DK</p>
          <p class="footer-author">@DKREY_06</p>
        </div>
        <div class="footer-image">
          <img src="/images/CatQ.png" alt="Cat" class="footer-cat" />
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup></script>

<style scoped>
.footer {
  background: #2c3e50;
  color: white;
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}

.footer-text {
  flex: 1;
}

.footer-text p {
  margin: 0;
  color: #ecf0f1;
  font-size: 1rem;
}

.footer-author {
  margin-top: 0.5rem !important;
  color: #42b883 !important;
  font-weight: 500;
}

.footer-image {
  flex-shrink: 0;
}

.footer-cat {
  width: 60px;
  height: 60px;
  object-fit: contain;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.footer-cat:hover {
  transform: scale(1.1);
}

@media (max-width: 768px) {
  .footer {
    padding: 1.5rem 0;
  }

  .footer-content {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .footer-cat {
    width: 50px;
    height: 50px;
  }

  .container {
    padding: 0 1rem;
  }
}

@media (max-width: 480px) {
  .footer {
    padding: 1rem 0;
  }

  .footer-text p {
    font-size: 0.9rem;
  }

  .footer-cat {
    width: 40px;
    height: 40px;
  }
}
</style>
