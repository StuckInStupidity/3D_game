const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');
const mode = document.body.dataset.mode;
registerBtn.addEventListener('click', () => {
  container.classList.add('active');
});
loginBtn.addEventListener('click', () => {
  container.classList.remove('active');
});

document.addEventListener("click", function (e) {
    if (e.target.classList.contains("alert-close")) {
        const alert = e.target.parentElement;
        alert.style.opacity = "0";
        setTimeout(() => alert.remove(), 300);
    }
});

(function(){
  const $ = (sel, el=document) => el.querySelector(sel);
  const $$ = (sel, el=document) => Array.from(el.querySelectorAll(sel));

  function typeL() {
    const element = document.getElementById("typewriter");
    if (!element) return;
    const text = element.textContent;
    element.textContent = '';
    let index = 0;
    function add() {
      if (index < text.length) {
        element.textContent += text[index];
        index++;
        setTimeout(add, 55);
      }
    }
    add();
  }
  typeL();

  window.addEventListener('load', () => {
    const menu = document.getElementById('menu');
    if (menu) menu.checked = false;
  });
  const header = document.querySelector('[data-header]');
  const onScroll = () => {
    if (!header) return;
    const scrolled = window.scrollY > 8;
    header.classList.toggle('is-scrolled', scrolled);
  };
  window.addEventListener('scroll', onScroll, {passive: true});
  onScroll();

  const io = new IntersectionObserver((entries)=>{
    for (const e of entries){
      if (e.isIntersecting){
        e.target.classList.add('in-view');
        io.unobserve(e.target);
      }
    }
  }, {threshold: 0.18});
  $$('.reveal').forEach(el => io.observe(el));

})();