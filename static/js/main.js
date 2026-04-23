

class ProfileCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    
    const fname = this.getAttribute('fname') || '';
    const lname = this.getAttribute('lname') || '';
    const photo = this.getAttribute('photo');
    const about = this.getAttribute('about') || '';
    const date = this.getAttribute('date') || '';
    const profileUrl = this.getAttribute('url') || '#';

   
    this.shadowRoot.innerHTML = `
    <style>
      :host { display: block; margin-bottom: 15px; }
      .profile-card { border: 1px solid #ddd; padding: 15px; border-radius: 8px; display: flex; gap: 15px; background: #fff; margin-top: 15px; }
      .avatar-wrapper { width: 60px; height: 60px; flex-shrink: 0; }
      .avatar { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; }
      .placeholder { background: #58525f; color: white; display: flex; align-items: center; justify-content: center; font-size: 24px; border-radius: 50%; height: 100%; }
      .profile-info h3 { margin: 0 0 5px 0; color: #333; }
      .profile-about { font-size: 14px; color: #000000; margin: 5px 0; }
      .profile-date { font-size: 12px; color: #999; }
      a { text-decoration: none; color: #000000; font-weight: bold; }
      .profile-card:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
    </style>

    <div class="profile-card">
      <div class="avatar-wrapper">
        ${photo 
          ? `<img src="${photo}" class="avatar">` 
          : `<div class="placeholder">${fname.charAt(0).toUpperCase()}</div>`
        }
      </div>

      <div class="profile-info">
        <h3 class="profile-name">
          <a href="${profileUrl}">${fname} ${lname}</a>
        </h3>
        ${about ? `<p class="profile-about">${about}</p>` : ''}
        <p class="profile-date">Регистрация: ${date}</p>
      </div>
    </div>
    `;

    const card = this.shadowRoot.querySelector('.profile-card');
    card.addEventListener('click', () => {
        window.location.href = profileUrl;
    });
    card.style.cursor = 'pointer';

  }
}

class UserPost extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    const data = {
      id: this.getAttribute('post-id'),
      authorName: this.getAttribute('author-name'),
      authorUrl: this.getAttribute('author-url'),
      authorPhoto: this.getAttribute('author-photo'),
      authorInitial: this.getAttribute('author-initial'),
      createdAt: this.getAttribute('created-at'),
      content: this.getAttribute('content'),
      postUrl: this.getAttribute('post-url'),
      postImage: this.getAttribute('post-image'),
      likesCount: this.getAttribute('likes-count'),
      isLiked: this.getAttribute('is-liked') === 'true',
      commentsCount: this.getAttribute('comments-count'),
      csrfToken: this.getAttribute('csrf-token'),
      actionUrl: this.getAttribute('action-url')
    };

  this.shadowRoot.innerHTML = `
<style>
  :host { 
    display: block; 
    margin-bottom: 25px; 
  }

  .post-card { 
    background: white; 
    border: 1px solid #eee;
    border-radius: 15px; 
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05); 
    transition: transform 0.2s ease;
    margin-bottom: 15px;
  }

  .post-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
  }

  .post-header { 
    display: flex; 
    align-items: center; 
    margin-bottom: 15px; 
  }

  .avatar { 
    width: 45px; 
    height: 45px; 
    border-radius: 50%; 
    object-fit: cover; 
    margin-right: 12px; 
    border: 1px solid #f0f0f0;
  }

  .placeholder { 
    width: 45px; 
    height: 45px; 
    border-radius: 50%; 
    background: #58525f; 
    color: white; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    margin-right: 12px;
    font-weight: bold;
  }

  .author-info a { 
    text-decoration: none; 
    color: #333; 
    font-weight: 700; 
    display: block; 
    margin-bottom: 2px;
  }

  .author-info a:hover {
    text-decoration: underline;
  }

  .post-date { 
    font-size: 12px; 
    color: #999; 
  }

  .post-content { 
    margin: 15px 0; 
  }

  .post-content a { 
    text-decoration: none; 
    color: #2c3e50; 
    line-height: 1.6; 
    font-size: 15px;
    display: block;
  }

  .post-image {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 15px -20px; 
    background: #f9f9f9;
  }

  .post-image img {
    max-width: 100%;
    max-height: 500px;
    object-fit: cover;
   
  }

  .post-footer-actions { 
    display: flex; 
    align-items: center; 
    gap: 15px; 
    margin-top: 15px; 
    border-top: 1px solid #f0f0f0; 
    padding-top: 15px; 
  }
 
  
  .like-btn { 
    background: #f8f9fa; 
    border: 1px solid #eee; 
    padding: 6px 12px;
    border-radius: 20px;
    cursor: pointer; 
    font-size: 14px; 
    display: flex; 
    align-items: center; 
    gap: 6px; 
    transition: all 0.2s; 
  }

  .like-btn:hover { 
    background: #f0f0f0;
    transform: scale(1.05);
  }

  .like-btn:active { 
    transform: scale(0.95); 
  }

  .comments-link { 
    text-decoration: none; 
    color: #58525f; 
    font-size: 14px; 
    font-weight: 500;
  }
  
  .comments-link:hover {
    text-decoration: underline;
  }
</style>

<article class="post-card">
  <div class="post-header">
    ${data.authorPhoto 
      ? `<img src="${data.authorPhoto}" class="avatar" alt="${data.authorName}">`
      : `<div class="placeholder">${data.authorInitial.charAt(0).toUpperCase()}</div>`
    }
    <div class="author-info">
      <a href="${data.authorUrl}">${data.authorName}</a>
      <span class="post-date">${data.createdAt}</span>
    </div>
  </div>

  <div class="post-content">
    <a href="${data.postUrl}">${data.content}</a>
  </div>

  ${data.postImage 
  ? `<div class="post-image">
       <img src="${data.postImage}" class="clickable-image" style="cursor:pointer;">
     </div>` 
  : ''}

  <div class="post-footer-actions">
    <form method="post" action="${data.actionUrl}" >
      <input type="hidden" name="csrfmiddlewaretoken" value="${data.csrfToken}">
      <input type="hidden" name="e_id" value="${data.id}">
      <button type="submit" class="like-btn">
        <span>${data.isLiked ? '❤️' : '🤍'}</span>
        <span style="font-weight: bold;">${data.likesCount}</span>
      </button>
    </form>

    <a href="${data.postUrl}#comments-section" class="comments-link">
      💬 Комментарии (${data.commentsCount})
    </a>
  </div>
</article>
`;
const img = this.shadowRoot.querySelector('.clickable-image');
if (img) {
  img.addEventListener('click', () => {
    openPostModal(data.id, data.postUrl);
  });
}
   

  }
}

customElements.define('user-post', UserPost);


customElements.define('profile-card', ProfileCard);

let _modalPostId = null;
let _modalIsLiked = false;

const IS_AUTHENTICATED = document.body.dataset.authenticated === 'true';
const CSRF_TOKEN = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';

async function openPostModal(postId, postUrl, csrfToken) {
  _modalPostId = postId;

  const resp = await fetch(`/blog/${postId}/modal/`);
  const d = await resp.json();

 
  const modalLeft = document.querySelector('.modal-left');
  const modalImg = document.getElementById('modal-img');
  if (d.image) {
    modalImg.src = d.image;
    modalLeft.style.display = 'flex';
    const saveBtn = document.getElementById('modal-save-btn');
    saveBtn.href = d.image;
    saveBtn.download = d.image.split('/').pop(); 
  } else {
    modalLeft.style.display = 'none';
  }

  
  document.getElementById('modal-author').textContent = d.author_name;
  document.getElementById('modal-author').href = d.author_url;
  document.getElementById('modal-date').textContent = d.created_at;
  document.getElementById('modal-content').textContent = d.content;
  document.getElementById('modal-full-link').href = postUrl;

  
  _modalIsLiked = d.is_liked; 
  updateLikeUI(d.likes_count, d.is_liked);

  
  renderComments(d.comments);

 
  const isAuth = document.body.dataset.authenticated === 'true';
  document.getElementById('modal-comment-form').style.display = isAuth ? 'flex' : 'none';
  document.getElementById('modal-login-hint').style.display = isAuth ? 'none' : 'block';

  
  document.getElementById('post-modal').style.display = 'flex';
  document.body.style.overflow = 'hidden';
}

function updateLikeUI(count, isLiked) {
  _modalIsLiked = isLiked;
  document.getElementById('modal-likes-count').textContent = count;
  document.getElementById('modal-like-icon').textContent = isLiked ? '❤️' : '🤍';
  const btn = document.getElementById('modal-like-btn');
  btn.classList.toggle('liked', isLiked);
}

function renderComments(comments) {
  const list = document.getElementById('modal-comments-list');
  if (!comments.length) {
    list.innerHTML = '<p class="no-comments">Комментариев пока нет</p>';
    return;
  }
  list.innerHTML = comments.map(c => `
    <div class="modal-comment">
      <a href="/blog${c.author_url}">${c.author}</a>
      <span>${c.text}</span>
    </div>
  `).join('');
 
  list.scrollTop = list.scrollHeight;
}

function closeModal() {
  document.getElementById('post-modal').style.display = 'none';
  document.body.style.overflow = '';
  document.getElementById('modal-comment-input').value = '';
  document.getElementById('modal-comment-error').textContent = '';
  _modalPostId = null;
}


document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('post-modal');
  if (!modal) return;

  
  document.getElementById('modal-close').addEventListener('click', closeModal);
  modal.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeModal(); });

  
  document.getElementById('modal-like-btn').addEventListener('click', async () => {
    if (!_modalPostId) return;
    if (document.body.dataset.authenticated !== 'true') {
      window.location.href = '/accounts/login/';
      return;
    }
    const resp = await fetch(`/blog/${_modalPostId}/modal/like/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': CSRF_TOKEN }
    });
    const d = await resp.json();
    updateLikeUI(d.likes_count, d.liked);
  });

  
  document.getElementById('modal-comment-submit').addEventListener('click', async () => {
    const input = document.getElementById('modal-comment-input');
    const error = document.getElementById('modal-comment-error');
    const btn = document.getElementById('modal-comment-submit');
    const text = input.value.trim();

    if (!text) {
      error.textContent = 'Введите текст комментария';
      return;
    }

    btn.disabled = true;
    error.textContent = '';

    const formData = new FormData();
    formData.append('comment_text', text);

    const resp = await fetch(`/blog/${_modalPostId}/modal/comment/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': CSRF_TOKEN },
      body: formData
    });

    if (resp.ok) {
      const newComment = await resp.json();
      
      const list = document.getElementById('modal-comments-list');
      const noComments = list.querySelector('.no-comments');
      if (noComments) noComments.remove();

      const div = document.createElement('div');
      div.className = 'modal-comment';
      div.innerHTML = `<a href="/blog${newComment.author_url}">${newComment.author}</a><span>${newComment.text}</span>`;
      list.appendChild(div);
      list.scrollTop = list.scrollHeight;
      input.value = '';
    } else {
      const d = await resp.json();
      error.textContent = d.error || 'Ошибка при отправке';
    }

    btn.disabled = false;
  });
});

