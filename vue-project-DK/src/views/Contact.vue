<template>
  <div class="contact-page">
    <div class="container">
      <h1>Наши контакты</h1>
      <p class="page-subtitle">Свяжитесь с нами удобным для вас способом</p>
      
      <div class="contacts-container">
        <div class="contacts-box">
          <div class="contacts-header">
            <h2>Мы в социальных сетях</h2>
            <p>Подписывайтесь и будьте в курсе новостей</p>
          </div>
          
          <ul class="contacts-list">
            <li>
              <a href="https://t.me/DKrey_06" target="_blank" class="contact-link">
                <div class="contact-icon telegram-icon">
                  <img src="/images/telegram-icon.png" alt="Telegram" class="icon-image">
                </div>
                <div class="contact-info">
                  <span class="contact-name">Telegram</span>
                  <span class="contact-handle">@DKrey_06</span>
                </div>
                <span class="contact-arrow">→</span>
              </a>
            </li>
            <li>
              <a href="https://vk.com/dkrey_06" target="_blank" class="contact-link">
                <div class="contact-icon vk-icon">
                  <img src="/images/vk-icon.png" alt="VK" class="icon-image">
                </div>
                <div class="contact-info">
                  <span class="contact-name">VK</span>
                  <span class="contact-handle">dkrey_06</span>
                </div>
                <span class="contact-arrow">→</span>
              </a>
            </li>
            <li>
              <a href="https://github.com/DKrey06" target="_blank" class="contact-link">
                <div class="contact-icon github-icon">
                  <img src="/images/github-icon.png" alt="GitHub" class="icon-image">
                </div>
                <div class="contact-info">
                  <span class="contact-name">GitHub</span>
                  <span class="contact-handle">DKrey06</span>
                </div>
                <span class="contact-arrow">→</span>
              </a>
            </li>
            <li>
              <a class="contact-link" @click="copyEmail">
                <div class="contact-icon email-icon">
                  <img src="/images/email-icon.png" alt="Email" class="icon-image">
                </div>
                <div class="contact-info">
                  <span class="contact-name">Email</span>
                  <span class="contact-handle">mrdmitry2006@mail.ru</span>
                </div>
                <span class="contact-arrow" :class="{ 'copied': showCopiedMessage }">
                  {{ showCopiedMessage ? '✓' : '→' }}
                </span>
              </a>
              <div v-if="showCopiedMessage" class="copied-message">
                Email скопирован в буфер обмена!
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const showCopiedMessage = ref(false)

const copyEmail = async () => {
  try {
    await navigator.clipboard.writeText('mrdmitry2006@mail.ru')
    showCopiedMessage.value = true
    setTimeout(() => {
      showCopiedMessage.value = false
    }, 2000)
  } catch (err) {
    console.error('Ошибка копирования: ', err)
    const textArea = document.createElement('textarea')
    textArea.value = 'mrdmitry2006@mail.ru'
    document.body.appendChild(textArea)
    textArea.select()
    document.execCommand('copy')
    document.body.removeChild(textArea)
    showCopiedMessage.value = true
    setTimeout(() => {
      showCopiedMessage.value = false
    }, 2000)
  }
}
</script>

<style scoped>
.contact-page {
  padding: 2rem 0;
  min-height: calc(100vh - 80px);
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding-bottom: 5rem;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 2rem;
}

h1 {
  color: #2c3e50;
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.page-subtitle {
  text-align: center;
  color: #666;
  font-size: 1.1rem;
  margin-bottom: 3rem;
}

.contacts-container {
  max-width: 600px;
  margin: 0 auto;
}

.contacts-box {
  background: white;
  padding: 2.5rem;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  border: 1px solid #e9ecef;
}

.contacts-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 2px solid #f0f0f0;
}

.contacts-header h2 {
  color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.contacts-header p {
  color: #666;
  font-size: 1rem;
}

.contacts-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.contacts-list li {
  padding: 1.25rem 0;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.3s;
}

.contacts-list li:hover {
  background-color: #f8f9fa;
  border-radius: 8px;
  margin: 0 -0.5rem;
  padding: 1.25rem 0.5rem;
}

.contacts-list li:last-child {
  border-bottom: none;
}

.contact-link {
  text-decoration: none;
  color: inherit;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s;
  cursor: pointer;
}

.contact-link:hover {
  background-color: rgba(66, 184, 131, 0.05);
}

.contact-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 12px;
  flex-shrink: 0;
  transition: all 0.3s;
}

.telegram-icon {
  background: rgba(0, 136, 204, 0.1);
}

.vk-icon {
  background: rgba(76, 117, 163, 0.1);
}

.github-icon {
  background: rgba(51, 51, 51, 0.1);
}

.email-icon {
  background: rgba(66, 184, 131, 0.1);
}

.icon-image {
  width: 32px;
  height: 32px;
  object-fit: contain;
  transition: transform 0.3s;
}

.contact-link:hover .icon-image {
  transform: scale(1.1);
}

.contact-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.contact-name {
  font-weight: 600;
  color: #2c3e50;
  font-size: 1.1rem;
}

.contact-handle {
  color: #666;
  font-size: 0.9rem;
}

.contact-arrow {
  color: #42b883;
  font-size: 1.2rem;
  font-weight: bold;
  transition: all 0.3s;
  margin-left: auto;
}

.contact-arrow.copied {
  color: #28a745;
  transform: scale(1.2);
}

.contact-link:hover .contact-arrow:not(.copied) {
  transform: translateX(3px);
}

.copied-message {
  color: #28a745;
  font-size: 0.8rem;
  text-align: center;
  margin-top: 0.5rem;
  padding: 0.25rem;
  background-color: rgba(40, 167, 69, 0.1);
  border-radius: 4px;
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-5px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .container {
    padding: 0 1rem;
  }
  
  .contacts-box {
    padding: 2rem 1.5rem;
  }
  
  h1 {
    font-size: 2rem;
  }
  
  .contact-icon {
    width: 48px;
    height: 48px;
  }
  
  .icon-image {
    width: 28px;
    height: 28px;
  }
}

@media (max-width: 480px) {
  .contacts-box {
    padding: 1.5rem 1rem;
  }
  
  .contact-link {
    gap: 0.75rem;
  }
  
  .contact-name {
    font-size: 1rem;
  }
  
  .contact-handle {
    font-size: 0.8rem;
  }
  
  .contact-icon {
    width: 44px;
    height: 44px;
  }
  
  .icon-image {
    width: 24px;
    height: 24px;
  }
}
</style>