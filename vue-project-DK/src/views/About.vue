<template>
  <div class="about-page">
    <div class="container">
      <h1>О нас и нашем проекте</h1>
      <hr class="featurette-divider" />

      <div class="row featurette">
        <div class="col-md-7">
          <h2 class="featurette-heading fw-normal lh-1">
            Читайте наши классные статьи!
            <span class="text-body-secondary"
              >Вам обязательно понравиться :)</span
            >
          </h2>
          <p class="lead">
            NEWS_DK - это современный новостной блог, где публикуются актуальные
            статьи на различные темы. Мы стремимся предоставлять качественный
            контент, который будет интересен и полезен нашим читателям.
          </p>
        </div>
        <div class="col-md-5">
          <img src="/images/News_about.png" width="300px" alt="News About" />
        </div>
      </div>

      <hr class="featurette-divider" />

      <div class="row featurette">
        <div class="col-md-7 order-md-2">
          <h2 class="featurette-heading fw-normal lh-1">
            Немного о создателе :)
            <span class="text-body-secondary">Он прикольный</span>
          </h2>
          <p class="lead">
            Создатель сайта - Кретов Дмитрий, студент ДВФУ. Этот проект
            разработан как лабораторная работа
          </p>
        </div>
        <div class="col-md-5 order-md-1">
          <img src="/images/Creator.jpg" width="300px" alt="Creator" />
        </div>
      </div>

      <hr class="featurette-divider" />
    </div>
  </div>
</template>

<script setup></script>

<style scoped>
.about-page {
  padding: 2rem 5rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 2.5rem;
}

.featurette-divider {
  margin: 4rem 0;
  border: 0;
  border-top: 1px solid #eee;
}

.row.featurette {
  display: flex;
  align-items: center;
  margin-bottom: 4rem;
}

.col-md-7 {
  flex: 0 0 58.333333%;
  max-width: 58.333333%;
  padding: 0 15px;
}

.col-md-5 {
  flex: 0 0 41.666667%;
  max-width: 41.666667%;
  padding: 0 15px;
  text-align: center;
}

.order-md-1 {
  order: 1;
}

.order-md-2 {
  order: 2;
}

.featurette-heading {
  font-size: 2rem;
  font-weight: 400;
  line-height: 1.2;
  margin-bottom: 1rem;
}

.text-body-secondary {
  color: #6c757d;
}

.lead {
  font-size: 1.25rem;
  font-weight: 300;
  line-height: 1.6;
}

img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .row.featurette {
    flex-direction: column;
    text-align: center;
  }

  .col-md-7,
  .col-md-5 {
    flex: 0 0 100%;
    max-width: 100%;
    margin-bottom: 2rem;
  }

  .order-md-1,
  .order-md-2 {
    order: 0;
  }

  .featurette-heading {
    font-size: 1.5rem;
  }

  .lead {
    font-size: 1.1rem;
  }
}
</style>
