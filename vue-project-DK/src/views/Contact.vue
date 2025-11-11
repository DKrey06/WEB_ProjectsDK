<template>
  <div class="contact-page">
    <div class="container">
      <h1>Наши контакты</h1>
      
      <div class="contacts-container">
        <div class="contacts-box">
          <ul class="contacts-list">
            <li>
              <a href="https://t.me/DKrey_06" target="_blank" class="contact-link">
                📱 Telegram
              </a>
            </li>
            <li>
              <a href="https://vk.com/dkrey_06" target="_blank" class="contact-link">
                👥 VK
              </a>
            </li>
            <li>
              <a href="https://github.com/DKrey06" target="_blank" class="contact-link">
                💻 GitHub
              </a>
            </li>
            <li class="contact-item">
              📧 Mail: mrdmitry2006@mail.ru
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.contact-page {
  padding: 2rem 0;
  min-height: calc(100vh - 80px);
}

.contacts-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem 0;
}

.contacts-box {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.contacts-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.contacts-list li {
  padding: 1rem 0;
  border-bottom: 1px solid #eee;
}

.contacts-list li:last-child {
  border-bottom: none;
}

.contact-link {
  text-decoration: none;
  color: #2c3e50;
  font-weight: 500;
  transition: color 0.3s;
  display: block;
}

.contact-link:hover {
  color: #42b883;
}

.contact-item {
  color: #2c3e50;
  font-weight: 500;
}
</style>